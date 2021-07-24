import csv
def get_freq(file):
    '''
    This function gets the counter for ORAL and LIT in the training file.
    It returns the frequency of the features and the entries from the csv files
    '''

    with open(file, mode="r", encoding="utf-8") as file_data:
        csv_reader = csv.reader(file_data, delimiter=",")
        file_data = [row for row in csv_reader]
        freq = {"ORAL": 0, "LIT": 0}

        sentence_id={(row[3],row[4],row[5]) for row in file_data}
        for sentence in sentence_id:
            entry=sentence[2]
            freq[entry] = freq.get(entry) + 1

        return freq,file_data

def get_probs(csv_results):
    '''
    This function returns the frequency of the oral and lit features for each word.
    '''
    results = dict()

    freq = csv_results[0]
    csv_data = csv_results[1]

    lit_freq,oral_freq = dict(),dict()
    lit_tokens,oral_tokens=list(),list()
    vocabluary = set()
    ng_smooth=sum(freq.values()) ** 2

    for element in csv_data:
        word,feat = element[0],element[5]
        vocabluary.add(word)

        if feat == "ORAL":
            oral_tokens.append((word, feat))
            oral_freq[element[0]] = oral_freq.get(element[0], 0) + 1

        elif feat == "LIT":
            lit_tokens.append((word, feat))
            lit_freq[element[0]] = lit_freq.get(element[0], 0) + 1


    for element in vocabluary:
        if lit_freq.get(element, 0) > 0:
            lit = lit_freq.get(element) / freq["LIT"]

        else:
            lit = freq["LIT"] / (ng_smooth)

        if oral_freq.get(element, 0) > 0:
            oral = oral_freq.get(element) / freq["ORAL"]

        else:
            oral = freq["ORAL"] / (ng_smooth)

        results[element] = oral,lit
    return results,freq

def classify(text, res):
   #Text classification
    probs,prior_prob=res[0],res[1]

    oral_prob,lit_prob=prior_prob["ORAL"],prior_prob["LIT"]
    orality = oral_prob/ (oral_prob + lit_prob)
    literality = lit_prob / (oral_prob + lit_prob)
    ng=sum(prior_prob.values()) ** 2
    orality_smooth = oral_prob/ ng
    literacy_smooth = lit_prob / ng

    sentence_prob = dict()

    for word in text:
        if bool(probs.get(word)):
            sentence_prob[word] = probs.get(word)

        else:
           sentence_prob[word] = orality_smooth, literacy_smooth

    for word in sentence_prob:

        orality *= sentence_prob[word][0]
        literality *= sentence_prob[word][1]

    if literality > orality :
        print(f" {text} is literal {literality}")
    else:
        print(f" '  {text} ' is oral {orality}")
    print(sentence_prob)
    input()
######


file=r"cl_2.csv"
data=get_freq(file)

res=get_probs(data)
text = "a seat at the bar which serves up surprisingly"
r=classify(text.split(),res)
