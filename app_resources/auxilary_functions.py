import json, os, sys
import re,os,shutil,tkinter
from datetime import datetime
from tkinter import filedialog, Tk, messagebox


def author_information():
    '''
    This provides information about the author and the program.
    '''
    text="app_resources/program_text_files/author_information.json"
    with open(text,mode="r",encoding="utf-8") as file:
        data=json.load(file)
        for line in data:
            print(line,data[line])
        input("Press enter to continue")

def program_description():
    text = "app_resources/program_text_files/program_description.txt"
    with open(text,mode="r",encoding="utf-8") as file:
        for line in file:
            print(line)
        input("Press enter to continue")

def file_finder():
    '''
    This initiates a filedialog that is allows the user to dynamically select a file.
    '''

    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    filename = filedialog.askopenfilename()
    root.withdraw()

    return filename

def program_end():
    # Der Benutzer bekommt die Moeglichkeit, seine Antwort nochmal zu bestaetigen.
    while True:
        final_answer=input("⚠️ Wollen Sie das Programm wirklich beenden?(y/n) ⚠️").lower()
        if final_answer == "y":
            print ("Das Programm wird jetzt beendet.")
            # Beenden des Programms
            raise SystemExit
            sys.exit()
        # Ablehnung
        elif final_answer == "n":
            print("Das Programm wird nicht beendet. Sie werden zum Hauptmenue weitergeleitet.")
            input("Druecken Sie die Eingabetaste, um fortzufahren: ")
            break
        # Unbekannte bzw. falsche Antwort
        else:
            print(f"{final_answer} ist keine gueltige Antwort. Entweder 'y' oder 'n' eingeben.")

