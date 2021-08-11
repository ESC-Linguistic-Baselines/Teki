#from teki_main_app import sentence_identification
import pickle

results = pickle.load( open ("debug.pickle","rb"))
# database=r"C:\Users\chris\Desktop\Teki\app_program_resources\default_files\default_training.csv"
#
# sentence_identification(results,database,False)

text = open("../app_program_resources/metric_data/spacy_data/ebay_system_results.csv", mode="w", encoding="utf-8")
for sen in results:
    res=results[sen]
    text.write(sen+"\n")
    for i in res:
        text.write(f"{i[0]},{i[1]},{i[2]}{i[3]},{i[4]}\n")
    text.write("\n")