from teki_main_app import get_text
from teki_main_app import analyze_content
from teki_main_app import spacy_tagger
import pickle
from teki_main_app import  identify_oral_literal
from teki_main_app import  get_freq

text=r"C:\Users\chris\Desktop\Bachleorarbeit\app_resources\train_files\cl_2_set.csv"

print(get_freq(text))





# res=get_text(text)
# r=analyze_content(res)
# data=open("data.pickle","wb")
# pickle.dump(r,data)
# #
# # r = pickle.load( open( "data.pickle", "rb" ) )
# # sp=spacy_tagger(r)
# #
# # data=open("data_3.pickle","wb")
# # pickle.dump(sp,data)
# # #
#
# # senten = pickle.load(open("sandbox/data_3.pickle", "rb"))
# # database=r"C:\Users\chris\Desktop\Bachleorarbeit\app_resources\train_files\pickle_set.csv"
# #
# # identify_oral_literal(senten,database)