#  -*- coding: utf-8 -*-

#########################
# standard libraries
#########################
import csv
import json
import logging
import os
import re
import sys
from tkinter import filedialog, Tk
from shutil import copyfile
#########################
# Pip libraries
#########################

try:
    import bs4
    import pandas as pd
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.model_selection import cross_val_score
except ImportError as error:
    print(error)

#########################
# Database Files
#########################

lit_french_file = "app_core_resources/default_files/lit_french.json"
oral_french_file = "app_core_resources/default_files/oral_french.json"
error_log = 'teki_error.log'

#########################
# Auxiliary Classes
#########################


class DiscourseAnalysis:
    """
     This class has the primary goal of providing functions and methods
     to automatically assign ORAL and LIT tags to the appropriate sentences.
     This is done in one of two ways: Language-dependent and language-independent criteria.
     The language-dependent method is an experimental way of creating a gold file.
     However, due to the lack of necessary training data, it was deemed not viable.
    """

    def __init__(self, collective_spacy_results):
        """
        :param collective_spacy_results:
            :type dict
                The sentences sentence_results from the tagging function.
        """
        self.collective_spacy_results = collective_spacy_results

    @staticmethod
    def read_database(infile):
        """
        This function loads the .csv file into the database.

        :param infile
            :type str
                The file to be read into the system.

        :return json_data
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
        The words that are removed depend on the corpus saved in the app resource.
        Its main implementation is when the system is being evaluated.
        However, this function is not necessarily fully operational and should be used with caution.

        :return redacted_corpus
            :rtype dict
                a redacted version of the corpus
        """

        # Keys from old corpus to be moved to the new corpus
        original_corpus = self.collective_spacy_results
        original_corpus_keys = self.collective_spacy_results.keys()

        # New corpus
        redacted_corpus = {key: list() for (key) in original_corpus_keys}
        elements_to_be_removed = list()

        # regex
        adverbs = re.compile(r"(?<!^)ment")
        ftr_smpl = re.compile(r"(?<!^)rai")
        hypenated_words = re.compile(r"\b\w*\s*[-]\s*\w*\b")

        # Oral and literal elements that will be removed from old corpus
        oral_infile = DiscourseAnalysis.read_database(oral_french_file)
        lit_infile = DiscourseAnalysis.read_database(lit_french_file)

        # Elements from the lit file
        for language_register in lit_infile:
            for word in lit_infile[language_register]:
                elements_to_be_removed.append(word)

        # Elements from the oral file
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

    class LanguageIndependentAnalysis:
        """
        This class contains various functions that rely on the syntactical and
        parts of speech tags to analyze the sentences and assign them a feature.
        """

        def __init__(self, sub_sentences):
            """
            The sentence from a collection of larger sentences
            """
            self.sub_sentences = sub_sentences

        def sentence_reconstruction(self):
            """
            The sentence consists of many elements when it is retrieved by this function.

            sen_id - token - POS - DEP - Sen No -Morphology
            It splits it apart, rebuilds the sentence and extracts the necessary identifiers

            :return token_count
                :rtype int
                    amount of tokens in a sentence.

            :return sentence
                :rtype str
                the reconstructed sentence.

            :return sen_id
                :rtype str
                unique id of the sentence

            :return sen_num
                :rtype int
                sentence number of the analyzed corpus
            """
            sentence = " ".join([word[0] for word in self.sub_sentences])
            sen_id = self.sub_sentences[0][3]
            sen_num = self.sub_sentences[0][4]
            token_count = len(self.sub_sentences)

            return token_count, sentence, sen_id, sen_num

        def part_of_speech(self):
            """
            This retrieves the syntactical and POS information from the sentence.

            :return pos_count
                :rtype dict
                    amount of pos tags in a sentence.

            :return pos
                :rtype list
                the reconstructed sentence.

            :return dep
                :rtype str
                syntatical dependencies in the sentence.

            :return morph
                :rtype list
                sentence number of the analyzed corpus
            """

            pos = [word[1] for word in self.sub_sentences]
            dep = [word[2] for word in self.sub_sentences]
            morph = [word[4] for word in self.sub_sentences]

            pos_count = dict()
            for i in range(len(pos)):
                pos_tag = pos[i]
                pos_count[pos_tag] = pos_count.get(pos_tag, 0) + 1

            return pos_count, pos, dep, morph

        def calculate_scores(self):
            """
            The score for the sentence is calculated for the the respective sentences.
            By analyzing the sentences based on the parameters listed below,
            it is possible to assign either LIT or Oral to a sentence.
            For more information on the parameters, please consult the documentation

            :return total_score
                :rtype dict
                the total scores for LIT and Oral
            """

            # Files
            oral_file = DiscourseAnalysis.read_database(oral_french_file)

            # Score and their respective points
            total_score = {"LIT": {},
                           "ORAL": {}}

            ######################################
            # LIT/ORAL CLASSIFICATION VARIABLES
            ######################################

            # Regex Expressions
            all_caps = re.compile(r"[A-Z\s]+")
            abbrev_vowels = re.compile("[a-zA-Z]{1,5}\.")
            abbrev_no_vowels = re.compile("[^aeiou]{1,5}$")
            multi_char = re.compile(r"(.)+\1", re.IGNORECASE)
            multi_word = re.compile(r"\b(\w+)\s+\1\b", re.IGNORECASE)
            numbers = re.compile(r"^\d+(.\d+)*$")

            # Sentence Information
            sentence = self.sentence_reconstruction()[1]
            sentence_length = len([word for word in sentence])
            sentence_vocab = [word for word in sentence.split()]
            avg_word_length = sum(len(word) for word in sentence_vocab) / len(sentence_vocab)

            # POS Information
            dep_info = self.part_of_speech()[2]
            pos_info = self.part_of_speech()[1]
            morph_info = str(self.part_of_speech()[3])

            ######################################
            # Counting Elements and Ratios 
            ######################################

            # Lexical counts
            word_count = dict()
            for word in sentence_vocab:
                word_count[word] = word_count.get(word, 0) + 1
            word_repeated = (max(word_count.values()))

            pos_count = dict()
            for i in range(len(pos_info)):
                gram = pos_info[i]
                pos_count[gram] = pos_count.get(gram, 0) + 1

            # Regex count
            abrev_count = len(abbrev_vowels.findall(sentence))
            abbrev_no_vowels_count = len(abbrev_no_vowels.findall(sentence))
            all_caps_count = len(all_caps.findall(sentence))
            numbers_info = len(numbers.findall(sentence))
            multi_char_count = len(multi_char.findall(sentence))
            word_word_redup = len(multi_word.findall(sentence))

            # POS/SYN counts
            adj_count = pos_count.get("ADJ", 0)
            dummy_subject_count = dep_info.count("expl:subj")
            emoticons = [emo for emo in oral_file["EMO"] if emo in sentence]
            nominal_subject_count = dep_info.count("nsubj")
            noun_count = pos_count.get("NOUN", 0) + pos_count.get("PROPN", 0)
            present_tense_count = morph_info.count("Pres")
            punct_count = pos_count.get("PUNCT", 0)
            verb_count = pos_count.get("VERB", 0)
            conj_count = pos_count.get("CCONJ", 0)

            # Ratios
            conj_verb_ratio = conj_count > verb_count
            isolated_verb_stems = sentence_length < 4 and verb_count < 1
            low_verb_high_adj_ratio = verb_count < 1 and adj_count > 3
            len_sen_and_len_word_amount_num = sentence_length < 25 and len(word_count) < 5 and numbers_info
            no_verb_short_sen_pro = verb_count == 0 and sentence_length < 10
            verb_sen_len_ratio = verb_count == 0 and sentence_length < 5 and noun_count < 0
            noun_verb_ratio = noun_count > verb_count

            #########################
            # LIT CLASSIFICATION I
            #########################

            # Sentence lenght measured in char.
            if sentence_length > 45:
                total_score["LIT"]["SEN_LEN"] = sentence_length
            elif sentence_length < 45:
                total_score["LIT"]["SEN_LEN"] = 0

            # High average word length
            if avg_word_length > 5:
                total_score["LIT"]["AVG_WORD_LEN"] = avg_word_length
            elif avg_word_length < 5:
                total_score["LIT"]["AVG_WORD_LEN"] = 0

            # Frequency of third person pronouns as dummy subjects
            if dummy_subject_count >= 1:
                total_score["LIT"]["THIRD_PERSON_EXPL"] = dummy_subject_count
            elif dep_info.count("expl:subj") < 1:
                total_score["ORAL"]["THIRD_PERSON_EXPL"] = 0

            # Frequency of nominal subjects e.g. je, moi, me, toi, etc.
            if nominal_subject_count >= 1:
                total_score["LIT"]["NOM_SUBJ"] = nominal_subject_count
            elif nominal_subject_count < 1:
                total_score["LIT"]["NOM_SUBJ"] = 0

            # Frequency of present tense verbs
            if present_tense_count >= 2:
                total_score["LIT"]["PRES_TENSE"] = present_tense_count
            elif present_tense_count < 2:
                total_score["LIT"]["PRES_TENSE"] = 0

            # Presence of abbreviations without vowels
            if abbrev_no_vowels_count:
                total_score["LIT"]["ABBR_NO_VOWEL"] = abbrev_no_vowels_count
            elif not abbrev_no_vowels_count:
                total_score["LIT"]["ABBR_NO_VOWEL"] = 0

            # High number of verbs compared to nouns
            if noun_verb_ratio:
                total_score["LIT"]["NP_VB_RATIO"] = noun_count + verb_count
            elif not noun_verb_ratio:
                total_score["LIT"]["NP_VB_RATIO"] = 0

            # Verb to adjective ratio
            if low_verb_high_adj_ratio:
                total_score["ORAL"]["LOW_VERB_HIGH_ADJ"] = verb_count + adj_count
            elif not low_verb_high_adj_ratio:
                total_score["ORAL"]["LOW_VERB_HIGH_ADJ"] = 0

            # More coordinating conjunctions than verbs
            if conj_verb_ratio:
                total_score["LIT"]["CCONJ_VB_RATIO"] = conj_count + verb_count
            elif conj_verb_ratio:
                total_score["LIT"]["CCONJ_VB_RATIO"] = 0

            # Short sentence, presence of numbers
            if len_sen_and_len_word_amount_num:
                total_score["LIT"]["SHORT_SEN_LENGTH_PRESENCE_OF_NUMBERS"] = 1
            elif len_sen_and_len_word_amount_num == False:
                total_score["LIT"]["SHORT_SEN_LENGTH_PRESENCE_OF_NUMBERS"] = 0

            #########################
            # ORAL CLASSIFICATION I
            #########################
            # Sentence Length (defined by the number of characters, not words, that appear in the sentence)
            if sentence_length < 30:
                total_score["ORAL"]["SEN_LEN"] = sentence_length
            elif sentence_length > 30:
                total_score["ORAL"]["SEN_LEN"] = 0

            # Short word length
            if avg_word_length < 5:
                total_score["ORAL"]["AVG_WORD_LENGTH"] = avg_word_length
            elif avg_word_length > 5:
                total_score["ORAL"]["AVG_WORD_LENGTH"] = 0

            # Short sentences without verbs, high number of pronouns
            if verb_sen_len_ratio:
                total_score["ORAL"]["VERB_SEN_LEN_RATIO"] = verb_sen_len_ratio
            elif not verb_sen_len_ratio:
                total_score["ORAL"]["VERB_SEN_LEN_RATIO"] = 0

            #  Word Reduplication
            if word_repeated > 1:
                total_score["ORAL"]["WORD_REDUPLICATION"] = word_repeated
            elif word_repeated < 1:
                total_score["ORAL"]["WORD_REDUPLICATION"] = 0

            # High use of punctuation for expressive effect
            if punct_count > 5:
                total_score["ORAL"]["HIGH_PUNCTION"] = punct_count
            elif punct_count < 5:
                total_score["ORAL"]["HIGH_PUNCTION"] = 0

            # High use of same character multiple times
            if multi_char_count > 0:
                total_score["ORAL"]["MULTI_CHAR_REDUPLICATION"] = multi_char_count
            elif multi_char_count < 1:
                total_score["ORAL"]["MULTI_CHAR_REDUPLICATION"] = 0

            # Same words back to back
            if word_word_redup:
                total_score["ORAL"]["WORD_WORD_REDUPLICATION"] = word_word_redup
            elif not word_word_redup:
                total_score["ORAL"]["WORD_WORD_REDUPLICATION"] = 0

            # Emphasis via all Caps
            if all_caps_count:
                total_score["ORAL"]["ALL_CAPS"] = all_caps_count
            elif all_caps_count < 1:
                total_score["ORAL"]["ALL_CAPS"] = 0

            # Isolated verb stems or imperatives
            if isolated_verb_stems:
                total_score["ORAL"]["ISOLATED_VERBS"] = sentence_length + verb_count
            elif not isolated_verb_stems:
                total_score["ORAL"]["ISOLATED_VERBS"] = 0

            # Emoticons
            if emoticons:
                total_score["ORAL"]["EMOTICONS"] = len(emoticons)
            elif not emoticons:
                total_score["ORAL"]["EMOTICONS"] = 0

            # Abbreviations and Acronyms
            if abrev_count:
                total_score["LIT"]["ABBR"] = abrev_count
            elif not abrev_count:
                total_score["LIT"]["ABBR"] = 0

            return total_score

        def feature_assignment(self):
            """
            This function takes the information from calculate_score and
            returns the highest score along with its respective feat
            """

            lit = self.calculate_scores()["LIT"]
            lit_score = sum(lit.values())
            lit_classification = {key:lit[key] for key in sorted(lit,key=lit.get,reverse=False) if lit[key] > 0}

            oral = self.calculate_scores()["ORAL"]
            oral_score = sum(oral.values())
            oral_classification = {key:oral[key] for key in sorted(oral,key=oral.get,reverse=False) if oral[key] > 0}

            # Returning the sentence score
            if lit_score > oral_score:
                return "LIT",lit_classification
            elif oral_score > lit_score:
                return "ORAL", oral_classification
            else:
                return "UNK"

    class FrenchBasedAnalysis:
        """
        This class is intended to a separate french dataset in order
        to create a gold file against which the independent test criteria is to be compared.
        However, due to the lack of necessary data and lack of decisive results,
        this function is not intended to be used, unless it has more data.
        """

        def __init__(self, sub_sentences):
            """
            The sentence from a collection of larger sentences
            """
            self.sub_sentences = sub_sentences

        def sentence_reconstruction(self):
            """
            The sentence consists of many elements when it is retrieved by this function.

            sen_id - token - POS - DEP - Sen No -Morphology
            It splits it apart, rebuilds the sentence and extracts the necessary identifiers

            :return token_count
                :rtype int
                    amount of tokens in a sentence.

            :return sentence
                :rtype str
                the reconstructed sentence.

            :return sen_id
                :rtype str
                unique id of the sentence

            :return sen_num
                :rtype int
                sentence number of the analyzed corpus
            """
            sentence = " ".join([word[0] for word in self.sub_sentences])
            sen_id = self.sub_sentences[0][3]
            sen_num = self.sub_sentences[0][4]
            token_count = len(self.sub_sentences)

            return token_count, sentence, sen_id, sen_num

        def part_of_speech(self):
            """
            This retrieves the syntactical and POS information from the sentence.

            :return pos_count
                :rtype dict
                    amount of pos tags in a sentence.

            :return pos
                :rtype list
                the reconstructed sentence.

            :return dep
                :rtype str
                syntatical dependencies in the sentence.

            :return morph
                :rtype list
                sentence number of the analyzed corpus
            """

            pos = [word[1] for word in self.sub_sentences]
            dep = [word[2] for word in self.sub_sentences]
            morph = [word[4] for word in self.sub_sentences]

            pos_count = dict()
            for i in range(len(pos)):
                pos_tag = pos[i]
                pos_count[pos_tag] = pos_count.get(pos_tag, 0) + 1

            return pos_count, pos, dep, morph

        def calculate_scores(self):
            """
            The scores for the respective sentences.
            These are based upon the criteria specified below.
            The score for this respective function is then return.

            :return total_score
                :rtype dict
                the total scores for LIT and Oral
            """

            # Files
            oral_file = DiscourseAnalysis.read_database(oral_french_file)
            lit_file = DiscourseAnalysis.read_database(lit_french_file)

            # Score and their respective points
            total_score = {
                "LIT": {},
                "ORAL": {}
            }

            ######################################
            # LIT/ORAL CLASSIFICATION VARIABLES
            ######################################

            # Regex Expressions
            adverbs = re.compile(r"(?<!^)ment")
            future_simple = re.compile(r"(?<!^)rai")
            hypenated_words = re.compile(r"\b\w*\s*[-]\s*\w*\b")
            ne_negation = re.compile(r"n'|ne")
            particle_negation = re.compile(r"pas|jamais|aucun|rien")

            # Sentence Information
            sentence = self.sentence_reconstruction()[1]

            # Language Registers

            # Lit
            francais_cultive = [word for word in sentence.split() if word in lit_file["FC"]]
            francais_cultive_abbs = [word for word in sentence.split() if word in lit_file["FC_abs"]]
            fl = [word for word in sentence.split() if word in lit_file["FRT"]]
            frt_pre = [word for word in sentence.split() if word in lit_file["FRT_PRE"]]
            frt_suf = [word for word in sentence.split() if word in lit_file["FRT_SUF"]]

            # Oral
            presentatif = len([word for word in sentence.split() if word in oral_file["pres"]])
            francais_argot = len([word for word in sentence.split() if word in oral_file["FA"]])
            francais_parle = len([word for word in sentence.split() if word in oral_file["FPA"]])
            francais_familier = len([word for word in sentence.split() if word in oral_file["FF"]])
            francais_familier_intes = len([word for word in sentence.split() if word in oral_file["FF_intens"]])
            francais_vulgaire = len([word for word in sentence if word in oral_file["FV"]])

            # Lexical information
            hypenated_words_count = hypenated_words.findall(sentence)

            # French Syntactical information
            proper_negation = ne_negation.findall(sentence) and particle_negation.findall(sentence)
            ne = len(ne_negation.findall(sentence))
            particle = len(particle_negation.findall(sentence))

            #########################
            # LIT CLASSIFICATION II
            #########################

            # Francais Cultive
            if francais_cultive:
                total_score["LIT"]["FC"] = 1

            # Francais Cultive Abbreviations
            if francais_cultive_abbs:
                total_score["LIT"]["FC_ABS"] = 1

            # Francais Technique, Francais Scientifique
            if fl:
                total_score["LIT"]["FRT"] = 1

            # Francais Technique Prefix
            if frt_pre:
                total_score["LIT"]["FRT"] = 1

            # Francais Technique Suffix
            if frt_suf:
                total_score["LIT"]["FRT_SUF"] = 1

            # Often used in formal French, even though not exclusively
            if len(adverbs.findall(sentence)) > 2:
                total_score["LIT"]["ADVB"] = 1

            # High use of Future Simple
            if len(future_simple.findall(sentence)) > 2:
                total_score["LIT"]["FUTURE_SIMPLE"] = 1

            # High use of être and impersonal constructs
            if sentence.count("être") > 3:
                total_score["LIT"]["Être"] = 1

            # Impersonal constructs
            if sentence.count("il") > 2:
                total_score["LIT"]["IL"] = 1

            # High use of hyphenated words
            if hypenated_words_count:
                total_score["LIT"]["HYPHENATED"] = 1

            # Negation with ne .... (pas,jamais..etc)
            if proper_negation:
                total_score["LIT"]["PROPER_NEGATION"] = 1

            #########################
            # ORAL CLASSIFICATION II
            #########################

            # Présentatif
            if presentatif:
                total_score["ORAL"]["PRESENTATIF"] = presentatif
            elif presentatif == 0:
                total_score["ORAL"]["PRESENTATIF"] = 0

            # Francais Argot
            if francais_argot:
                total_score["ORAL"]["FRANCAIS_ARGOT"] = francais_argot
            elif francais_argot == 0:
                total_score["ORAL"]["FRANCAIS_ARGOT"] = 0

            # Francais Parle
            if francais_parle:
                total_score["ORAL"]["FRANCAIS_PARLE"] = francais_parle
            elif francais_parle == 0:
                total_score["ORAL"]["FRANCAIS_PARLE"] = 0

            # Francais Familier
            if francais_familier:
                total_score["ORAL"]["FRANCAIS_FAMILIER"] = francais_familier
            elif francais_familier == 0:
                total_score["ORAL"]["FRANCAIS_FAMILIER"] = francais_familier

            # Francais Familier Intensifiers
            if francais_familier_intes:
                total_score["ORAL"]["FRANCAIS_FAMILIER_INTENSIFIERS"] = francais_familier_intes
            elif francais_familier == 0:
                total_score["ORAL"]["FRANCAIS_FAMILIER_INTENSIFIERS"] = 0

            # Francais Vulgaire
            if francais_vulgaire:
                total_score["ORAL"]["FRANCAIS_VULGAIRE"] = francais_vulgaire
            elif francais_vulgaire == 0:
                total_score["ORAL"]["FRANCAIS_VULGAIRE"] = 0

            # Improper Negation
            if ne == False and particle == True:
                total_score["ORAL"]["IMPROPER_NEGATION"] = ne

            return total_score

        def feature_assignment(self):
            """
            This function takes the information from calculate_score and
            returns the highest score along with its respective feat.
            """

            lit = self.calculate_scores()["LIT"]
            lit_score = sum(lit.values())
            lit_classification = {key:lit[key] for key in sorted(lit,key=lit.get,reverse=False) if lit[key] > 0}

            oral = self.calculate_scores()["ORAL"]
            oral_score = sum(oral.values())
            oral_classification = {key:oral[key] for key in sorted(oral,key=oral.get,reverse=False) if oral[key] > 0}

            # Returning the sentence score
            if lit_score > oral_score:
                return "LIT"
            elif oral_score > lit_score:
                return "ORAL"
            else:
                return "UNK"


