import pickle


text = pickle.load(open("../oral.pickle", "rb"))

for i in text:
    print(i)
    for entry in i[]:
        print(entry)