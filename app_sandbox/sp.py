import spacy
from spacy.lang.fr.examples import sentences


sentence="Cet homme, je l'ai vu très souvent"
nlp = spacy.load("fr_core_news_sm")
doc = nlp(sentence )

print(doc.text)
for token in doc:
    print(token.text, token.pos_, token.dep_)