#########################
# Auxiliary functions
#########################

def about_program():
    """
    This reads in the readme file and displays it to the user.

    :param
        There are no parameters

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
    This function deletes the error log file by overwriting it
     with a error log file of the same name.

    :param error_log
        :type str The name of the log file to be cleared.
    """

    logging.FileHandler(error_log, "w")
    print("The log file will be cleared after restarting the program.\n")
    input("Please press enter to return the main menu....")

def restore_default_database ():
    """
    This restores the default database
    """
    options = "yes", "no"

    while True:
        for number, choice in enumerate(options):
            print(number, choice)
        print("")
        user = input("Are you sure that you would like restore the default database?").lower()
        if user == "0":  # Yes
            input("The database will now be restored. Please press enter to continue...")
            print("Please wait while the database is being restored....")
            destination = "app_core_resources/default_files/default_training.csv"
            source = "app_core_resources/default_files/default_recovery.csv"
            copyfile(source, destination)
            input("The database has been restored.Please press enter to return the main menu...")
        elif user == "1":  # No
                input("The database will not be restored.Please press enter to return the main menu...")
        else:  # Incorrect or invalid answer
            print(f"'{user}' is not a valid response. Please enter a valid response.\n")


def end_program():
    """
    This allows the user to safely exit the program.
    """
    options = "yes", "no"

    while True:
        for number, choice in enumerate(options):
            print(number, choice)
        print("")
        user = input("Are you sure that you would like exit the program?").lower()
        if user == "0":  # Yes
                sys.exit("The program will now be terminated.")
        elif user == "1":  # No
            sys.exit("The program will not be terminated.")
        else:  # Incorrect or invalid answer
            print(f"'{user}' is not a valid response. Please enter a valid response.\n")


