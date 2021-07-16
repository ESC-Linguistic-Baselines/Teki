import json,os, sys

def program_information():
    '''
    This provides information about the author and the program.
    '''
    text="app_ressources/program_text_files/author_information.json"
    with open(text,mode="r",encoding="utf-8") as file:
        data=json.load(file)
        for line in data:
            print(line,data[line])
        input("Press enter to continue")
