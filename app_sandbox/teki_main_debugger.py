from teki_main_app import sentence_identification
import pickle

results = pickle.load(open ("debug.pickle", "rb"))
database=r"default_training.csv"
#
sentence_identification(results,database,False)

