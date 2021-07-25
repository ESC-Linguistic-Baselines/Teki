from teki_main_app import get_text
from teki_main_app import analyze_content
from teki_main_app import spacy_tagger
import pickle
from teki_main_app import  identify_oral_literal
from teki_main_app import  get_freq
from teki_main_app import get_probs
from teki_main_app import classify

text=r"C:\Users\chris\Desktop\Bachleorarbeit\app_resources\train_files\cl_2_upated.csv"
c="a seat at the bar which serves up surprisingly"

freq=get_freq(text)

prob=get_probs(freq)
print(prob)

print(classify(c.split(),prob))



