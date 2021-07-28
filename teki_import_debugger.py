import csv

def evaluate_naive_bayes():

    gold_file = "app_resources/app_dev/dev_results/naive_bayes/gold_28_07_2021_33_27_.csv"
    system_file = "app_resources/app_dev/dev_results/naive_bayes/system_28_07_2021_33_27_.csv"

    gold_results = dict()
    system_results = dict()

    feat_1 = "ORAL"
    feat_2 = "LIT"

    true_positive = 0
    false_positive = 0
    false_negative = 0
    true_negative = 0

    with open(gold_file, mode="r", encoding="utf-8") as gold, open(system_file, mode="r", encoding="utf-8") as system:
        csv_gold_reader, csv_system_reader = csv.reader(gold, delimiter=","), csv.reader(system, delimiter=",")

        for row in csv_gold_reader:
            key = row[3]+row[4]
            value = row[5]
            gold_results[key] = value

        for row in csv_system_reader:
            key = row[3]+row[4]
            system_results[key] = row[5]

    for i in gold_results:
        gold_res = gold_results[i]
        sys_res=system_results[i]

        if gold_res == feat_1 and sys_res == feat_1:
            true_positive += 1

        elif gold_res != feat_1 and sys_res != feat_1:
            true_negative += 1

        elif gold_res != feat_1 and sys_res == feat_2:
            false_positive += 1

        elif gold_res == feat_1 and sys_res != feat_2:
            false_negative+= 1

        print(i,  system_results[i], gold_results[i])
    results = {"TP": true_positive, "FP": false_positive, "FN": false_negative, "TN": true_negative}
    print(results)


evaluate_naive_bayes()