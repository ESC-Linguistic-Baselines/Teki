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
import bs4

#########################
# Auxiliary Classes
#########################


class DiscourseAnalysis:
    """

    """

    class PosSyntacticalAnalysis:
        """
        This class contains various functions that rely on the syntactical and
        parts of speech tags to analyze the sentences and assign them a feature.

        """

        def __init__(self, sub_sentences):
            self.sub_sentences = sub_sentences

        def sentence_reconstruction(self):
            """

            :return:
            """

            sentence = " ".join([word[0] for word in self.sub_sentences])
            word_count = len(self.sub_sentences)

            return word_count, sentence

        def part_of_speech(self):
            """

            :return:
            """
            pos = [word[1] for word in self.sub_sentences]
            return pos

        def pos_grams(self):
            """

            :return:
            """

            gram_count = dict()

            pos = self.part_of_speech()
            for i in range(len(pos) - 1):
                gram=pos[i], pos[i+1]

                gram_count[gram] = gram_count.get(gram,0)+1

            for i in range(len(pos)):
                gram = pos[i]
                gram_count[gram] = gram_count.get(gram, 0) + 1

            return gram_count

        def feature_assignment(self):
            """

            :return:
            """

            sentence = self.sentence_reconstruction()[1]
            sentence_length = self.sentence_reconstruction()[0]
            pos = self.part_of_speech()
            gram_count = self.pos_grams()

            noun_count = gram_count.get("NOUN",0)+gram_count.get("PROPN",0)

            verb_count = gram_count.get("VERB", 0)

            instance_one = (
                    sentence_length < 8,
                    noun_count > verb_count,
                    "a" == "b"
                    )

            if instance_one.count(True) > instance_one.count(False):
                return "ORAL"

            else:
                return "UNKNOWN"

    class TokenAnalysis:

        def __init__(self, sub_sentences):
            self.sub_sentences = sub_sentences

        def reconstruct(self):
            sentence = " ".join([word[0] for word in self.sub_sentences])
            return sentence,  len(self.sub_sentences)

#########################
# auxiliary functions
#########################


error_log = 'app_resources/app_content_docs/teki_error.log'


def about_program():
    """
    This reads in the readme file and displays it to the user

    :param
        There are no parameters as it has access to the necessary data which

    :return
        :rtype None
    """

    text = r"README.MD"
    with open(text, mode="r", encoding="utf-8") as read_me:
        for line in read_me:
            print(line.strip())
        input("\nPlease press enter to continue...")


def clear_log(error_log):
    """
        This function deletes the error log file by overwriting it with a error log
        file of the same name.

    :param str
        'error_log': The name of the log file to be cleared.

     :return
        :rtype None
    """

    logging.FileHandler(error_log, "w")
    input("The log file will be cleared after restarting the program.\n")


def dependency_generate():
    """
        This function generates the dependencies that that the main script needs to run properly

    :param str
        'error_log': The name of the log file to be cleared.

     :return
        :rtype None
        There is no object, but a file is created that is placed in the main directory
    """
    app_compressed_data = os.listdir(os.getcwd()+"\\app_compressed_data")
    app_dev = os.listdir(os.getcwd()+"\\app_dev\\dev_files")
    app_test = os.listdir(os.getcwd()+"\\app_test\\app_test")
    app_train= os.listdir(os.getcwd()+"\\app_dev_train\\app_train")
    compressed_data = os.listdir(os.getcwd()+"\\app_compressed_data")

    files = {
        "app_compressed_data": app_compressed_data,
        "app_dev": app_dev,
        "app_test": app_test,
        "compressed_data": compressed_data,
        "app_train": app_train,
        }

    out = "teki_resource_list.json"
    out_file = open(out, "w+")
    json.dump(files, out_file, indent=2)

    print("The app resource directory file has been updated.")


def end_program():
    """
        This function ends the main app or brings back to the main menu

    :param
        There are no parameters as it has access to the necessary data which

     :return
        :rtype None
    """

    while True:
        final_answer = input("Do you really want to end the program (y/n) ?: ").lower()
        if final_answer == "y":
            print("The program will now be terminated...")
            raise SystemExit
        # No
        elif final_answer == "n":
            print("The program will not be terminated and you will be brought back to the main menu.")
            input("Press enter to continue...")
            break


def evaluation():

    def hello():
        print("Hello")

    def evaluate_sentence_tokenizer():
        pass

    def evaluate_naive_bayes():
        pass

    def evaluation_spacy_tagger():
        pass

    def evaluation_spacy_tokenizer():
        pass

    def cross_validation():
        pass

    # This is the dynamic menu that the user has access during this function
    output_menu = {"read file contents": hello,
                   "return to menu": lambda: False
                   }

    # Submenu parameters
    menu_name = "Evaluation Menu"
    menu_information = "How would you like to proceed with the file:"
    sub_menu(output_menu, menu_name, menu_information)


