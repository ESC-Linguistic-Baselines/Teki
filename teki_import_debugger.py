import pickle
from app_resources.app_auxiliary_functions import DiscourseAnalysis


data = pickle.load(open("sms_pickle_data.pickle","rb"))
key=list(data.keys())
i=2
sentence=data[key[i]]

system = DiscourseAnalysis.PosSyntacticalAnalysis(sentence)
reconstruct=system.sentence_reconstruction()
system.feature_assignment()
print(reconstruct)