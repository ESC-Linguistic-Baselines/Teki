from app_resources.app_auxiliary_functions import DiscourseAnalysis
import pickle

data = pickle.load(open(r"C:\Users\chris\Desktop\Bachleorarbeit\oral.pickle","rb"))

for corpus_sentence_id in data:
    print(corpus_sentence_id)
    # sub_sentences = corpus_sentence_id[corpus_sentence_id]
    # sentence_info = DiscourseAnalysis.LanguageIndependentAnalysis(sub_sentences)
