import spacy
doc = nlp("This is a sentence.")
lemmatizer = nlp.add_pipe("lemmatizer")
# This usually happens under the hood
processed = lemmatizer(doc)