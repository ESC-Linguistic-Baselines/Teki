import pickle
# from teki_main_app import sentence_identification
from app_resources.app_auxiliary_functions import DiscourseAnalysis

file = r"C:\Users\chris\Desktop\Bachleorarbeit\pickle_data.pickle"
load = pickle.load(open(file, "rb"))
database="app_resources/app_dev/dev_results/naive_bayes/system.csv"

new_corpus=DiscourseAnalysis(load).redacted_corpus()
print(new_corpus)