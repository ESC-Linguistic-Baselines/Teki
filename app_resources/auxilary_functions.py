#  -*- coding: utf-8 -*-

#########################
# Importing standard python libraries
#########################

import os
import csv
import json
import logging
import re
from tkinter import filedialog, Tk

#########################
# auxiliary functions
#########################
f = 'app_resources/app_content_docs/error.log'

def author_information():
    """
    function description


    input:



    output:
    """

    text = "app_resources/app_content_docs/author_information.json"
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

    text = "app_resources/app_content_docs/program_description.txt"
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
            new_sentence += f"{tok}<END>"
            new_tokens.append(tok)
        else:
            new_sentence += f"{tok} "

    new = new_sentence.split("<END>")
    res = [sen for sen in new if bool(sen) is True]

    return res


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


def write_to_database(feature, sentence, database):
    with open(database, mode="a", encoding="utf-8", newline="") as analysis:
        fnames = "token_text", "token_pos", "token_dep", "token_id", "sen_no", "oral_literate"
        writer = csv.DictWriter(analysis, fieldnames=fnames)

        for element in sentence:
            sen_word = element[0]
            sen_word_pos = element[1]
            sen_word_dep = element[2]
            sen_word_id = element[3]
            sen_word_tag = element[4]

            writer.writerow(
                {"token_text": sen_word,
                 "token_pos": sen_word_pos,
                 "token_dep": sen_word_dep,
                 "token_id": sen_word_tag,
                 "sen_no": sen_word_id,
                 "oral_literate": feature
                 })


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


def dependency_generate():

       doc=os.listdir(os.getcwd()+"\\app_content_docs")
       dev= os.listdir(os.getcwd()+"\\app_dev\\dev_files")
       test=os.listdir(os.getcwd()+"\\app_test\\test_files")
       compressed=os.listdir(os.getcwd()+"\\app_compressed_data")


       files={"docs":doc,
              "dev":dev,
              "test":test,
              "compressed":compressed}

       out=r"C:\Users\chris\Desktop\Bachleorarbeit\app_resource_files.json"
       out_file = open(out, "w+")

       json.dump(files,out_file,indent = 2)

       print("updated")