import pickle,re
from app_resources.app_auxiliary_functions import DiscourseAnalysis

data = pickle.load(open("pickle_data.pickle", "rb"))

for i in data:
    sub= data[i]
    system = DiscourseAnalysis(data).PosSyntacticalAnalysis(sub)
    reconstruct = system.feature_assignment ( )
    print(reconstruct)


