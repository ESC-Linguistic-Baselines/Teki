
def sentence_tokenizer(tokens_orth):
    new_tokens = list()
    sentences = list()
    tokens_orth.append(" ")

    for tok in tokens_orth:
        context = tokens_orth.index(tok)
        # Wort
        if tok.endswith(".") == False:
            new_tokens.append(tok)

        # Satzterminierend
        else:
            if tokens_orth[context+1].islower():
                new_tokens.append(tok)

            else:
                new_tokens.append(tok[:-1])
                new_tokens.append(".")
                if tokens_orth[context].endswith(".") and tokens_orth[context + 1].endswith("."):
                    continue

                else:

                    sentences.append(new_tokens)
                    new_tokens=list()

    return sentences

#tokens="Das ist ein Bsp-Text, d.h. er enthält bzw. beinhaltet i.A. Sonderzeichen. Hier beginnt ein zweiter Satz. Und hier eine unbek. schoene Abkuerzung. Und hier eine schw. Abkuerzung."
tokens="L'histoire du nu non consenti est un peu conne. Je suis la. Et toi. Je suis la? Et toi. Mon."
t=tokens.split()
tk=sentence_tokenizer(t)

import spacy
nlp = spacy.load("fr_core_news_sm")

def tagger(corpus_content):
    """
    This function relies on the Spacy module for assessing the linguistic properties of a given sentence or a batch of sentences.
    """


    result= {sen:list() for sen in range(len(corpus_content)) }

    for i in range (len(corpus_content)):
        s=" ".join(corpus_content[i])

        doc=nlp(s)
        for token in doc:
            sentence_results=token.text, token.pos_, token.dep_
            result[i].append(sentence_results)

    return result

tagger(tk)