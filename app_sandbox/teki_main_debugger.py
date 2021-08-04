from app_resources.app_auxiliary_functions import DiscourseAnalysis
import pickle

collective_results_tagged = pickle.load(open(r"/oral.pickle", "rb"))

for corpus_sentence_id in collective_results_tagged:
    sub_sentences = collective_results_tagged[corpus_sentence_id]
    sentence_info = DiscourseAnalysis.LanguageIndependentAnalysis(sub_sentences)
    feat = sentence_info.feature_assignment()
    sentence = sentence_info.sentence_reconstruction()[1]
    sen_id = sentence_info.sentence_reconstruction()[2]
    sen_num = sentence_info.sentence_reconstruction()[3]
    print(feat)