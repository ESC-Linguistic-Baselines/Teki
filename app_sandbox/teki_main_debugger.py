from teki_main_app import generate_training_data
import pickle

results = pickle.load(open ("debug.pickle", "rb"))
database=r"default_training.csv"
#
generate_training_data(results,database,False)

