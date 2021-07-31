import pickle,re
from app_resources.app_auxiliary_functions import DiscourseAnalysis

data = pickle.load(open("pickle_data.pickle", "rb"))

for i in data:
    sub= data[i]
    system = DiscourseAnalysis(data).TokenAnalysis(sub)
    point = system.feature_assignment()
    print(point)



