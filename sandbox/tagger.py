import pickle,csv

filename="corpus_content.pickle"
infile = open(filename,'rb')
sentence_results = pickle.load(infile)
infile.close()

analysis_results="app_resources/train_files/training_res.csv"
fnames ="token_text","token_pos","token_dep","token_id","oral_literate"

sentence=""
pos={}

analysis_results=r"C:\Users\chris\Desktop\Bachleorarbeit\app_resources\train_files\training_res.csv"
fnames ="token_text","token_pos","token_dep","token_id","oral_literate"

import spacy

def spacy_tagger(corpus_content):
    """
    After the the texts have been parsed into sentences,
    the respective sentences will then be tokenized
    """

    print("The individual sentences are now being tagged for parts of speech. Please wait...")

    print(corpus_content)
    corpus=corpus_content[0][0]
    tag=corpus_content[1]
    result = {sen: list() for sen in range(len(corpus))}
    nlp = spacy.load("fr_core_news_sm")

    for i in range(len(corpus)):
        s = "".join(corpus[i])
        doc = nlp(s)
        for token in doc:
            sentence_results = token.text, token.pos_, token.dep_
            result[i].append((sentence_results))


    input("The sentences have been succesfully tagged. Please press enter to continue...")
    print(result)
    return (result,tag)


def identify_oral_literal(sentence_results,database):
    pos = {}


    analysis_results = database
    fnames = "token_text", "token_pos", "token_dep", "token_id","sen_no", "oral_literate"

    def res(sen_info, feature, ID,sen_no):

                with open(analysis_results, mode="a", encoding="utf-8", newline="") as analysis:
                    writer = csv.DictWriter(analysis, fieldnames=fnames)

                    for entry in sen_info:

                        tok_txt = entry[0]
                        tok_pos = entry[1]
                        tok_dep = entry[2]

                        writer.writerow(
                            {"token_text": tok_txt,
                             "token_pos": tok_pos,
                             "token_dep": tok_dep,
                             "token_id": ID+f"{sen_no}",
                             "sen_no":f"SEN:{sen_no}",
                             "oral_literate": feature
                             })

    sentence_info = sentence_results[0]

    id = sentence_results[1]
    sen_no=0
    for entry in sentence_info:
        sen_no+=1
        for i in sentence_info[entry]:
            POS = i[1]

            # counting POS
            if POS not in pos:
                pos[POS] = 1
            else:
                pos[POS] += 1

        res(sentence_info[entry], "LIT", id,sen_no)


r=spacy_tagger(sentence_results)
identify_oral_literal(r,analysis_results)