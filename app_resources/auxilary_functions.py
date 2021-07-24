import json, os, sys
import re,os,shutil,tkinter
from datetime import datetime
from tkinter import filedialog, Tk, messagebox
import traceback

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
        input("\nPress enter to continue")

def sentence_tokenizer(tokens_orth,abbrev):
    new_tokens = list()
    sentences = list()
    new_sentence = ""
    regex = re.compile("[a-zàâçéèêëîïôûùüÿñæœ]+[.!?]|[*!?.]|\s[.·]+")

    for tok in tokens_orth:

        if regex.findall(tok):
            new_sentence += f" {tok} <END>"
            new_tokens.append(tok)
        else:
            new_sentence += f" {tok}"

    new = new_sentence.split("<END>")
    res = [sen for sen in new if bool(sen) == True]

    return [res]

def file_finder():
    '''
    This initiates a filedialog that is allows the user to dynamically select a file.
    The user will be prompted to select a file until a file has been choosen.
    The user also aslo
    '''

    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    filename = filedialog.askopenfilename()
    root.withdraw()

    return filename

def menu(output_menu, menu_name, menu_information):
    '''
    This is a variation of the main menu that is found in the main app.
    '''

    invalid_option = f'An error occurred. You can return to {menu_name} by pressing enter.'

    while True:
        print(f'\n\t\t~ {menu_name} ~\n')
        print(f'{menu_information}\n')

        for num, elem in enumerate(output_menu, start=1):
            print(f'{num}: {elem}')

        choice_str = input("\nPlease enter the menu number:")

        menu_option = output_menu.get(choice_str.title())

        if menu_option:
            break
        else:
            try:
                choice_num = int(choice_str)
            except:
                input(invalid_option)
                with open("app_resources/app_docs/error.log", mode="a") as log:
                    log.write(traceback.format_exc())
            else:
                if 0 < choice_num and choice_num <= len(output_menu):
                    func_list = list(output_menu.values())
                    function_number = choice_num - 1
                    options_func_dict = func_list[function_number]
                    break
                else:
                    input(invalid_option)
    try:
        return options_func_dict()

    except:
        with open("app_resources/app_docs/error.log", mode="a") as log:
            log.write(traceback.format_exc())
        return options_func_dict

def program_end():
    '''
    This function terminates the main menu and the main program.
    '''

    while True:
        final_answer=input("⚠️ Do you really want to end the program?(y/n) ⚠️").lower()
        if final_answer == "y":
            print ("The program will now be terminated")

            raise SystemExit
        #No
        elif final_answer == "n":
            print("The program will not be terminated and you will be brought back to the main menu")
            input("Press enter to continue:")
            break

        #Unknown, incorrect answer
        else:
            print(f"{final_answer} is not a vaild answer. Enter either 'y' or 'n'.")
