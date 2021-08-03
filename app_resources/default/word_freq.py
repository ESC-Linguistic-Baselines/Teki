import csv

count = dict()

with open ("default_result_sentence.csv",mode="r",  encoding="utf-8") as res:
    csv_reader = csv.reader(res,delimiter = ",")

    for row in csv_reader:
        for word in row[0].split():
            count[word] = count.get(word,0) + 1

for word in sorted(count,key=count.get,reverse=False):
    print(word,count[word])