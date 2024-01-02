# Load libraries
import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("core/chatbot/DescisionTree/data.csv")

le_type = LabelEncoder()
df['genre_type'] = le_type.fit_transform(df['genre_type'])

le_author = LabelEncoder()
df['liked_author'] = le_author.fit_transform(df['liked_author'])

le_nation = LabelEncoder()
df['nation'] = le_nation.fit_transform(df['nation'])

le_modern_or_classic = LabelEncoder()
df['modern_or_classic'] = le_modern_or_classic.fit_transform(df['modern_or_classic'])

le_target = LabelEncoder()
df['target'] = le_target.fit_transform(df['target'])

le_content = LabelEncoder()
df['content'] = le_content.fit_transform(df['content'])

#split dataset in features and target variable
feature_cols = ['genre_type', 'content', 'target', 'modern_or_classic','nation', 'liked_author']
X = df[feature_cols] # Features
y = df.result_book # Target variable

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # 70% training and 30% test

# Create Decision Tree classifer object
clf = DecisionTreeClassifier(criterion="entropy", max_depth=3)

# Train Decision Tree Classifer
clf = clf.fit(X_train.values,y_train)

#Kiểm tra nhãn thể loại có thuộc dataset chưa
def genre_validation(genre_label):
    try:
        le_type.transform([genre_label])
    except:
        return False
    return True

#Kiểm tra nhãn tên tác giả có thuộc dataset chưa
def author_validation(author_label):
    try:
        le_author.transform([author_label])
    except:
        return False
    return True

#Kiểm tra nhãn tên quốc gia có thuộc dataset chưa
def nation_validation(nation_label):
    try:
        le_nation.transform([nation_label])
    except:
        return False
    return True

#Kiểm tra nhãn xu hướng(cổ điển hay hiện đại) có thuộc dataset chưa
def modern_or_classic_validation(modern_or_classic_label):
    try:
        le_modern_or_classic.transform([modern_or_classic_label])
    except:
        return False
    return True

#Kiểm tra nhãn mục đích có thuộc dataset chưa
def target_validation(target_label):
    try:
        le_target.transform([target_label])
    except:
        return False
    return True

#Kiểm tra nhãn nội dung có thuộc dataset chưa
def content_validation(content_label):
    try:
        le_content.transform([content_label])
    except:
        return False
    return True


#Gợi ý sách
def recommendation_book(data_predict):
    #Predict the response for test dataset
    # data_predict = {
    #     'genre_type': ['Tình cảm'],
    #     'liked_author': ['Nguyễn Nhật Ánh'],
    #     'nation': ['Nước ngoài'],
    #     'modern_or_classic': ['Hiện đại'],
    #     'target': ['Phát triển'],
    #     'content': ['Quê hương và gia đình']
    # }
    result_data = []
    result_data.append(le_type.transform(data_predict['genre_type'])[0])
    result_data.append(le_content.transform(data_predict['content'])[0])
    result_data.append(le_target.transform(data_predict['target'])[0])
    result_data.append(le_modern_or_classic.transform(data_predict['modern_or_classic'])[0])
    result_data.append(le_nation.transform(data_predict['nation'])[0])
    result_data.append(le_author.transform(data_predict['liked_author'])[0])
    #print(result_data)
    y_pred = clf.predict([result_data])

    return y_pred[0]
