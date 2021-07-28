import pickle,re
from app_resources.app_auxiliary_functions import DiscourseAnalysis


data = pickle.load(open("sms_pickle_data.pickle","rb"))
# key=list(data.keys())
# i="cmr-88milsms-a8-sen_no-0"
# sentence=data[i]
#
# system = DiscourseAnalysis.PosSyntacticalAnalysis(sentence)
# reconstruct=system.sentence_reconstruction()
# r=system.feature_assignment()
# print(reconstruct)
# print(r)

# print(reconstruct)
for i in data:
    sentence=data[i]
    system = DiscourseAnalysis.PosSyntacticalAnalysis(sentence)
    feat=system.feature_assignment()
    print(i,feat,system.sentence_reconstruction())

