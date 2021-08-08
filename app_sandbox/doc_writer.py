import json


def oral ():

    argot=open("../app_program_resources/default_files/mueller_registers/FA.txt", mode="r", encoding="utf-8")
    argot_suffix=open("../app_program_resources/default_files/mueller_registers/FA_suf.txt", mode="r", encoding="utf-8")
    emoticons=open("../app_program_resources/default_files/mueller_registers/emoticons.csv", mode="r", encoding="utf-8")
    emoticon_symbols=[i.split(",")[0] for i in emoticons]

    francais_vulgaire=open("../app_program_resources/default_files/mueller_registers/FV.txt", mode="r", encoding="utf-8")
    fpa=open("../app_program_resources/default_files/mueller_registers/FPA.txt", mode="r", encoding="utf-8")
    francais_familier=open("../app_program_resources/default_files/mueller_registers/FF.txt", mode="r", encoding="utf-8")
    francais_familier_inst=open("../app_program_resources/default_files/mueller_registers/FF_inst.txt", mode="r", encoding="utf-8")
    presentatifs=open("../app_program_resources/default_files/mueller_registers/FA_pres.txt", mode="r", encoding="utf-8").read().split()


    with open ("../user_databases/oral_french.json", mode="w", encoding="utf-8") as oral_file:

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

    francais_cultive = open("../app_program_resources/default_files/mueller_registers/FCL.txt", mode="r", encoding="utf-8").read().split()
    francais_cultive_abs = open("../app_program_resources/default_files/mueller_registers/FCL_abs.txt", mode="r", encoding="utf-8").read().split()
    francais_ecrit = open("../app_program_resources/default_files/mueller_registers/FRE.txt", mode="r", encoding="utf-8").read().split()
    francais_technique = open("../app_program_resources/default_files/mueller_registers/FL.txt", mode="r", encoding="utf-8").read().split()
    francais_technique_suf = open("../app_program_resources/default_files/mueller_registers/FL_suf.txt", mode="r", encoding="utf-8").read().split()
    francais_technique_pre = open("../app_program_resources/default_files/mueller_registers/Fl_pre.txt", mode="r", encoding="utf-8").read().split()

    # writing to json file
    with open("../user_databases/lit_french.json", mode="w", encoding="utf-8") as oral_file:
        data = {
            "FC": [word for word in francais_cultive],
            "FC_abs": [word for word in francais_cultive_abs],
            "FRE": [word for word in francais_ecrit],
            "FRT": [word for word in francais_technique],
            "FRT_SUF": [word for word in francais_technique_suf],
            "FRT_PRE": [word for word in francais_technique_pre]
        }
        json.dump(data, oral_file, indent=2)

