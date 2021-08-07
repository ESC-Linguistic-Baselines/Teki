from teki_main_app import sentence_identification
import pickle

results = pickle.load( open ("debug.pickle","rb"))
database=r"C:\Users\chris\Desktop\Teki\app_program_resources\default_files\default_training.csv"

sentence_identification(results,database,False)