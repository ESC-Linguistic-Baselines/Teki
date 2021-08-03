import spacy

def get_text(file):
    data=dict()
    nlp = spacy.load("en_core_web_sm")
    with open(file, mode="r", encoding="utf-8") as text_file,open("../app_resources/default/dev_training.csv", mode="w", encoding="utf-8") as res:
        for line in enumerate(text_file):
           sen=line[1].split()[:-1]
           doc=nlp(" ".join(sen))
           for token in doc:
               feat=line[1].split()[-1]
               feat=feat.replace("true","ORAL")
               feat=feat.replace("false","LIT")
               sen_num=f"SEN:{line[0]}"
               sen_id="SNACK_BAR"
               res.write(f"{token.text},{token.pos_},{token.dep_},{sen_num},{sen_id},{feat}\n")

    return data

get_text("test_set_3.txt")
