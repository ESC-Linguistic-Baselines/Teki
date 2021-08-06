from teki_main_app import sentence_identification
import pickle

p = pickle.load(open("debug.pickle","rb"))

f  = "app_core_resources/default_files/default_training.csv"
sentence_identification(p,database_file=f,system_evaluation=False)

