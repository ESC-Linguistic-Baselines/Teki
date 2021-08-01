from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score


data= pd.read_csv("classify.csv")
vectorizer = CountVectorizer()
text = data["text"].values
counts = vectorizer.fit_transform(text)

classifier = MultinomialNB()
classes=data["feat"].values
classifier.fit(counts,classes)

# test_msgs = ['$$$ Free Cash From Nigerian Prince!', "Hey, what did you think of last night's episode of 'Friends'?"]
# test_msg_counts = vectorizer.transform(test_msgs)

scores = cross_val_score(classifier,counts, classes, cv=5)

print(scores)