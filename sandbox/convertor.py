def get_text(file):
    data=dict()
    with open(file, mode="r", encoding="utf-8") as text_file,open("cl_2.csv", mode="w", encoding="utf-8") as res:
        for line in enumerate(text_file):
           id = line[1].split()[-1]
           sen=line[1].split()[:-1]

           for word in sen:
               res.write(f"{word},POS,DEP,FUNC,SEN:{line[0]},{id}\n")


    return data

get_text("test_set_3.txt")