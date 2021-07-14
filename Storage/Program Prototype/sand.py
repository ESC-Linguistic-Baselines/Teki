from textblob.classifiers import NaiveBayesClassifier
data=list()
with open ("test_set_1") as file:
    for line in file:
        res=" ".join(line.split()[:-1]),line.split()[-1]
        data.append(res)

cl = NaiveBayesClassifier(data[:2])

# Classify some text
text="On le fait déjà. Ce que je te dis c'est que si tu passes de la proportion actuelle de renouvelable"

sentence=cl.classify(text)
acc=cl.accuracy(data[3:])

print(acc)  # "pos"

 # Show 5 most informative features
cl.show_informative_features(5)