import random
import json

import torch

from .model import NeuralNet
from .nltk_utils import bag_of_words, pyvi_tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('core/chatbot/intents_new.json', 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)


FILE = "core/chatbot/data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"


from .DescisionTree.recommendation import genre_validation,author_validation, nation_validation, modern_or_classic_validation, target_validation, content_validation, recommendation_book

def tag_validation(tag, i, data_predict):
    data_validation = False
    if i == 0:
        data_validation = genre_validation(tag)
        print("Check valid: ", data_validation)
        if data_validation: data_predict['genre_type'] = [tag]
    elif i == 1:
        data_validation = author_validation(tag)
        print("Check valid: ", data_validation)
        if data_validation: data_predict['liked_author'] = [tag]
    elif i == 2:
        data_validation = nation_validation(tag)
        print("Check valid: ", data_validation)
        if data_validation: data_predict['nation'] = [tag]
    elif i == 3:
        data_validation = modern_or_classic_validation(tag)
        print("Check valid: ", data_validation)
        if data_validation: data_predict['modern_or_classic'] = [tag]
    elif i == 4:
        data_validation = target_validation(tag)
        print("Check valid: ", data_validation)
        if data_validation: data_predict['target'] = [tag]
    elif i == 5:
        data_validation = content_validation(tag)
        print("Check valid: ", data_validation)
        if data_validation: data_predict['content'] = [tag]
    return data_validation

def return_question(step):
    question = [
        "Thể loại bạn thích là gì? (Khoa học viễn tưởng, Tình cảm, Kinh dị,...)",
        "Tác giả bạn thích là gì?(Stepehn King, H. G. Well,...)",
        "Bạn thích đọc sách Việt Nam hay Nước ngoài?",
        "Xu hướng đọc sách là Cổ điển hay Hiện đại?",
        "Mục đích đọc sách của bạn là gì?(Học hỏi, Giải trí, Phát triển bản thân,...)",
        "Nội dung sách bạn thích là gì? (Khám phá vũ trụ, Du hành thời gian, Quê hương và gia đình,...)"
    ]
    return question[step]

def recommendation_1(sentence1, step, data_predict):
    # question = [
    #             "Thể loại bạn thích là gì? (Khoa học viễn tưởng, Tình cảm, Kinh dị,...)",
    #             "Tác giả bạn thích là gì?(Stepehn King, H. G. Well,...)",
    #             "Bạn thích đọc sách Việt Nam hay Nước ngoài?",
    #             "Xu hướng đọc sách là Cổ điển hay Hiện đại?",
    #             "Mục đích đọc sách của bạn là gì?(Học hỏi, Giải trí, Phát triển bản thân,...)",
    #             "Nội dung sách bạn thích là gì? (Khám phá vũ trụ, Du hành thời gian, Quê hương và gia đình,...)"
    #             ]
    # data_predict = {
    #     'genre_type': [''],
    #     'liked_author': [''],
    #     'nation': [''],
    #     'modern_or_classic': [''],
    #     'target': [''],
    #     'content': ['']
    # }
    length_question = 5
    if step <= length_question:
        #print("Vui lòng trả lời câu hỏi")
        #print(return_question(step))
        #sentence1 = input("You: ")

        sentence1 = pyvi_tokenize(sentence1)
        X1 = bag_of_words(sentence1, all_words)
        X1 = X1.reshape(1, X1.shape[0])
        X1 = torch.from_numpy(X1).to(device)
        output1 = model(X1)
        _, predicted1 = torch.max(output1, dim=1)
        tag1 = tags[predicted1.item()]
        probs1 = torch.softmax(output1, dim=1)
        prob1 = probs1[0][predicted1.item()]

        if prob1.item() > 0.75:
            # if tag1 == "Kết thúc gợi ý":
            #     print(f"{bot_name}: Kết thúc quá trình gợi ý")
            #     return "Kết thúc quá trình gợi ý"
            for intent1 in intents['intents']:
                if tag1 == intent1["tag"]:
                    print("TAG 1", tag1)
                    data_validation1 = tag_validation(tag1, step, data_predict)
                    if data_validation1 == True:
                        #print(data_predict)
                        #print(f"{bot_name}: {random.choice(intent1['responses'])}")
                        return [random.choice(intent1['responses']), "success"]
                    else:
                        #print(f"{bot_name}: Vui lòng trả lời lại câu hỏi")
                        return ["Vui lòng trả lời lại câu hỏi", "fail"]
        else:
            print(f"{bot_name}: I do not understand...")
            return ["I do not understand...", 'fail']

def result_recommend(data_predict):
    book_name = recommendation_book(data_predict)
    return book_name





def get_response(msg):
    intents = reload_intents() # Lấy dữ liệu mới nhất (sau train)
    sentence = pyvi_tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return [random.choice(intent['responses']), tag]

    return "Vui lòng cung cấp thông tin phù hợp..."


def reload_intents():
    with open('core/chatbot/intents_new.json', 'r', encoding='utf-8') as json_data:
        intents = json.load(json_data)
    return intents

