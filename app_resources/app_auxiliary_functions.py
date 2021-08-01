#  -*- coding: utf-8 -*-

#########################
# Importing standard python libraries
#########################

import csv
import json
import logging
import re
from tkinter import filedialog, Tk

#########################
# Importing pip libraries
#########################

try:
    import bs4
except ImportError as  error:
    print(error)

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
                The .json file to be read into the system

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

        # Keys from old corpus to be moved to the new corpus
        original_corpus = self.collective_results_tagged
        original_corpus_keys = self.collective_results_tagged.keys()

        # New corpus
        redacted_corpus = {key: list() for (key) in original_corpus_keys}
        elements_to_be_removed = list()

        # regex
        adverbs = re.compile(r"(?<!^)ment")
        ftr_smpl = re.compile(r"(?<!^)rai")
        hypenated_words = re.compile(r"\b\w*\s*[-]\s*\w*\b")

        # Oral and literal elements that will  be removed from old corpus
        oral_infile = DiscourseAnalysis.read_database("app_resources/app_common_docs/lit_french.json")
        lit_infile = DiscourseAnalysis.read_database("app_resources/app_common_docs/oral_french.json")

        # Moving elements from one dictionary to another, minus the redacted elements
        for language_register in lit_infile:
            for word in lit_infile[language_register]:
                elements_to_be_removed.append(word)

        for language_register in oral_infile:
            for word in oral_infile[language_register]:
                elements_to_be_removed.append(word)

        # Creating the new redacted corpus
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

            :return:
            """
            sentence = " ".join([word[0] for word in self.sub_sentences])
            sen_id = self.sub_sentences[0][3]
            sen_num = self.sub_sentences[0][4]
            word_count = len(self.sub_sentences)

            return word_count, sentence, sen_id, sen_num

        def part_of_speech(self):
            """

            """

            pos = [word[1] for word in self.sub_sentences]
            dep = [word[2] for word in self.sub_sentences]
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
            total_score = { "LIT": {}, "ORAL": {} }

            # Lexical and POS information
            sentence = self.sentence_reconstruction()[1]
            sentence_length = len([word for word in sentence])
            pos = self.part_of_speech()[1]
            dep = self.part_of_speech()[2]
            morph = str(self.part_of_speech()[3])
            gram_count = self.part_of_speech()[0]

            # Vocabulary
            vocab = [word for word in sentence.split()]
            words, characters = len(vocab), len([word for word in sentence])
            avg_word_length = round(words / characters * 100)

            # Word count
            word_count = dict()
            for word in vocab:
                word_count[word] = word_count.get(word, 0)+1

            # Regex Expressions for typical features
            multi_char = re.compile(r"(.)+\1", re.IGNORECASE)
            multi_word = re.compile(r"\b(\w+)\s+\1\b", re.IGNORECASE)
            all_caps = re.compile(r"[A-Z\s]+")
            numbers = re.compile(r"^\d+(.\d+)*$")
            abbrev_no_vowels = re.compile("[^aeiou]{1,5}$")
            abbrev_vowels = re.compile("[a-zA-Z]{1,5}\.")

            #########################
            # LIT
            #########################

            # NOUN/PRONOUN/PROPN to VERB Ratio
            np = gram_count.get("NOUN", 0) + gram_count.get("PROPN", 0)
            vb = gram_count.get("VERB", 0)

            # Third person occurs frequently
            if dep.count("expl:subj") > 1:
                total_score["LIT"]["THIRD_PERSON_EXPL"] = 1

            # First person does not occur frequently
            if dep.count("nsubj") < 1:
                total_score["LIT"]["NOM_SUBJ"] = 1

            # The present tense of verbs occurs frequently
            if morph.count("Pres") > 2:
                total_score["LIT"]["PRES_TENSE"] = 1

            # Abbreviations
            if abbrev_no_vowels.findall(sentence):
                total_score["LIT"]["ABBR"] = 1

            # High number of nouns compared to nouns
            if np > vb:
                total_score["LIT"]["NP_VB_RATIO"] = 1

            # Low number of verbs, with high number of adjectives.
            if vb < 1 and pos.count("ADJ") > 3:
                total_score["ORAL"]["NO_VERBS"] = 1

            # More coordinating conjunctions than verbs
            if pos.count("CCONJ") > pos.count("VERB"):
                total_score["LIT"]["CCONJ_VB_RATIO"] = 1

            # Long sentence length
            if sentence_length > 10:
                total_score["LIT"]["LONG_SEN_LENGTH"] = 1

            # High word length with low word length and  high number of sentences
            if sentence_length < 25 and len(word_count) < 5:
                if numbers.findall(sentence):
                    total_score["LIT"]["LONG_WORD_LENGTH"] = 1

            # High average word length
            if avg_word_length > 10:
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

            #  Word Reduplication
            if (max(word_count.values())) > 1:
                total_score["ORAL"]["WORD_REDUPLICATION"] = 1

            # High use of punctuation for effect
            if gram_count.get("PUNCT", 0) > 5:
                total_score["ORAL"]["SYMBOL_REDUPLICATION"] = 1

            # High use of same character multiple times
            if multi_char.findall(sentence):
                total_score["ORAL"]["MULTI_CHAR_REDUPLICATION"] = 1

            # Same words back to back
            if multi_word.findall(sentence):
                total_score["ORAL"]["WORD_WORD_REDUPLICATION"] = 1

            # Emphasis via all Caps
            if all_caps.findall(sentence):
                total_score["ORAL"]["ALL_CAPS"] = 1

            # Isolated verb stems or imperatives
            if sentence_length < 4 and vb < 1:
                total_score["ORAL"]["ISOLATED_VERBS"] = 1

            # High use of using adjectives and constructions at the beginning of the sentence
            if pos.count("ADJ") > 3:
                total_score["ORAL"]["ADJ"] = 1

            # Emoticons
            emoticons = [emo for emo in oral_file["EMO"] if emo in sentence]
            if emoticons:
                total_score["ORAL"]["EMO"] = 1

            if abbrev_vowels.findall(sentence):
                total_score["LIT"]["ABBR"] = 1

            return total_score

        def feature_assignment(self):
            """


            """
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
        """

        """

        def __init__(self, sub_sentences):
            """

            :param sub_sentences:
            """
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

            """

            pos = [word[1] for word in self.sub_sentences]
            dep = [word[2] for word in self.sub_sentences]
            morph = [word[5] for word in self.sub_sentences]

            gram_count = dict()
            for i in range(len(pos)):
                gram = pos[i]
                gram_count[gram] = gram_count.get(gram, 0) + 1

            return gram_count, pos, dep, morph


        def calculate_scores(self):

            """

            """

            # Files for typical words of oral and lit French
            feat_1 = "app_resources/app_common_docs/oral_french.json"
            feat_2 = "app_resources/app_common_docs/lit_french.json"
            oral_file = DiscourseAnalysis.read_database(feat_1)
            lit_file = DiscourseAnalysis.read_database(feat_2)

            # Sentence
            sentence = self.sentence_reconstruction()[1]

            # Regex
            adverbs = re.compile(r"(?<!^)ment")
            ftr_smpl = re.compile(r"(?<!^)rai")
            hypenated_words=re.compile(r"\b\w*\s*[-]\s*\w*\b")
            negation = re.compile(r"n'|ne")
            negation_words =re.compile(r"pas|jamais|aucun|rien")


            # Score and their respective points
            total_score = {
                "LIT": {},
                "ORAL": {}
            }

            #########################
            # LIT
            #########################

            # Francais Cultive
            fcl = [word for word in sentence.split() if word in lit_file["FC"]]
            if fcl:
                total_score["LIT"]["FC"] = 1

            # Francais Cultive Abbreviations
            fcl_abs = [word for word in sentence.split() if word in lit_file["FC_abs"]]
            if fcl_abs:
                total_score["LIT"]["FC_ABS"] = 1

            # Francais Technique, Francais Scientifique
            fl = [word for word in sentence.split() if word in lit_file["FC_abs"]]
            if fl:
                total_score["LIT"]["FRT"] = 1

            # Francais Technique Prefix
            frt_pre =[word for word in sentence.split() if word in lit_file["FRT_PRE"]]
            if frt_pre:
                total_score["LIT"]["FRT"] = 1

            # Francais Technique Suffix
            frt_suf = [word for word in sentence.split() if word in lit_file["FRT_SUF"]]
            if frt_suf:
                total_score["LIT"]["FRT_SUF"] = 1

            # Often used in formal French, even though not exclusively
            if len(adverbs.findall(sentence)) > 2:
                total_score["LIT"]["ADVB"] = 1

            # High use of Future Simple
            if len(ftr_smpl.findall(sentence)) > 2:
                total_score["LIT"]["FUTURE_SIMPLE"] = 1

            # High use of être and impersonal constructs
            if sentence.count("être") > 3:
                total_score["LIT"]["Être"] = 1

            # Impersonal constructs
            if sentence.count("il") > 2:
                total_score["LIT"]["IL"] = 1

            # High use of hyphenated words
            if hypenated_words.findall(sentence):
                total_score["LIT"]["HYPHENATED"] = 1

            # Negation
            if negation.findall(sentence) and negation_words.findall(sentence):
                total_score["LIT"]["PROPER_NEGATION"] = 1

            #########################
            # Oral
            #########################

            """
            ORAL
            •	Swear words
            •	Future compose
            •	Higher user of contractions
            """

            # Presentatifs
            pres = [word for word in sentence.split() if word in oral_file["pres"]]
            if pres:
                total_score["ORAL"]["pres"] = 1

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
            if ff_res:
                total_score["ORAL"]["FF"] = 1

            # Francais Familier Intesifiers
            ff__intens_res = [word for word in sentence.split()if word in oral_file["FF_intens"]]
            if ff__intens_res:
                total_score["ORAL"]["ff__intens_res"] = 1

            # Francais Vulgaire
            fv=oral_file["FV"]
            fv_res=[word for word in sentence if word in fv]
            if fv_res:
                total_score["ORAL"]["FV"] = 1

            # Improper Negation
            if negation.findall(sentence)== False and negation_words.findall(sentence)==True:
                total_score["ORAL"]["IMPROPRER_NEGATION"] = 1


            return total_score

        def feature_assignment(self):
            """

            :return:
            """

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

