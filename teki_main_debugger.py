import pickle,re
from app_resources.app_auxiliary_functions import DiscourseAnalysis
from app_resources.app_auxiliary_functions import system_evaluation
from teki_main_app import sentence_identification

data = pickle.load(open("app_sandbox/oral.pickle", "rb"))
database = "app_resources/app_common_default_docs/default_training.csv"

system_evaluation()