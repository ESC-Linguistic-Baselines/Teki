import spacy
nlp = spacy.load("fr_core_news_sm")

doc = nlp(u"je serai")

for token in doc:
    print(token, token.lemma, token.lemma_)