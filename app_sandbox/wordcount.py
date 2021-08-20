import csv
with open("system_20_08_2021_09_18_08.csv",mode="r",encoding="utf-8") as system, \
        open("gold_20_08_2021_09_18_08.csv",mode="r",encoding="utf-8")  as gold:
    csv_reader_1 = csv.reader(system, delimiter = ",")
    csv_reader_2 = csv.reader(gold, delimiter=",")
    for sys,gold in zip(csv_reader_1,csv_reader_2):
        print(sys[-1], gold[-1])