def evaluation():
    """
    This function simply contains two sub-functions: evaluate_naive_bayes and cross_validation
    """

    def evaluate_naive_bayes():
        """
        This function allows the user to dynamically select two files: gold file and a system file.
        The gold file is the file that is the one that is created by hand.
        The system file is the one that was generated by the system.
        """

        # Reference files
        input("Please first select the system file and then the gold file. Press enter to continue...")
        system_file, gold_file = file_finder(), file_finder()

        system = open(system_file, mode="r", encoding="utf-8")
        gold = open(gold_file, mode="r", encoding="utf-8")
        csv_gold_reader, csv_system_reader = csv.reader(gold, delimiter=","), csv.reader(system, delimiter=",")

        sentence_features = dict()

        feat_1, feat_2 = "LIT", "ORAL"

        true_positive = 0
        false_positive = 0
        false_negative = 0
        true_negative = 0

        for row in csv_gold_reader:
            sen, feat = row[0], row[1]
            sentence_features[sen] = {"SYS": "", "GOLD": ""}
            sentence_features[sen]["GOLD"] = feat

        for row in csv_system_reader:
            sen, feat = row[0], row[1]
            sentence_features[sen]["SYS"] = feat

        for entry in sentence_features:
            results = sentence_features[entry]
            feats = list(results.values())
            gold_feat = feats[1]
            sys_feat = feats[0]

            if sys_feat == feat_1 and gold_feat == feat_1:
                true_positive += 1

            elif sys_feat == feat_2 and gold_feat == feat_2:
                true_negative += 1

            elif sys_feat == feat_1 and gold_feat == feat_2:
                false_positive += 1

            elif sys_feat == feat_2 and gold_feat == feat_1:
                false_negative += 1

        accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)
        error_rate = true_negative / (true_positive + true_negative + false_positive + false_negative)
        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + true_negative)
        f_score = (2 * precision * recall) / (precision + recall)

        system_metrics = {
            "Accuracy": round(accuracy, 4),
            "Error rate": round(error_rate, 4),
            "Precision": round(precision, 4),
            "Recall": round(recall, 4),
            "F-score": round(f_score, 4),
            }

        for metric in system_metrics:
            print(metric, system_metrics[metric])

    def cross_validation():
        """
        Using k-fold validation with skilearn, pandas and multinomial bayes,
        the data can be cross validated.
        Simply select the appropriate file for the respective directory.
        """
        data = pd.read_csv(file_finder())
        vectorizer = CountVectorizer()
        text = data["text"].values
        counts = vectorizer.fit_transform(text)

        classifier = MultinomialNB()
        classes = data["feat"].values
        classifier.fit(counts, classes)

        scores = cross_val_score(classifier, counts, classes, cv=10)
        for score in scores:
            print(score)

    # This is the dynamic menu that the user has access during this function
    output_menu = {"evaluate naive bayes": evaluate_naive_bayes,
                   "cross validation": cross_validation,
                   "return to menu": lambda: False}

    # Submenu parameters
    menu_name = "Evaluation Menu"
    menu_information = "Which files would you like to evaluate:"
    sub_menu(output_menu, menu_name, menu_information)


