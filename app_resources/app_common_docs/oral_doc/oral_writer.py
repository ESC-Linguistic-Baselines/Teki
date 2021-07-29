import json

def argot():
    """
    writes to the argot files
    """

    with open("argot.json",mode="w", encoding="utf-8") as argot_file:

        data={
            "argot": "flic"
        }

        json.dump(data, argot_file)


argot()