error_log = 'teki_error.log'
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

    def cross_validation():
        pass

    # This is the dynamic menu that the user has access during this function
    output_menu = {"evaluate naive bayes": evaluate_naive_bayes,
                    "cross validation":cross_validation,
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
            tag = ( "bon", "ego", "sty", "stn", "pre", "vst", "emo", "enc",
                    "imp", "att", "acc", "ann", "con", "info", "lex", "ort", "slo", "syn")

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
    regex = re.compile(rf'''(?P<sentence_basic>[a-zàâçéèêëîïôûùüÿñæœ]+[.!?-])|# single punctutation marks
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


def write_sentences(collective_results, file, sen_num=False, sen_id=False, feat=False, feat_save=False):
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
    feat_save == False
    with open(file, mode="a+", encoding="utf-8", newline="") as results:
        if feat_save != True:
            fieldnames = "sentence", "sentence_id", "SEN:"
            writer = csv.DictWriter(results, fieldnames=fieldnames)

            for res in collective_results:
                sentence = collective_results[res]

                for number, sen in enumerate(sentence):
                    writer.writerow({"sentence": sen,
                                     "sentence_id": res,
                                     "SEN:": f"SEN:{number}",
                                     })

        else:
            fieldnames = "sen", "sen_num", "sen_id","sen_feat"
            writer = csv.DictWriter(results, fieldnames=fieldnames)
            sen=collective_results
            writer.writerow({"sen": sen,
                             "sen_num":sen_num,
                             "sen_id":sen_id,
                             "sen_feat":feat})

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
