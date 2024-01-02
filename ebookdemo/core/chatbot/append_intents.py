import re
import sys

# patterns_covert = {
#     '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
#     '[đ]': 'd',
#     '[èéẻẽẹêềếểễệ]': 'e',
#     '[ìíỉĩị]': 'i',
#     '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
#     '[ùúủũụưừứửữự]': 'u',
#     '[ỳýỷỹỵ]': 'y'
# }

# def convert(text):
#     output = text
#     for regex, replace in patterns_covert.items():
#         output = re.sub(regex, replace, output)
#         # deal with upper case
#         output = re.sub(regex.upper(), replace.upper(), output)
#     return output


import json

from random import choices, choice

def create_response(line_response, books): #Thêm sách cho từng reponse của một thể loại
    random_books = []

    size_books = len(books)
    if len(books) >= 3:
        size_books = 3

    for i in range(size_books):
        random_book = choice(books)
        while random_book in random_books:
            random_book = choice(books)
        random_books.append(random_book)

    for book in random_books:
        line_response += book.book_name + ', '

    return line_response[0:-2]

def reponse_tag_exist(tag, books, d): #Cập nhật reponse cho thể loại đã tồn tại
    responses_new = []
    responses_new.append(create_response(line_response="Gợi ý của chúng tôi về " + tag + " dành cho bạn: ", books=books))
    responses_new.append(create_response(line_response="Một số cuốn sách thuộc thể loại " + tag + " : ", books=books))
    responses_new.append(
        create_response(line_response="Những cuốn sách " + tag + " có thể bạn sẽ thích: ", books=books))
    d['responses'] = responses_new

def reponse_tag_new(genre, tag, books): #Cập nhật reponse cho thể loại mới
    genre_convert = genre.genre_name
    patterns = [
        genre_convert,
        "Tôi muốn tìm sách về " + genre_convert,
        "Thể loại " + genre_convert,
        "Gợi ý sách về " + genre_convert
    ]
    responses = []
    responses.append(create_response(line_response="Gợi ý của chúng tôi về " + tag + " dành cho bạn: ", books=books))
    responses.append(create_response(line_response="Một số cuốn sách thuộc thể loại " + tag + " : ", books=books))
    responses.append(create_response(line_response="Những cuốn sách " + tag + " có thể bạn sẽ thích: ", books=books))

    new_intent = {
        "tag": tag,
        "patterns": patterns,
        "responses": responses
    }
    return new_intent

def reponse_most_book(books_all, d):
    most_viewed_book = max(books_all, key=lambda book: book.book_view)
    most_viewed_book_name = most_viewed_book.book_name
    responses_most_viewed = []
    responses_most_viewed.append("Cuốn sách " + most_viewed_book_name + " có nhiều lượt xem nhất hiên tại.")
    responses_most_viewed.append("Cuốn sách được xem nhiều nhất là " + most_viewed_book_name)
    responses_most_viewed.append("Cuốn sách có nhiều view nhất " + most_viewed_book_name)
    d['responses'] = responses_most_viewed

def reponse_detail_book(book):
    responses_detail = []
    description = book.book_description.split()
    description = description[0: 15 if len(description) > 15 else len(description)]
    description = ' '.join(description)
    response = "Chi tiết về sách " + book.book_name + " : " + "Tác giả: " + book.book_author + ", Mô tả: " + description + "..., Lượt xem: " + str(book.book_view) + ", Điểm rating: " + str(book.book_rating) + '.'
    responses_detail.append(response)
    return responses_detail

def reponse_detail_new(book, tag):
    book_name_convert = book.book_name
    patterns = [
        book_name_convert,
        "Chi tiết về " + book_name_convert,
        "Chi tiết về cuốn sách " + book_name_convert,
        "Sách " + book_name_convert + " như thế nào",
        "Thông tin chi tiết về sách " + book_name_convert
    ]
    responses = []
    responses.append(reponse_detail_book(book))
    new_intent = {
        "tag": tag,
        "patterns": patterns,
        "responses": responses
    }
    return new_intent

def append_intents(genres, books_all):
    with open('core/chatbot/intents_new.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    for genre in genres:    #Cập nhật response theo thể loại
        tag = genre.genre_name
        books = genre.book.all()
        exist_tag = False
        for d in data['intents']:
            if d['tag'] == tag :
                exist_tag = True
                reponse_tag_exist(tag, books, d)

        if exist_tag == False: #Chưa có danh mục này trong data
            new_intent = reponse_tag_new(genre, tag, books)
            # Thêm dữ liệu mới vào danh sách intents
            data["intents"].append(new_intent)

    #Theo lượt xem nhiều nhất
    for d in data['intents']:
        if d['tag'] == 'most view':
            reponse_most_book(books_all=books_all, d=d)

    #Theo chi tiet sach
    for book in books_all:
        tag = book.book_name
        exist_tag = False
        for d in data['intents']: # Cập nhật thông tin khi sách đã tồn tại trong tập dữ liệu
            if d['tag'] == tag :
                exist_tag = True
                d['responses'] = reponse_detail_book(book)

        if exist_tag == False: #Thêm chi tiết sách mới vào tập dữ liệu
            new_intent = reponse_detail_new(book, tag)
            data["intents"].append(new_intent)  # Thêm dữ liệu mới vào danh sách intents


    # Lưu tệp JSON với dữ liệu mới
    with open('core/chatbot/intents_new.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
