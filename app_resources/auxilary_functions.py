#  -*- coding: utf-8 -*-

#########################
# Importing standard python libraries
#########################

import json
import logging
import re
from tkinter import filedialog, Tk

#########################
# auxiliary functions
#########################
f = 'app_resources/app_docs/error.log'
logging.basicConfig(filename=f,
                    level=logging.DEBUG,
                    format="""\n%(levelname)s_TIME: %(asctime)s\nFILE_NAME: %(filename)s\nMODULE: %(module)s
                    \nLINE_NO: %(lineno)d\nERROR_NAME: %(message)s\n"""
                    )


def author_information():
    """
    function description


    input:



    output:
    """

    text = "app_resources/app_docs/author_information.json"
    with open(text, mode="r", encoding="utf-8") as file:
        data = json.load(file)
        for line in data:
            print(line, data[line])

        input("Press enter to continue")


def program_description():
    """
    function description


    input:



    output:
    """

    text = "app_resources/app_docs/program_description.txt"
    with open(text, mode="r", encoding="utf-8") as file:
        for line in file:
            print(line)
        input("\nPress enter to continue")


def sentence_tokenizer(tokens_orth):
    """
    function description


    input:



    output:
    """

    new_tokens = list()

    new_sentence = ""
    regex = re.compile("[a-zàâçéèêëîïôûùüÿñæœ]+[.!?]|[*!?.]|\s[.·]+")

    for tok in tokens_orth:

        if regex.findall(tok):
            new_sentence += f" {tok} <END>"
            new_tokens.append(tok)
        else:
            new_sentence += f" {tok}"

    new = new_sentence.split("<END>")
    res = [sen for sen in new if bool(sen) is True]

    return [res]


def file_finder():
    """
    function description


    input:



    output:
    """

    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    filename = filedialog.askopenfilename()
    root.withdraw()

    return filename


def menu(output_menu, menu_name, menu_information):
    """
    function description


    input:



    output:
    """

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
            except Exception as error:
                logging.exception(error)
                input(invalid_option)

            else:
                if 0 < choice_num <= len(output_menu):
                    func_list = list(output_menu.values())
                    function_number = choice_num - 1
                    options_func_dict = func_list[function_number]
                    break
                else:
                    input(invalid_option)
    try:
        return options_func_dict()

    except Exception as error:
        logging.exception(error)
        return options_func_dict


def program_end():
    """
    function description


    input:



    output:
    """

    while True:
        final_answer = input("Do you really want to end the program?(y/n) ").lower()
        if final_answer == "y":
            print("The program will now be terminated")

            raise SystemExit
        # No
        elif final_answer == "n":
            print("The program will not be terminated and you will be brought back to the main menu")
            input("Press enter to continue:")
            break


def clear_log(f):
    """
    function description


    input:



    output:
    """

    logging.FileHandler(f, "w")
    print("The log file will be cleared after restarting the program.\n")
