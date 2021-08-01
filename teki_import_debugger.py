import pickle,re
from app_resources.app_auxiliary_functions import DiscourseAnalysis
from teki_main_app import sentence_identification

data = pickle.load(open("coll_.pickle", "rb"))
database="app_resources/default/dev_training.csv"
sentence_identification(data,database,True)

