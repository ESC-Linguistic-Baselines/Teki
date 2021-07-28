import pickle,csv
from teki_main_app import sentence_identification
from app_resources.app_auxiliary_functions import DiscourseAnalysis
from app_resources.app_auxiliary_functions import save_sentences

# pickle file
file = r"C:\Users\chris\Desktop\Bachleorarbeit\pickle_data.pickle"
load = pickle.load(open(file, "rb"))

database = "app_resources/app_dev/dev_results/naive_bayes/emoticons.csv"
system_corpus = DiscourseAnalysis(load).redacted_corpus()

sentence_one_gold = load["e05p-001-sen_no-0"]
sentence_one_system = system_corpus["e05p-001-sen_no-0"]


s=DiscourseAnalysis.PosSyntacticalAnalysis(sentence_one_system)
res=DiscourseAnalysis.PosSyntacticalAnalysis(sentence_one_system).feature_assignment()

# print(res,s.sentence_reconstruction())
# print()
#
# print(DiscourseAnalysis.TokenAnalysis(sentence_one_system).feature_assignment())

sentence_identification(load, database,True)