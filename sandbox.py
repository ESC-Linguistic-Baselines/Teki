import spacy
from spacy.lang.fr.examples import sentences

nlp = spacy.load("fr_core_news_sm")
doc = nlp("moi lui je le vois pas ")

for token in doc:
    print(token.text, token.pos_, token.dep_)