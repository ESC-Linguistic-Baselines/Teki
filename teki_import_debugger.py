import pickle,re
from app_resources.app_auxiliary_functions import DiscourseAnalysis
from app_resources.app_auxiliary_functions import evaluation
from teki_main_app import sentence_identification

data = pickle.load(open("oral.pickle", "rb"))
database = "app_resources/default/dev_training.csv"

evaluation()