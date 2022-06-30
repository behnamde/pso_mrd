"""
Spam Classification Using NLTK and SKLearn
Behnam Dehghani
"""

# Import necessary libraries
import numpy as np
import pandas as pd

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.ensemble import RandomForestClassifier

import pickle
import re


# Read dataset
path = "D:\\My Learning Materials\\python\\Test\\spam.csv"
data = pd.read_csv(path, usecols=['v1', 'v2'])
print(data.head())
print(data.info())

# tokenizing first messages to see the text is clean or not after removing stopwords
for text in data.v2[0]:
    print(">> " + text)
    text_tokens = word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
    print("+++ {}".format(tokens_without_sw))

# EDA
data.iloc[:, 0].value_counts().plot(kind='bar')


# Preprocessing
stemmer = PorterStemmer()
words = stopwords.words("english")

# new column that has only cleaned texts
data['cleaned'] = data['v2'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())

print(data['cleaned'][0])

# incoding labels and puting them into a new coulmn
data['label'] = data['v1'].apply(lambda x: 0 if x == 'spam' else 1)

# Vectorizing the cleaned data and making features out of them
vectorizer = TfidfVectorizer(min_df= 3, stop_words="english", sublinear_tf=True, norm='l2', ngram_range=(1, 2))
final_features = vectorizer.fit_transform(data['cleaned']).toarray()
final_features.shape

# X: Features, y: Target
X = data['cleaned']
y = data['label']

# Split the data set to train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

# Model Pipeline
pipeline = Pipeline([('vect', vectorizer),
                     ('chi',  SelectKBest(chi2, k=1200)),
                     ('clf', RandomForestClassifier())])

# Training the model and saving the initial model
model = pipeline.fit(X_train, y_train)
with open('RandomForest.pickle', 'wb') as f:
    pickle.dump(model, f)

# Evaluation the trained model
ytest = np.array(y_test)

print(classification_report(ytest, model.predict(X_test)))
print(confusion_matrix(ytest, model.predict(X_test)))

# Predict using the test dataset
print(model.predict(X_test))