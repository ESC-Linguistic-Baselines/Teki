import json


def vocab_writer():
    """
    These are typical words that occur with in spoken French in the different registers.
    """

    with open("oral_french.json", mode="w+", encoding="utf-8") as argot_file:

        data={
            "FPA": {
                "PRE": [],
                "SUFF": [],
                "VOC": ["chose","enfant","bouqin","homme","ami","vin","cela","nous","mourir","",
                        "cinéma","apéritif","télévision","","","","","","","","","","","","","","","","","","","","","",],


            "FRE": {
                "PRE": [],
                "SUFF": [],
                "VOC": ["mais","alors","enfin","voyez","mm","ben","ah","bah","puis alors","puis après","mais pourtant",
                        "truc","gosse","livre","type","copain","pinard","ça","on","crever","","","","","","","",""]
            }





            }


        json.dump(data, argot_file,indent=2)


vocab_writer()