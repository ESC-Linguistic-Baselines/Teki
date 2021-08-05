import pickle
from teki_main_app import sentence_identification
r = pickle.load(open("p.picke", "rb"))

database= r"C:\Users\chris\Desktop\Bachleorarbeit\app_resources\default_docs\default_training.csv"
sentence_identification(r,database,False)
