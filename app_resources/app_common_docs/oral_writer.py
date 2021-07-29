import json


def vocab_writer():
    """
    These are typical words that occur with in spoken French in the different registers.
    """

    with open("oral_french.json", mode="w+", encoding="utf-8") as argot_file:

        data={

            "FRE": {
                "PRE": [],
                "SUFF": [],
                 "VOC": []
            }

            }


        json.dump(data, argot_file,indent=2)


vocab_writer()