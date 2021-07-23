import pickle,csv

filename="tags"
infile = open(filename,'rb')
sentence_results = pickle.load(infile)
infile.close()

analysis_results="app_resources/train_files/training_res.csv"
fnames ="token_text","token_pos","token_dep","token_id","oral_literate"

sentence=""
pos={}

analysis_results="app_resources/train_files/training_res.csv"
fnames ="token_text","token_pos","token_dep","token_id","oral_literate"

def res(sen_info,feature,ID):

    with open(analysis_results, mode="a", encoding="utf-8",newline="") as analysis:
        writer = csv.DictWriter(analysis, fieldnames=fnames)

        for entry in sen_info:

            tok_txt=entry[0]
            tok_pos=entry[1]
            tok_dep=entry[2]

            print(tok_txt,ID)

            writer.writerow(
                {"token_text": tok_txt,
                "token_pos": tok_pos,
                "token_dep": tok_dep,
                "token_id": ID,
                "oral_literate": feature
                 })

sentence_info=sentence_results[0]
id=sentence_results[1]
for entry in sentence_info:
    for i in sentence_info[entry]:
        POS=i[1]

        #counting POS
        if POS not in pos:
            pos[POS]=1
        else:
            pos[POS]+=1


    if entry > 1:
        res(sentence_info[entry], "LIT", id)
    if entry < 2:
        res(sentence_info[entry], "ORAL", id)