def feature_extraction():
    """
        This function is for extracting features based on their tags from the respective corpora.

    :param
        There are no parameters as it has access to the necessary data which

     :return
        :rtype None
        The data is written to the respective files
    """

    document = r"C:\Users\chris\Desktop\Bachleorarbeit\app_resources\app_dev\dev_files\sms_0_29507.xml"
    outfile = "emoticons.csv"
    corpus = "SMS"
    text = ""
    # SMS files
    with open(document, mode="r", encoding="utf-8") as in_file, open(outfile, mode="a+", encoding="utf-8", newline="") as out_file:
        soup = bs4.BeautifulSoup(in_file, "lxml")
        fieldnames = "token", "type", "token_tag"
        csv_writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        tag_results = dict()

        if corpus == "SMS":
            for element in soup.find_all("distinct", type="emoticon"):
                emoticon = element.getText()
                tag_results[emoticon] = tag_results.get(emoticon, 0)+1

            for emo in sorted(tag_results, key=tag_results.get, reverse=False):
                csv_writer.writerow({
                    "token": emo,
                    "type": "emoticon",
                    "token_tag": "sms_0_29507",
                })

        # Ebay Corpus
        else:
            tag = ("bon", "ego", "sty", "stn", "pre", "vst", "emo", "enc", "imp", "att", "acc", "ann", "con", "info", "lex", "ort", "slo", "syn")

            for t in sorted(tag):
                types = {" ".join(element.getText().split()) for element in soup.find_all(t)}
                for element in types:
                    print(bool(types))
                    csv_writer.writerow({
                        "token": element,
                        "type": t,
                        "token_tag": text
                    })


def file_finder():
    """
        This function allows to the user to select a file using the dialog with tkinter.

    :param
        There are no parameters as it has access to the necessary data which

     :return
        :rtype str
        'filename': this returns the path name of the selected file.
    """

    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    filename = filedialog.askopenfilename()
    root.withdraw()

    return filename


def sentence_tokenizer(simple_split_tokens):
    """
        This function takes in a text tokenized by .split() method and reconstructs them into sentences
        using regular expressions

    :param
        :type list
            'simple_split_tokens': The list of tokens of the sentences/text

     :return
        :rtype list
        'filename': this returns the path name of the selected file.
    """

    # regex expression for recognizing sentences
    regex = re.compile(rf'''(?P<sentence_basic>[a-zàâçéèêëîïôûùüÿñæœ]+[.!?])|# single punctutation marks
                            (?P<sentence_punctuatuion>)[*!?.]|
                            (?P<sentencec_period>)[.·]
                            ''', re.VERBOSE)

    new_tokens, sentence = list(), str()

    for tokens in simple_split_tokens:
        match = regex.findall(tokens)

        if match:
            sentence += f"{tokens}<END>"
            new_tokens.append(tokens)
        else:
            sentence += f"{tokens} "

    new_sentence = sentence.split("<END>")

    # Filters out sentences that only consist of white space.
    sentence_results = [sen for sen in new_sentence if bool(sen) is True]

    return sentence_results


def save_sentences(collective_results, file):
    """
    this saves the untagged sentences to a desired text file
    :param
        :type dict
            'collective_results': The results from the sentence tokenization.

        :type str
            'file': the path name of the text where the sentences should be saved.

     :return
        :rtype
            returns the value of the respective function
    """

    with open(file, mode="a+", encoding="utf-8", newline="") as results:
        fieldnames = "sentence", "sentence_id"
        writer = csv.DictWriter(results, fieldnames=fieldnames)

        for res in collective_results:
            sentence = collective_results[res]
            for sen in sentence:
                writer.writerow({"sentence": sen,
                                 "sentence_id": res})


def sub_menu(output_menu, menu_name, menu_information):
    """
    This is a simplified version of the menu  found in the main application

    :param
        :type dict

        'output_menu' the functions that should be executed as desired.

        :type str
            'menu_name:' name of the respective menu

        :type str
            'menu information': information that should be displayed in the sub_menu

     :return
        :rtype
            returns the value of the respective function
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
        logging.exception(f"Sub menu error: {error}")
        return options_func_dict


def write_to_database(feature, sentence, database):
    """
    This writes the tagging results to the desired database

    :param
        :type str

        'feature' the feature of the sentence

        :type str
            'sentence:' the sentence to be written to the file

        :type str
            'database': the path name of the database

     :return
        :rtype
            returns the value of the respective function
    """

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
                 }
            )


if __name__ == "__main__":
    pass