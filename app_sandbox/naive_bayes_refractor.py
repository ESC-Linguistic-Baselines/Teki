def get_text(file):

    file_data = dict()

    with open(file, mode="r", encoding="utf-8") as text_file:
        for line in text_file:
            line = line.strip()
            sentence = tuple(line.split()[:-1])
            feature = line.split()[-1]
            file_data[sentence] = feature

    return file_data


def doc_feature_count(file_data):

    feature_count = {"LIT": 0, "ORAL": 0}

    for doc in file_data:
        feature_count[file_data[doc]] = feature_count.get(file_data[doc]) + 1

    return feature_count


def word_feature_assignment(data):

    features = list()
    for sentence in data:
        for word in sentence:
            features.append((word, data[sentence]))

    return features


def feature_prob(features, prior_prob):
    lit_count, oral_count = dict(), dict()
    lit_tokens, oral_tokens = list(),list()

    vocabulary = set()

    results = dict()

    for word in features:
        vocabulary.add(word[0])
        if word[1] == "LIT":
            lit_tokens.append(word)
        else:
            oral_tokens.append(word)

    for word in features:
        if word[1] == "LIT":
            lit_count[word[0]] = lit_count.get(word[0], 0) + 1
        else:
            oral_count[word[0]] = oral_count.get(word[0], 0) + 1

    for word in vocabulary:
        if lit_count.get(word, 0) > 0:

            lit_prob = lit_count.get(word) / prior_prob["LIT"]

        else:
            # Smooth
            lit_prob = prior_prob["LIT"] / (sum(prior_prob.values()) ** 2)

        if oral_count.get(word, 0) > 0:
            oral_prob = oral_count.get(word) / prior_prob["ORAL"]

        else:
            # Smooth
            oral_prob = prior_prob["ORAL"] / (sum(prior_prob.values()) ** 2)

        results[word] = lit_prob, oral_prob

    return results


##############################################

def classify(text, probs, feat_count):
    lit_prob = feat_count["LIT"] / (sum(feat_count.values()))
    oral_prob = feat_count["ORAL"] / (sum(feat_count.values()))

    lit_smooth = feat_count["LIT"] / (sum(feat_count.values()) ** 2)
    oral_smooth = feat_count["ORAL"] / (sum(feat_count.values()) ** 2)
    prob_res = dict()

    for word in text:
        if bool(probs.get(word)):
            prob_res[word] = probs.get(word)
        else:
            prob_res[word] = lit_smooth, oral_smooth

    print(prob_res)
    for word in prob_res:
        lit_prob *= prob_res[word][0]
        oral_prob *= prob_res[word][1]

    print(lit_prob,oral_prob)
    if lit_prob > oral_prob:
        print(f"The text is lit: {lit_prob} .")
    else:
        print(f"The text is oral: {oral_prob} .")


def run_script(input, text):

    # Read File
    file = get_text(input)

    # prior prob of files
    feat_count = doc_feature_count(file)

    # Word Feature pair
    feature_set = word_feature_assignment(file)

    probs = feature_prob(feature_set, feat_count)

    classify(text, probs, feat_count)

###########################################################
# Hauptprogramm
###########################################################

if __name__ == "__main__":
    infile = r"test_set_2.txt"
    text = "a seat at the barwhich serves up surprisingly".split()

    run_script(infile, text)
