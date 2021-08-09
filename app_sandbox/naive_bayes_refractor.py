def get_text(file):
    data=dict()

    with open(file, mode="r", encoding="utf-8") as text_file:
        for line in text_file:
            line=line.strip()
            sentence = tuple(line.split()[:-1])
            feature=line.split()[-1]
            data[sentence]=feature
    return data

def doc_prior(data):
    prob={"true":0,"false":0}

    for doc in data:
        prob[data[doc]]=prob.get(data[doc])+1

    s=sum(prob.values())

    prob["true"]=prob["true"]
    prob["false"]=prob["false"]

    return prob

def feature_extraction (data):

    features=list()
    for sentence in data:
        for word in sentence:

            features.append((word,data[sentence]))

    return features

def feature_prob(features,prior_prob):

    true_count=dict()
    false_count=dict()

    vobulary= set()

    true_tokens=list()
    false_tokens=list()

    res=dict()

    for word in features:
        vobulary.add(word[0])
        if word[1]=="true": true_tokens.append(word)
        else:false_tokens.append(word)

    for word in features:
        if word[1]=="true": true_count[word[0]]=true_count.get(word[0],0)+1
        else:false_count[word[0]] = false_count.get(word[0], 0)+1

    for word in vobulary:
        if true_count.get(word,0) > 0:
            tr=true_count.get(word)/prior_prob["true"]


        else:
            tr=prior_prob["true"]/(sum(prior_prob.values())**2)

        if false_count.get(word,0) > 0:

            fl=false_count.get(word)/prior_prob["false"]
            print(false_count.get(word),prior_prob["false"])
        else:
            fl=prior_prob["false"]/(sum(prior_prob.values())**2)

        res[word]=tr,fl

    return res

##############################################

def classify(text,probs,prior_prob):
    true=prior_prob["true"]/(prior_prob["true"]+prior_prob["false"])
    false=prior_prob["false"]/(prior_prob["true"]+prior_prob["false"])
    true_smooth=prior_prob["true"]/(sum(prior_prob.values())**2)
    false_smooth=prior_prob["false"]/(sum(prior_prob.values())**2)
    s = dict()


    for word in text:
        if bool(probs.get(word)):
            s[word]=probs.get(word)

        else:
            s[word] = true_smooth, false_smooth


    for word in s:

        true*=s[word][0]


        false*=s[word][1]

    res = true, false
    ans=1

    system_results = {"TP": 0, "FP": 0, "FN": 0}

    if true > false:

        print(f" is true with {true}")
    else:
        print(f" ' {text} ' is false with ",false)



def run_script(input,text):

    # Read File
    file = get_text(input)

    # prior prob of files
    prior_prob=doc_prior(file)

    feature_set=feature_extraction(file)
    probs=feature_prob(feature_set,prior_prob)

    classify(text,probs,prior_prob)

###########################################################
# Hauptprogramm
###########################################################

if __name__ == "__main__":

    # noinspection PyInterpreter
    input = r"test_set_3.txt"
    text = "Vous dites imbécile"

    run_script(input,text.split())
    get_text("test_set_3.txt")
