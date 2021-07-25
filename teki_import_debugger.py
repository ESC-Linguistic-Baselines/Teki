from teki import get_text
from teki import analyze_content
from teki import spacy_tagger
import pickle
from teki import  identify_oral_literal

# # text=r"C:\Users\chris\Desktop\Bachleorarbeit\app_resources\app_dev\dev_files\ebayfr-e05p_0_149.xml"
# #
# # res=get_text(text)
# # r=analyze_content(res)
# data=open("data.pickle","wb")
# pickle.dump(r,data)

# r = pickle.load( open( "data.pickle", "rb" ) )
# sp=spacy_tagger(r)
#
# data=open("data_3.pickle","wb")
# pickle.dump(sp,data)
# #

senten = pickle.load(open("sandbox/data_3.pickle", "rb"))
database=r"C:\Users\chris\Desktop\Bachleorarbeit\app_resources\train_files\pickle_set.csv"

identify_oral_literal(senten,database)