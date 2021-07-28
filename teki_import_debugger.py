from app_resources.app_auxiliary_functions import sentence_tokenizer


a="Non!!!!!!!!! Pitie!!!!!!!! il refai le cours de la semaine derniere"

res=sentence_tokenizer(a.split())

print(res[0])

import spacy
import contextualSpellCheck

nlp = spacy.load("fr_core_news_sm")
sentence = "Ok keep cool pr l'entreprise et tiens moiiiiiiiiiiii au jus quand tu l'as trouvée ^^ et bon séjour toulousain :P bisous ;-)"

doc = nlp(res[0])

print(doc.text)
for token in doc:
    print(token.text, token.pos_, token.dep_)


