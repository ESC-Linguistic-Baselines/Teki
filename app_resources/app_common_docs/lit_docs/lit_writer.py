import json

# Mueller Texts
francais_cultive = open("FCL.txt", mode="r", encoding="utf-8").read().split()
francais_cultive_abs = open("FCL_abs.txt", mode="r", encoding="utf-8").read().split()
francais_ecrit = open("FRE.txt", mode="r", encoding="utf-8").read().split()
francais_technique = open("FL.txt", mode="r", encoding="utf-8").read().split()
francais_technique_suf = open("FL_suf.txt", mode="r", encoding="utf-8").read().split()
francais_technique_pre = open("FL_pre.txt", mode="r", encoding="utf-8").read().split()

# writing to json file
with open ("../lit_french.json", mode="w", encoding="utf-8") as oral_file:

    data={
        "FC":[word for word in francais_cultive ],
        "FC_abs": [word for word in francais_cultive_abs],
        "FRE":[word for word in francais_ecrit],
        "FRT":[word for word in francais_technique],
        "FRT_SUF":[word for word in francais_technique_suf],
        "FRT_PRE":[word for word in francais_technique_pre]
    }
    json.dump(data,oral_file,indent=2)


