import bs4
from bs4 import BeautifulSoup
document="sandbox/test.xml"
with open(document, mode="r", encoding="utf-8") as file:
    soup = bs4.BeautifulSoup(file, "lxml")
    xml_tag_id=list()
    for tag in soup.select("div[id]"):
        xml_tag_id.append(tag["id"])

def sentence_tokenizer(tokens_orth,abbrev):
    new_tokens = list()
    sentences = list()
    tokens_orth.append(" ")

    new_sentence=""

    punctuation="!",".","?"

    for tok in tokens_orth:
        # Wort
        if (tok[-1] in punctuation)==False:
            new_sentence+=tok+" "
            new_tokens.append(tok)

        # Satzterminierend
        else:

            new_sentence+=f"{tok} <END>"
            sentences.append(new_tokens)
            new_tokens = list()

    res=[new_sentence.split("<END>")]
    print(len(res[0]))
    return res


corpus_text = soup.find("div", id=xml_tag_id[2]).getText().strip().split()

sentence_tokenizer(corpus_text,list())