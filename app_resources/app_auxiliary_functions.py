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
     This class has the primary goal of providing functions and methods
     to automatically assign ORAL and LIT tags to the appropriate sentences.
     This is done in one of two ways: Language-dependent and Language-independent criteria.

    """

    def __init__(self, collective_results_tagged):
        """
        :param collective_results_tagged:
            :type dict
                The sentences results from the tagging function.
        """
        self.collective_results_tagged = collective_results_tagged

    @staticmethod
    def read_database(infile):
        """
        This function loads the .csv file into the database. It is accessible by all classes and functions
        within its scope.

        :param infile:
            :type str
                The .csv file to be read in.

        :return csv_data:
            :type list
                a list with a nest listed of the respective .csv entries
        """

        with open(infile, mode="r", encoding="utf-8") as file:
            json_data = json.load(file)

        return json_data

    def redacted_corpus(self):
        """
        This function returns a redacted version of the corpus.
        It is redacted as certain words are removed from the corpus.
        The words that are removed depend on the corpus saved in the app resource .
        Its main implementation is when the system is being evaluated.

        :return:
            :rtype dict
                'redacted_corpus': a redacted version of the corpus.
        """

        # Creating the new corpus
        original_corpus = self.collective_results_tagged
        original_corpus_keys = self.collective_results_tagged.keys()
        elements_to_be_removed = list()

        # oral and literal elements
        oral_infile = DiscourseAnalysis.read_database("app_resources/app_common_docs/lit_french.json")
        lit_infile = DiscourseAnalysis.read_database("app_resources/app_common_docs/oral_french.json")

        for language_register in lit_infile:
            for word in lit_infile[language_register]:
                elements_to_be_removed.append(word)

        for language_register in oral_infile:
            for word in oral_infile[language_register]:
                elements_to_be_removed.append(word)

        redacted_corpus = {key: list() for (key) in original_corpus_keys}

        for sent in original_corpus:
            corpus_sentence = original_corpus[sent]
            for number, sentence in enumerate(corpus_sentence):
                word = sentence[0]
                if word not in elements_to_be_removed:
                    redacted_corpus[sent].append(sentence)

        return redacted_corpus

    class PosSyntacticalAnalysis:
        """
        This class contains various functions that rely on the syntactical and
        parts of speech tags to analyze the sentences and assign them a feature.
        """

        def __init__(self, sub_sentences):
            """
            """
            self.sub_sentences = sub_sentences

        def sentence_reconstruction(self):
            """


            """
            sentence = " ".join([word[0] for word in self.sub_sentences])
            word_count = len(self.sub_sentences)

            return word_count, sentence

        def part_of_speech(self):
            """

            """

            dep = [word[2] for word in self.sub_sentences]
            pos = [word[1] for word in self.sub_sentences]
            morph = [word[5] for word in self.sub_sentences]
            gram_count = dict()

            for i in range(len(pos)):
                gram = pos[i]
                gram_count[gram] = gram_count.get(gram, 0) + 1

            return gram_count, pos, dep, morph

        def calculate_scores(self):
            """

            :return:
            """

            feat_1 = "app_resources/app_common_docs/oral_french.json"
            oral_file = DiscourseAnalysis.read_database(feat_1)

            # Score and their respective points
            total_score = {
                "LIT": {},
                "ORAL": {}
                    }

            # Lexical and POS information
            pos = self.part_of_speech()[1]
            dep = self.part_of_speech()[2]
            morph = str(self.part_of_speech()[3])

            gram_count = self.part_of_speech()[0]
            sentence = self.sentence_reconstruction()[1]
            sentence_length = len([word for word in sentence])

            # Vocabulary
            voc = [word for word in sentence.split()]
            words, characters = len(voc), len([word for word in sentence])
            avg_word_length = round(words / characters * 100)
            word_count = dict()

            # Word count
            for word in voc:
                word_count[word] = word_count.get(word, 0)+1

            # Emoticon elements
            emoticons = set(oral_file["EMO"]) & set(voc)

            # Regex Expressions for typical features
            multi_char = re.compile(r"(.)+\1", re.IGNORECASE)
            multi_word = re.compile(r"\b(\w+)\s+\1\b", re.IGNORECASE)
            all_caps = re.compile(r"[A-Z\s]+")
            numbers = re.compile(r"^\d+(.\d+)*$")
            abb = re.compile("\b(?:[A-Z][a-z]*){2,}")

            # NOUN/PRONOUN/PROPN to VERB Ratio
            np = gram_count.get("NOUN", 0) + gram_count.get("PROPN", 0)
            vb = gram_count.get("VERB", 0)

            #########################
            # LIT
            #########################

            # Third person occurs frequently
            if dep.count("expl:subj") > 1:
                total_score["LIT"]["THIRD_PERSON_EXPL"] = 1

            # First person does not occur frequently
            if dep.count("nsubj") < 1:
                total_score["LIT"]["nsubj"] = 1

            # The present tense of verbs occurs frequently
            if morph.count("Pres") > 2:
                total_score["LIT"]["PRES"] = 1

            # High number of abbreviations
            if abb.findall(sentence):
                total_score["LIT"]["ABBR"] = 1

            # Noun to Verb Ratio
            if np > vb:
                total_score["LIT"]["NP_VB_RATIO"] = 1

            # Ratio of subordinating conjunctions (tagged as KOUS or KOUI) to full verbs.
            if pos.count("CCONJ")>pos.count("VERB"):
                total_score["LIT"]["CCONJ_VB_RATIO"] = 1

            # Long sentence length
            if sentence_length > 25:
                total_score["LIT"]["LONG_SEN_LENGTH"] = 1

            # High word length
            if sentence_length < 25 and len(word_count) < 5:
                if numbers.findall(sentence):
                    total_score["LIT"]["LONG_WORD_LENGTH"] = 1

            # High average word length
            if avg_word_length > 15:
                total_score["LIT"]["AVG_WORD_LENGTH"] = 1

            #########################
            # Orality
            #########################

            # Short word length
            if avg_word_length < 10:
                total_score["ORAL"]["SHORT_WORD_LENGTH"] = 1

            # Short sentence length
            if sentence_length < 15:
                total_score["ORAL"]["SHORT_SEN_LENGTH"] = 1
                # Short sentences with interrogative pronouns

            # Short sentences without verbs, high number of pronouns
            if vb == 0 and sentence_length < 5:
                total_score["ORAL"]["HIGH_PRONOUN_COUNT"] = 1

            # Reduplication
            if (max(word_count.values())) > 1:
                total_score["ORAL"]["WORD_REDUPLICATION"] = 1

            # Frequent use of !!!, ???, etc.
            if gram_count.get("PUNCT", 0) > 5:
                total_score["ORAL"]["SYMBOL_REDUPLICATION"] = 1

            # Using the same character multiple times
            if multi_char.findall(sentence):
                total_score["ORAL"]["MULTI_CHAR_REDUPLICATION"] = 1

            # Same words back to back
            if multi_word.findall(sentence):
                total_score["ORAL"]["WORD_WORD_REDUPLICATION"] = 1

            # Emphasis
            if all_caps.findall(sentence):
                total_score["ORAL"]["ALL_CAPS"] = 1

            # Isolated verb stems  or imperatives with question marks/exclamation marks
            if sentence_length < 4 and vb < 1:
                total_score["ORAL"]["ISOLATED_VERBS"] = 1

            # Low number of verbs
            if vb == 0:
                total_score["ORAL"]["NO_VERBS"] = 1

            #if common:total_score["ORAL"]["EMOTICONS"] = len(common)

            # # Low number of function words
            # if function_words:
            #     total_score["ORAL"]["FUNCTION_WORDS"] = 1

            # Proportion of sentences beginning with a coordinating conjunction.
            # if coor_conj:
            #     total_score["ORAL"]["coor_conj"] = 1

            # High use of using adjectives and constructions at the beginning of the sentence
            if pos.count("ADJ") > 3:
                total_score["ORAL"]["CCONJ"] = 1

            # Emoticons
            if emoticons:
                total_score["ORAL"]["EMO"] = 1

            return total_score

        def feature_assignment(self):

            feat_1_score = sum(self.calculate_scores()["LIT"].values())
            feat_2_score = sum(self.calculate_scores()["ORAL"].values())

            # Returning the results
            if feat_1_score > feat_2_score:
                return "LIT"

            elif feat_2_score > feat_1_score:
                return "ORAL"

            else:
                return "UNK"

    class TokenAnalysis:

        def __init__(self, sub_sentences):
            self.sub_sentences = sub_sentences

        def sentence_reconstruction(self):
            sentence = " ".join([word[0] for word in self.sub_sentences])
            return sentence, len(self.sub_sentences)

        def calculate_scores(self):

            """

            a.	French

            LIT
            •	Use of professional terminology
            •	Use of français cultivé
            •	 Qu’est-ce que
            •	Inversion
            •	Old verb forms that are no longer used in spoken French
            o	Future simple
             high number of abb
              high use of impersonal constructions like "il est certain, il est probable"
              high use of "être"
            """
            feat_1 = "app_resources/app_common_docs/oral_french.json"
            oral_file = DiscourseAnalysis.read_database(feat_1)
            feat_2 = "app_resources/app_common_docs/lit_french.json"
            lit_file = DiscourseAnalysis.read_database(feat_2)
            sentence = self.sentence_reconstruction()[0]

            # Score and their respective points
            total_score = {
                "LIT": {},
                "ORAL": {}
            }
            #########################
            # LIT
            #########################
            fcl = [word for word in sentence.split() if word in lit_file["FC"]]
            if fcl:
                total_score["LIT"]["FC"] = 1

            fcl_abs = [word for word in sentence.split() if word in lit_file["FC_abs"]]
            if fcl_abs:
                total_score["LIT"]["FC_ABS"] = 1

            fl = [word for word in sentence.split() if word in lit_file["FC_abs"]]
            if fl:
                total_score["LIT"]["FRT"] = 1

            frt_pre =[word for word in sentence.split() if word in lit_file["FRT_PRE"]]
            if frt_pre:
                total_score["LIT"]["FRT"] = 1

            frt_suf = [word for word in sentence.split() if word in lit_file["FRT_SUF"]]
            if frt_suf:
                total_score["LIT"]["FRT_SUF"] = 1

            #########################
            # Oral
            #########################


            """
            ORAL
            •	 High usage of présentatifs (c’est, ce sont, ça, il y a, voici)
            •	Swear words
            •	Self-corrections
            •	Only use of ? to ask a question
            •	Français vulgaire
            •	Future compose
            •	Simplification of verb forms
            •	Higher user of contractions
            •	Negation particle without pronoun
            high use of punctuation
            high verb use
            """

            # Francais Argot
            arg_res = [word for word in sentence.split() if word in oral_file["FA"]]
            if arg_res:
                total_score["ORAL"]["FA"] = 1

            # Francais Parle
            fpa_res = [word for word in sentence.split() if word in oral_file["FPA"]]
            if fpa_res:
                total_score["ORAL"]["FPA"] = 1

            # Francais Familier
            ff_res=[word for word in sentence.split() if word in oral_file["FF"]]
            if ff_res:total_score["ORAL"]["FF"] = 1

            ff__intens_res = [word for word in sentence.split()if word in oral_file["FF_intens"]]
            if ff__intens_res:
                total_score["ORAL"]["ff__intens_res"] = 1

            # Francais Vulgaire
            fv=oral_file["FV"]
            fv_res=[word for word in sentence if word in fv]
            if fv_res:
                total_score["ORAL"]["FV"] = 1

            ebay_att=oral_file["ebay_att"]
            ebay_att_res=[word for word in sentence.split() if word in ebay_att]

            if ebay_att_res:
                total_score["ORAL"]["ebay_att"] = 1

            ebay_ann = oral_file["ebay_ann"]
            ebay_ann_res = [word for word in sentence.split() if word in ebay_ann]
            if ebay_ann_res:
                total_score["ORAL"]["ebay_ann"] = 1

            ebay_bon = oral_file["ebay_bon"]
            ebay_bon_res = [word for word in sentence.split() if word in ebay_bon]
            if ebay_bon_res:
                total_score["ORAL"]["ebay_bon"] = 1

            return total_score

        def feature_assignment(self):

            feat_1_score = sum(self.calculate_scores()["LIT"].values())
            feat_2_score = sum(self.calculate_scores()["ORAL"].values())

            # Returning the results
            if feat_1_score > feat_2_score:
                return "LIT"

            elif feat_2_score > feat_1_score:
                return "ORAL"

            else:
                return "UNK"

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
    app_compressed_data = os.listdir(os.getcwd() + "\\app_compressed_data")
    app_dev = os.listdir(os.getcwd() + "\\app_dev\\dev_files")
    app_test = os.listdir(os.getcwd() + "\\app_test\\app_test")
    app_train = os.listdir(os.getcwd() + "\\app_dev_train\\app_train")
    compressed_data = os.listdir(os.getcwd() + "\\app_compressed_data")

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
    # Reference files
    gold_file = "app_resources/app_dev/dev_results/sentence_tokenizer/results.csv"
    system_file = "app_resources/app_dev/dev_results/sentence_tokenizer/results.csv"

    gold = open(gold_file, mode="r", encoding="utf-8")
    system = open(system_file, mode="r", encoding="utf-8")
    csv_gold_reader, csv_system_reader = csv.reader(gold, delimiter=","), csv.reader(system, delimiter=",")

    gold_results = dict()
    system_results = dict()

    def evaluate_sentence_tokenizer():

        true_positive = 0
        false_positive = 0
        false_negative = 0
        true_negative = 0

        for row in csv_gold_reader:
            gold_results[row[1]] = gold_results.get(row[1], 0) + 1

        print(gold_results)

    def evaluate_naive_bayes():

        feat_1 = "ORAL"
        feat_2 = "LIT"

        true_positive = 0
        false_positive = 0
        false_negative = 0
        true_negative = 0

        for row in csv_gold_reader:
            key = row[3] + row[4]
            value = row[5]
            gold_results[key] = value

        for row in csv_system_reader:
            key = row[3] + row[4]
            system_results[key] = row[5]

        for i in gold_results:
            gold_res = gold_results[i]
            sys_res = system_results[i]

            if gold_res == feat_1 and sys_res == feat_1:
                true_positive += 1

            elif gold_res != feat_1 and sys_res != feat_1:
                true_negative += 1

            elif gold_res != feat_1 and sys_res == feat_2:
                false_positive += 1

            elif gold_res == feat_1 and sys_res != feat_2:
                false_negative += 1

        results = {"TP": true_positive, "FP": false_positive, "FN": false_negative, "TN": true_negative}

    def evaluation_spacy_tagger():
        pass

    def evaluation_spacy_tokenizer():
        pass

    # This is the dynamic menu that the user has access during this function
    output_menu = {"evaluate sentence sentence_tokenizer": evaluate_sentence_tokenizer,
                   "evaluate naive bayes": evaluate_naive_bayes,
                   "evaluation spacy tagger": evaluation_spacy_tagger,
                   "evaluation spacy sentence_tokenizer": evaluation_spacy_tokenizer,
                   "return to menu": lambda: False
                   }

    # Submenu parameters
    menu_name = "Evaluation Menu"
    menu_information = "Which files would you like to evaluate:"
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
    with open(document, mode="r", encoding="utf-8") as in_file, open(outfile, mode="a+", encoding="utf-8",
                                                                     newline="") as out_file:
        soup = bs4.BeautifulSoup(in_file, "lxml")
        fieldnames = "token", "type", "token_tag"
        csv_writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        tag_results = dict()

        if corpus == "SMS":
            for element in soup.find_all("distinct", type="emoticon"):
                emoticon = element.getText()
                tag_results[emoticon] = tag_results.get(emoticon, 0) + 1

            for emo in sorted(tag_results, key=tag_results.get, reverse=False):
                csv_writer.writerow({
                    "token": emo,
                    "type": "emoticon",
                    "token_tag": "sms_0_29507",
                })

        # Ebay Corpus
        else:
            tag = (
            "bon", "ego", "sty", "stn", "pre", "vst", "emo", "enc", "imp", "att", "acc", "ann", "con", "info", "lex",
            "ort", "slo", "syn")

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
                            (?P<sentence_period>)[.·]
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
        fieldnames = "sentence", "sentence_id", "SEN:"
        writer = csv.DictWriter(results, fieldnames=fieldnames)

        for res in collective_results:
            sentence = collective_results[res]

            for number, sen in enumerate(sentence):
                writer.writerow({"sentence": sen,
                                 "sentence_id": res,
                                 "SEN:": f"SEN:{number}",
                                 })


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

    with open(database, mode="a+", encoding="utf-8", newline="") as analysis:
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
