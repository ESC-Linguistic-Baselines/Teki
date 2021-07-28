import pickle
from app_resources.app_auxiliary_functions import DiscourseAnalysis

data = pickle.load(open("pickle_data.pickle","rb"))

sentence = data["e05p-003-sen_no-1"]
system = DiscourseAnalysis.PosSyntacticalAnalysis(sentence).feature_assignment()

print(system)