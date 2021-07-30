import spacy
from spacy.lang.fr.examples import sentences

r=spacy.explain("ADP")
print(r)
nlp = spacy.load("fr_core_news_sm")
doc = nlp("tu es pour moi ou contre la loi")
print(doc.text)
for token in doc:
    print(token.text, token.pos_, token.dep_, token.morph)