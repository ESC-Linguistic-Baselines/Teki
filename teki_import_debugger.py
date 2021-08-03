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
        sentence_info = DiscourseAnalysis.PosSyntacticalAnalysis(sub_sentences)
        feat = sentence_info.feature_assignment()[0]
        if feat == "UNK": unk+=1
        if feat == "LIT": lit+=1
        if feat == "ORAL": oral+=1
        # if feat == "ORAL":
        #     print(sentence_info.sentence_reconstruction()[1])
        #     print(feat,sentence_info.feature_assignment())
        #     print("")

    print("LIT",lit)
    print("ORAL",oral)
    print("UNK",unk)

check("oral.pickle")
print("")
check("lit.pickle")