def file_finder():
    """
    This function allows to the user to select a file using the dialog with tkinter.

    :return path_name
        :rtype str
            the string of the path_name file.
    """

    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    path_name = filedialog.askopenfilename()
    root.withdraw()

    return path_name


def sentence_tokenizer(simple_split_tokens):
    """
    This function takes in a text tokenized by .split() method and reconstructs them into sentences
    using regular expressions.

    :param simple_split_tokens
        :type list
            The list of tokens of the sentences/text

     :return sentence_results
        :rtype list
        This is a list of all the sentence contained within the corpus
    """

    # regex expression for recognizing sentences
    regex = re.compile(rf'''(?P<sentence_basic>[a-zàâçéèêëîïôûùüÿñæœ]+[.!?-])|# single punctutation marks
                            (?P<sentence_punctuatuion>)[*!?.]| # typical sentence punctation 
                            (?P<sentence_period>)[.·] # different period types 
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

    # Filters out sentences that only consist of white space
    sentence_results = [sen for sen in new_sentence if bool(sen) is True]

    return sentence_results


def write_sentences(collective_results=False, results_file=False, sen_num=False, sen_id=False, feat=False, feat_save=False):
    """
    this saves the untagged sentences to a desired text file
    :param collective_results
        :type dict
            all of the results produced by the spacy tagger.
    :param results_file
        :type str
            this is the path name of the file where the sentences should be written.

    :param sen_num
        :type int
        number of the respective sentence

    :param sen_id
        :type str
            id of the respective sentence

    :param feat
        :type str
        the feature that should be assigned to the sentence.

    :param feat_save
        :type bool
        this is to determine if the feature should be saved.
    """

    with open(results_file, mode="a", encoding="utf-8", newline="") as results:
        if not feat_save:
            fieldnames = "sentence", "sentence_id", "SEN:"
            writer = csv.DictWriter(results, fieldnames=fieldnames)

            for res in collective_results:
                sentence = collective_results[res]
                for number, sen in enumerate(sentence):
                    writer.writerow({
                                    "sentence": sen,
                                     "sentence_id": res,
                                     "SEN:": f"SEN:{number}",
                                     })
        elif feat_save:
            fieldnames = "sen", "sen_num", "sen_id", "sen_feat"
            writer = csv.DictWriter(results, fieldnames=fieldnames)
            sen = collective_results
            writer.writerow({
                            "sen": sen,
                             "sen_num": sen_num,
                             "sen_id": sen_id,
                             "sen_feat": feat
                            })


def sub_menu(output_menu, menu_name, menu_information):
    """
    This is a simplified version of the menu found in the main application.

    :param output_menu
        :type dict
            the functions that should be executed as desired.

    :param menu_name
        :type str
            name of the respective menu

    :param menu information
        :type str
            information that should be displayed in the sub_menu

    :return
        :rtype
            returns the value of the respective function
    """
    invalid_option = f'An error occurred. You can return to {menu_name} by pressing enter...'

    while True:
        banner = menu_name, menu_information
        for word in banner:
            print(word.center(50))

        for number, option in enumerate(output_menu, start=1):
            print(f'{number}: {option}')

        choice_str = input("\nPlease enter the desired menu number:")
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


def write_to_database(feature, corpus_sentence_id, sentence, database):
    """
    This writes the tagging sentence_results to the desired database

    :param feature
        :type str
            the feature of the sentence

    :param sentence
        :type str
            the sentence to be written to the file.

    :param database
        :type str
            the path name of the database
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
                 "token_id": corpus_sentence_id,
                 "sen_no": sen_word_id,
                 "oral_literate": feature
                 }
            )