import bs4
from bs4 import BeautifulSoup
import re

document="sandbox/test.xml"
with open(document, mode="r", encoding="utf-8") as file:
    soup = bs4.BeautifulSoup(file, "lxml")
    xml_tag_id=list()
    for tag in soup.select("div[id]"):
        xml_tag_id.append(tag["id"])

def sentence_tokenizer(tokens_orth,abbrev):
    new_tokens = list()
    sentences = list()
    new_sentence=""
    regex=re.compile("[a-zàâçéèêëîïôûùüÿñæœ]+[.!?]|[*!?.]|\s[.·]+")

    for tok in tokens_orth:

        if regex.findall(tok):
            new_sentence += f" {tok} <END>"
            new_tokens.append(tok)
        else:
            new_sentence += f" {tok}"

    new=new_sentence.split("<END>")
    res=[sen for sen in new if bool(sen)==True]

    return [res]


corpus_text = soup.find("div", id=xml_tag_id[2]).getText().strip().split()
#corpus_text="tu es qui? je suis chez moi!"
c="Oui, une fin est prévue, en cherchant on tombe rapidement sur des chiffres mais ceux-ci ne se sont jamais montrés très précis dans le passé ... On parle de quelques années, mais sans doute pas une dizaine"
corpus_text=c.split()

s=sentence_tokenizer(corpus_text,list())

print(s)