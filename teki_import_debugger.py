import pickle,re
from app_resources.app_auxiliary_functions import DiscourseAnalysis
#from teki_main_app import sentence_identification

def check (file):
    data = pickle.load(open(file, "rb"))
    database="app_resources/default/dev_training.csv"

    oral=0
    lit = 0
    unk = 0
    for corpus_sentence_id in data:
        sub_sentences = data[corpus_sentence_id]
        sentence_info = DiscourseAnalysis.FrenchBasedAnalysis(sub_sentences)
        feat = sentence_info.feature_assignment()[0]
        if feat == "UNK": unk+=1
        if feat == "LIT": lit+=1
        if feat == "ORAL": oral+=1
        # if feat == "ORAL":
        #     print(sentence_info.sentence_reconstruction()[1])
        #     print(feat,sentence_info.feature_assignment())
        #     print(sentence_info.feature_assignment())
        #     print("")

    lit_per=round(lit/(oral+lit+unk),4)*100
    oral_per=round(oral/(oral+lit+unk),4)*100
    unk_per = round(unk/(oral+lit+unk),4)*100
    res = {"lit":lit_per, "oral":oral_per, "unk":unk_per}

    print(file)
    for i in sorted(res,key=res.get,reverse=True):
        print(i,res[i])

check("oral.pickle")
print("")
check("lit.pickle")
