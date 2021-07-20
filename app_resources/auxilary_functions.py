import json, os, sys
import re,os,shutil,tkinter
from datetime import datetime
from tkinter import filedialog, Tk, messagebox


def author_information():
    '''
    This provides information about the author and the program.
    '''
    text="app_resources/app_docs/author_information.json"
    with open(text,mode="r",encoding="utf-8") as file:
        data=json.load(file)
        for line in data:
            print(line,data[line])
        input("Press enter to continue")

def program_description():
    text = "app_resources/app_docs/program_description.txt"
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
    raise SystemExit

