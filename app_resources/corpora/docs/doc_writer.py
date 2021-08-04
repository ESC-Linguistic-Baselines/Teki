import json

"""
FA	français argotique
FF	Français familier
FPA	français parlé
FP	Français populaire
FV	Français vulgaire
présentatifs
"""

def oral ():

    argot=open("fra_oral_doc/FA.txt", mode="r", encoding="utf-8")
    argot_suffix=open("fra_oral_doc/FA_suf.txt", mode="r", encoding="utf-8")
    emoticons=open("fra_oral_doc/emoticons.csv", mode="r", encoding="utf-8")
    emoticon_symbols=[i.split(",")[0] for i in emoticons]

    francais_vulgaire=open("fra_oral_doc/FV.txt", mode="r", encoding="utf-8")
    fpa=open("fra_oral_doc/FPA.txt", mode="r", encoding="utf-8")
    francais_familier=open("fra_oral_doc/FF.txt", mode="r", encoding="utf-8")
    francais_familier_inst=open("fra_oral_doc/FF_inst.txt", mode="r", encoding="utf-8")
    presentatifs=open("fra_oral_doc/presentatifs.txt", mode="r", encoding="utf-8").read().split()


    with open ("../databases/oral_french.json", mode="w", encoding="utf-8") as oral_file:

        data={
             "EMO":emoticon_symbols,
             "FA":[i for i in argot.read().split()],
             "FA_suf":[i for i in argot_suffix.read().split()],
             "FV":[i for i in francais_vulgaire.read().split()],
             "FPA":[i for i in fpa.read().split()],
             "FF":[i for i in francais_familier.read().split()],
             "FF_intens":[i for i in francais_familier_inst.read().split()],
              "pres": [word for word in presentatifs]
             }

        json.dump(data,oral_file,indent=2)


def lit ():
    import json

    francais_cultive = open("fra_lit_docs/FCL.txt", mode="r", encoding="utf-8").read().split()
    francais_cultive_abs = open("fra_lit_docs/FCL_abs.txt", mode="r", encoding="utf-8").read().split()
    francais_ecrit = open("fra_lit_docs/FRE.txt", mode="r", encoding="utf-8").read().split()
    francais_technique = open("fra_lit_docs/FL.txt", mode="r", encoding="utf-8").read().split()
    francais_technique_suf = open("fra_lit_docs/FL_suf.txt", mode="r", encoding="utf-8").read().split()
    francais_technique_pre = open("fra_lit_docs/Fl_pre.txt", mode="r", encoding="utf-8").read().split()

    # writing to json file
    with open("../databases/lit_french.json", mode="w", encoding="utf-8") as oral_file:
        data = {
            "FC": [word for word in francais_cultive],
            "FC_abs": [word for word in francais_cultive_abs],
            "FRE": [word for word in francais_ecrit],
            "FRT": [word for word in francais_technique],
            "FRT_SUF": [word for word in francais_technique_suf],
            "FRT_PRE": [word for word in francais_technique_pre]
        }
        json.dump(data, oral_file, indent=2)

