import json

"""
FA	français argotique
FF	Français familier
FPA	français parlé
FP	Français populaire
FV	Français vulgaire
"""

argot=open("FA.txt", mode="r", encoding="utf-8")
argot_suffix=open("FA_suf.txt", mode="r", encoding="utf-8")
emoticons=open("emoticons.csv",mode="r",encoding="utf-8")
emoticon_symbols=[i.split(",")[0] for i in emoticons]
ebay_att=open("ebay_att.csv",mode="r",encoding="utf-8")
ebay_ann=open("ebay_ann.csv",mode="r",encoding="utf-8")
ebay_bon=open("ebay_bon.csv",mode="r",encoding="utf-8")

francais_vulgaire=open("FV.txt", mode="r", encoding="utf-8")
fpa=open("FPA.txt",mode="r",encoding="utf-8")
francais_familier=open("FF.txt", mode="r", encoding="utf-8")
francais_familier_inst=open("FF_inst.txt", mode="r", encoding="utf-8")


with open ("oral_french.json",mode="w",encoding="utf-8") as oral_file:

    data={
        "ebay_att":[i.split(",")[0] for i in ebay_att],
        "ebay_ann": [i.split(",")[0] for i in ebay_ann],
        "ebay_bon":[i.split(",")[0] for i in ebay_bon],
         "EMO":emoticon_symbols,
         "FA":[i for i in argot.read().split()],
         "FA_suf":[i for i in argot_suffix.read().split()],
         "FV":[i for i in francais_vulgaire.read().split()],
         "FPA":[i for i in fpa.read().split()],
         "FF":[i for i in francais_familier.read().split()],
         "FF_intens":[i for i in francais_familier_inst.read().split()]

    }

    json.dump(data,oral_file,indent=2)

