#  -*- coding: utf-8 -*-

#########################
# Importing standard python libraries
#########################
import csv
import logging
import os
import pickle
import sys
import timeit
from datetime import datetime

if __name__ == "__main__":
    # Starting the program will take a bit of time due to the amount of libraries being imported.
    # This is to measure the loading time of the program. It should take around 3 - 8 seconds to load everything.

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    start = timeit.default_timer()
    print(f"The current time is {current_time}.")
    print("Please wait while libraries and files are being imported...")
    print("This could take a while depending on your system resources.\n")

#########################
#  Program description
#########################
"""
This program's function is to access the literacy and orality 
of French chat data by using markers that can identify said features.
"""


#########################
# Program continuation function
#########################


def continue_program(*args):
    """
    This function acts as a prompt for the user.
    They can choose to either continue with the program or exit.

    :param '*args'
        :type str
            It can take as many string arguments as necessary. These are displayed as the message prompts

    :return
       :rtype None
    """

    # Displays the error prompt messages.
    for message in args:
        print(message)
    print("")

    while True:
        # The while-loop remains in place until the user provides an appropriate response.
        user = input("Would you still like to continue with the program (y/n) ?: ").lower()

        # Yes
        if user == "y":
            user = input("Are you sure? Program stability cannot be guaranteed (y/n)?: ").lower()

            #  Yes
            if user == "y":
                """
                This will cause the loop to be broken. 
                This will therefore also allow the main program to continue running. 
                However, stability cannot be guaranteed. 
                """
                break
            else:
                sys.exit("The program will now be terminated.")

        # No answer
        elif user == "n":
            sys.exit("The program will not be terminated.")

        # Incorrect or invalid answer
        else:
            print(f"'{user}' is not a valid response. Please enter a valid response.\n")

#########################
# Importing pip libraries
#########################

library_error=list()
try:
   import bs4
   import spacy
   import lxml

   from spacy.lang.fr import French
   from spacy.tokenizer import Tokenizer
   from bs4 import BeautifulSoup

except ImportError as error:
    library_error.append(error)
    logging.exception(f" Module import': is due to '{error})'")

#########################
# Importing custom files and modules
#########################
"""
A program-wide check is performed for the necessary files . 
The program can still be started if any of the necessary files are missing, 
but the program stability will be greatly compromised. 
"""

core_file_missing = list()
if os.path.exists("app_resources"):
    # Necessary file names stored as requirement_resources.txt
    with open ("requirement_resources.txt", mode="r", encoding="utf-8") as resource:
        for line in resource:
             if os.path.exists(line.strip()) == False:
                 core_file_missing.append(line)

    try:
        # importing custom modules from the auxiliary functions file
        from app_resources.app_auxiliary_functions import (
            about_program,
            clear_log,
            DiscourseAnalysis,
            end_program,
            evaluation,
            file_finder,
            sub_menu,
            write_sentences,
            sentence_tokenizer,
            write_to_database)

    except Exception as error:
        print("It seems that not all custom modules could be imported. Please check the log file.")
        logging.exception(f" custom module import': is due to '{error})'")

else:
    message = "The app resource directory is either missing or has been renamed."
    continue_program(message)

#########################
# Main Program Functions
#########################


def get_text(document):
    """
    This functions reads in a text file. This file is either the app_common_default_docs file
    or it is the file that has been dynamically specified by the user.
    The check is done by looking for the .xml ending in the program file.

    :param
       :type str 'document':
            a path to the desired document file.

    :return
        :rtype <class 'bs4.BeautifulSoup>
        'soup': if the user chooses an xml-file, then a beautiful object is returned.

        :rtype str
            'csv_data': if the user chooses csv file

        :rtype str
            'text': if the user chooses anything else other than .xml file or .csv file

    Returns
    """
    name, extension = os.path.splitext(document)

    with open(document, mode="r", encoding="utf-8") as file:

        if extension == ".xml":
            soup = bs4.BeautifulSoup(file, "lxml")
            return soup

        elif extension == ".csv":
            csv_reader = csv.reader(file, delimiter=",")
            csv_data = [row for row in csv_reader]
            return csv_data

        else:
            text=""
            for line in file:
                word = line.rstrip().split()
                for w in word:
                    text+=f"{w} "
            return text

def get_database():
    """
    This function retrieves the designated database file that is saved in an .csv file
    The database should have the following format for it to be properly processed.
    Word, POS, Dep, Sentence number, Corpus Tag, Feature, Tag
    corrélés,VERB,acl:relcl,SEN:2,cmr-wiki-c001-a1,LIT

    :param
        There are no parameters.

    :return
        :rtype str
            'database' is the path name of the database.
    """

    # It retrieves the file by invoking the function file_finder from app_auxiliary_functions.py
    database = file_finder()

    return database


def analyze_content(text):
    """
    This function has the main function of returning the results of the sub-functions.
    it is therefore more of a container of sorts.

    :param
        :type str
            'text' is the the data from the get_text function.

    :return
        :rtype dict
        the collective results of the user

    """

    def tag_save(sentence_count, collective_results):
        """
        This function gives the user the option of either tagging their results or
        saving them in a designated file.

        :param
            :type int
             'sentence_count': the number of sentences in the selection

        :param
            :type dict
            'collective_results': all of the sentences with their respective id.s

        :return:
            if user tags
            :rtype None
            else
            :rtype
                returns the collective results back so that they can be tagged.
        """
        while True:
            options= "tag sentences","save sentences","return"

            for number,choice in enumerate(options,start=1):
                print(number,choice)
            print("")

            user = input(f"The text has been parsed into {sentence_count} sentences. How would you like to proceed? ")
            if user == "1":
                input("The results will now be tagged. Please press enter to continue with the tagging process...")
                return collective_results

            elif user == "2":
                print("Please select the directory:")
                path = file_finder()
                write_sentences(collective_results, path)
                input(f"The results have been saved in {path}. Press enter to return to the main menu.")
                return False

            elif user == "3":
                input("The sentences will neither be saved nor tagged. Please press enter to return to the main menu...")
                break

            else:
                print(f"{user} is not a valid option. Please enter a valid option.")

    def read_contents():

        """
        This function only reads in the text data. After the text data has been read,
        the user will be forwarded to the main menu.

        :param
           There are no parameters as it has access to the necessary data which are within its scope

        :return
            :rtype None
        """

        for row in text:
            print(row)
        input("\nPlease press enter to continue to the main menu.")

    def xml_analysis():
        """
        This function automatically extracts textual information from
        the .xml files that are located in the app resource directory.py.
        It is theoretically possible for it to work with any file that has
        a corresponding .xml format.

        However, since the function has been written specifically with those files in mind,
        the respective lines would have to be changed in order for it to accommodate other .xml files


        :param:
            There are no parameters as it has access to the necessary data which
            is within the scope of this function.

        :return:
            if user tags
            :rtype collective results

            else
            :rtype
                None
                the user is brought back to the main menu
        """

        # Renamed as soup so as to be consistent with beautiful soup terminology
        soup = text

        while True:

            while True:
                """
                The respective directories are listed from which the user may select.
                The user must input a valid option that is in the range
                of the corpus length. Once done, the loop will be broken and the user can progress.
                """
                corpora = "eBay", "SMS", "Wikiconflict"
                for num, corpus in enumerate(corpora, start=1):
                    print(num, corpus)

                corpus_choice = input("\nFrom which corpus are you extracting the information?")

                if corpus_choice.isdigit():
                    check_choice = int(corpus_choice)

                    if check_choice in list(range(1, 4)):
                        corpus_choice = int(corpus_choice)
                        break
                    else:
                        print(f"{corpus_choice} is not a valid option. Please select a valid option.")

            # xml id tags are only relevant for the .xml corpora as  .txt do not have xml tags.
            xml_tag_id = list()

            if corpus_choice == 1:  # eBay listing
                for tag in soup.select("div[id]"):
                    xml_tag_id.append(tag["id"])

            elif corpus_choice == 2 or 3:  # SMS, Wikiconflict
                for tag in soup.select("post"):
                    xml_tag_id.append(tag["xml:id"])
            else:
                print("You did not enter a valid corpus number.\n")

            while True:
                print(f"There are {len(xml_tag_id)} tags. Please enter a selection range from 0 - {len(xml_tag_id)}.")
                print("A range should be specified as follows with a single space between both numbers: start stop.\n")
                corpus_range_choice = input("Please enter a valid selection: ")
                print("")

                try:
                    """
                    If the user has entered a valid selection, 
                    then this range i.e. selection is extracted from the desired corpus. 
                    The sentences are then parsed using the sentence_tokenizer located in the auxiliary_functions.
                    It returns the parsed sentences and they are saved together with their respective id in a dictionary.
                    """

                    corpus_range_choice = corpus_range_choice.split()
                    start, stop = int(corpus_range_choice[0]), int(corpus_range_choice[1])
                    collective_results = dict()
                    sentence_count = 0

                    for i in range(start, stop):

                        # Extracting the selection and tokenizing it.
                        if corpus_choice == 1:
                            corpus_text = soup.find("div", id=xml_tag_id[i]).getText().strip().split()
                            results = sentence_tokenizer(corpus_text)
                            collective_results[xml_tag_id[i]] = results

                        elif corpus_choice == 2 or 3:
                            corpus_text = soup.find("post", {"xml:id": xml_tag_id[i]}).getText().strip().split()
                            results = sentence_tokenizer(corpus_text)
                            collective_results[xml_tag_id[i]] = results

                    #  Calculating the total amount of sentences
                    for sentence in collective_results:
                        sentence_count += len(collective_results[sentence])
                    return tag_save(sentence_count, collective_results)

                except Exception as error:
                    logging.exception(f"xml_analysis error due to: {error}")
                    print(f"{corpus_range_choice} is not a valid selection. Please enter a valid choice.\n")

    def txt_analysis():

        """
        This function tokenizes any text that is saved in .txt-style document.

        :param:
            There are no parameters as it has access to the necessary data which
            is within the scope of this function.

        :return:
            if user tags
            :rtype collective results

            else
            :rtype
                None
                the user is brought back to the main menu
        """

        """
        Creates simplified tokens for the sake of creating sentence-level tokens.
        The real tokens will be done with spacy. 
        """

        tokens = text.split()
        user = input("Please enter a unique identifier ONLY using number of characters from (a-z, A-Z, 0-9) for this text: ")
        results = sentence_tokenizer(tokens)
        collective_results = dict()

        for num, sen in enumerate(results):
            path_id = f"{user}_{num}"
            collective_results[path_id] = [sen]

        return tag_save(len(results), collective_results)

    # This is the dynamic menu that the user has access during this function
    output_menu = {"read file contents": read_contents,
                   "analyze .XML data": xml_analysis,
                   "analyze .TXT data": txt_analysis,
                   "return to  main menu": lambda: False
                   }

    # Submenu parameters
    menu_name = "Analysis Menu"
    menu_information = "How would you like to proceed with the file:"
    menu = sub_menu(output_menu, menu_name, menu_information)

    return menu


def spacy_tagger(corpus_content):
    """
    This function works with the spacy tagger. It has the goal of parsing the sentences into their respective tokens.

    The relevant elements from spacy are:
    Word
    Part-of-speech
    Dependencies

    :parameter:
       :type dict
        'corpus_content': the results from the extract functions are processed here

    :return
        :type dict
        'collective_results_tagged': the tagged and tokenized results of the corpus content.
    """
    print("The individual sentences are now being tagged.")
    print("The duration will depend on your system resources and the number of sentences being tagged.")
    print("Please wait...\n")

    nlp = spacy.load("fr_core_news_sm")
    collective_results_tagged = dict()

    for sent in corpus_content:
        corpus_sentence = corpus_content[sent]
        new_sentence = list()

        for number, sentence in enumerate(corpus_sentence):
            # Creates a doc object with all lexical information using spacy
            doc = nlp(sentence)
            for token in doc:
            # the results of the Spacy analysis
                new_sentence.append((token.text, token.pos_, token.dep_, sent, f"SEN:{number}", str(token.morph),token.lemma_))
            #  generates a unique identifier for the sentences
            new_key = f"{sent}-sen_no-{number}"
            collective_results_tagged[new_key] = new_sentence
            # overwriting the old with a new list so that the new results can be saved.
            new_sentence = list()
    input("The sentences have been successfully tagged. Please press enter to continue...")
    return collective_results_tagged


def sentence_identification(collective_results_tagged, database, system_evaluation):
    """
    This function takes the sentence and its lexical information to determine the most appropriate feature to be assigned to said sentence.
    If the system is being run in evaluation mode, then a respective file is created i.e. a gold standard, against which the system results can be compared.

    :parameter
        :type dict
            'collective_results_tagged': The results that have been tagged. The should be saved somewhere in the
            the programs directory.py

        :type str
        ' database': the path file to the respective directory.py

    :return
        :rtype None
            This function has no return, but saves the result to the specified database.
    """

    current_time = datetime.now().strftime("%d_%m_%Y_%M_%S_")
    system_file = f"app_resources/app_common_results/system_{current_time}.csv"
    gold_file = f"app_resources/app_common_results/gold_{current_time}.csv"

    if system_evaluation:
        redacted_corpus = DiscourseAnalysis(collective_results_tagged).redacted_corpus()
        input("The system is being evaluated. Please press enter to start the evaluation...")
        # System results
        for corpus_sentence_id in redacted_corpus:
            sub_sentences = collective_results_tagged[corpus_sentence_id]
            sentence_info = DiscourseAnalysis.LanguageIndependentAnalysis(sub_sentences)
            feat = sentence_info.feature_assignment()
            sentence = sentence_info.sentence_reconstruction()[1]
            sen_id = sentence_info.sentence_reconstruction()[2]
            sen_num = sentence_info.sentence_reconstruction()[3]
            write_sentences(sentence, system_file, sen_num, sen_id, feat, True)

        # Gold results
        for corpus_sentence_id in collective_results_tagged:
            sub_sentences = collective_results_tagged[corpus_sentence_id]
            sentence_info = DiscourseAnalysis.FrenchBasedAnalysis(sub_sentences)
            feat = sentence_info.feature_assignment()
            sentence = sentence_info.sentence_reconstruction()[1]
            sen_id = sentence_info.sentence_reconstruction()[2]
            sen_num = sentence_info.sentence_reconstruction()[3]
            write_sentences(sentence, gold_file, sen_num,sen_id, feat, True)

        input("The evaluation was completed without any errors. Please press enter to continue the main menu...")

    else:
        # This option is activated when the system is not being evaluated.
        while True:
            options = "automatically", "manually"
            for number, choice in enumerate (options):
                print(number, choice)
            print("")

            user = input ("Would you like to have the features assigned automatically or manually? ")

            if user == "0":
                # Automatic Assignment
                for corpus_sentence_id in collective_results_tagged:
                    sub_sentences = collective_results_tagged[corpus_sentence_id]
                    sentence_info = DiscourseAnalysis.LanguageIndependentAnalysis(sub_sentences)
                    feat = sentence_info.feature_assignment()
                    sentence = sentence_info.sentence_reconstruction()[1]
                    sen_id = sentence_info.sentence_reconstruction()[2]
                    sen_num = sentence_info.sentence_reconstruction()[3]
                    write_to_database(feat, sub_sentences, database)
                    write_sentences(sentence,
                                    f"app_resources/default_docs/default_result_sentence_{current_time}.csv", sen_num, sen_id, feat, True)
                print(f"\nAll of the sentences have been automatically assigned the most appropriate feature.")
                input("Please press enter to continue to the main... ")
                break

            elif user == "1":
                # Manually assignment of features
                options = "LIT", "ORAL"
                for number, choice in enumerate(options):
                    print(number, choice)
                print("")

                user = input("Please enter the number of the desired feature")

                if user == "0":
                    feat="LIT"
                elif user == "1":
                    feat = "ORAL"

                for corpus_sentence_id in collective_results_tagged:
                    sub_sentences = collective_results_tagged[corpus_sentence_id]
                    sentence_info = DiscourseAnalysis.LanguageIndependentAnalysis(sub_sentences)
                    write_to_database(feat, sub_sentences, database)
                    sentence = sentence_info.sentence_reconstruction()[1]
                    sen_id = sentence_info.sentence_reconstruction()[2]
                    sen_num =  sentence_info.sentence_reconstruction()[3]
                    write_sentences(sentence,
                                    f"app_resources/default_docs/default_result_sentence_{current_time}.csv", sen_num, sen_id, feat, True)

                print(f"\nAll of the sentences have been assigned the feature {feat}.")
                input("Please press enter to continue to the main... ")
                break

            else:
                print(f"{user} is not a valid option.")


def get_feat_count(file):
    """
    This function retrieves the count of the features in the database.

    :param
        :type str
            'file'': the path file of the database

    :return
        :rtype dict
            'prior_prob': the frequency of said features.

        :rtype list
            'training_data': the data from the csv file saved in a list.
    """

    with open(file, mode="r", encoding="utf-8") as training_data:
        csv_reader = csv.reader(training_data, delimiter=",")
        training_data = [row for row in csv_reader]

        # Features to be found in the text
        feat_count = {"LIT": 0, "ORAL": 0}
        sentence_lex = {(row[3], row[4], row[5])
                        for row in training_data}

        for sentence in sentence_lex:
            feat = sentence[2]
            feat_count[feat] = feat_count.get(feat,0) + 1

        print("The structure of the database is as follows:")
        print("LIT:",feat_count.get("LIT",0))
        print("ORAL:",feat_count.get("ORAL",0))
        print("")

        return feat_count, training_data


def get_probs(freq_training_data):
    """
    This function calculates the probability of the features.

        P(s) = the probability of a sentence
        c = the count of a word
        s = meaning of word
        w = the word

    a-prior probability:
        Determine the proportions (= probabilities) of the different possible meanings s of a word w
        P(s) = C(s,w)/C(w)

    individual feature probabilities:
        count how often each classification (oral) feature occurs with the different possible features
        p(Cj|S) = C(Cj,s)/C(s)

    for OOV (out of vocabulary) words, the following smoothing formula is used.
    Smoothing the data using the method from Ng (1997)
        p(Cj|Sn) = P(Sn)/N = C(Sn)/N**2 for (Cj,Sn) = 0
        N is the training data.

    :param
        :type tuple
            'csv_results': is a tuple which contains the frequency of the feature and the file_data

    :return
        :rtype dict
            'freq': the frequency of said features.

        :rtype dict
            'prob_results': the probability of the each word having a certain feature.
    """

    prior_prob, training_data = freq_training_data[0], freq_training_data[1]

    prob_results = dict()
    freq_feat_1, freq_feat_2 = dict(), dict()
    tokens_feat_1, tokens_feat_2 = list(), list()

    vocabulary = set()
    n_training_data = sum(prior_prob.values())

    for element in training_data:
        """
         Smoothing the data using the method from Ng (1997)
         p(Cj|Sn) = P(Sn)/N = C(Sn)/N**2 for (Cj,Sn) = 0
         N is the training data
         """

        word, feat = element[0], element[5]
        vocabulary.add(word)

        if feat == "LIT":
            tokens_feat_1.append((word, feat))
            freq_feat_1[word] = freq_feat_1.get(word, 0) + 1

        elif feat == "ORAL":
            tokens_feat_2.append((word, feat))
            freq_feat_2[word] = freq_feat_2.get(word, 0) + 1

        # Calculating the MLE probability of Feat 1
        if freq_feat_1.get(word, 0) > 0:
            feat_1_prob = freq_feat_1.get(word) / prior_prob["LIT"]
        else:
            # Ng Smoothing
            feat_1_prob = prior_prob["LIT"] / n_training_data ** 2

        # Calculating the MLE probability of Feat 2
        if freq_feat_2.get(word, 0) > 0:
            feat_2_prob = freq_feat_2.get(word) / prior_prob["ORAL"]
        else:
            # Ng smooth
            feat_2_prob = prior_prob["ORAL"] / n_training_data ** 2

        prob_results[word] = feat_1_prob, feat_2_prob

    return prior_prob, prob_results

def document_classificaiton(probabilities):
    """
    This function calculates the probability of the sentence.
    Using comparative product values, the biggest product with respect to feature 1 and feature 2 is chosen.
    The bigger value indicates that the sentence most likely belongs to this value as opposed to the other value

    This is based on bayes rule which is P(s|c) = P(c|s)·P(s)/P(c)
        * a-posterior = P(s|c)
        * feature = P(c|s)
        * a priori = P(s)

    The value is calculated using a variation of bayes called 'naive bayes'
       A naive bayes assumes that all individual features cj of context c used in classification (oral) are independent of each other.
       This contextual independence is therefore the nativity.

        s′ = argmaxs∈S  ( P(c|s) · P(s)/ P(c) ) = argmaxs∈S P(c|s) · P(s)

        The only relevant part is the maximum argument which is then:
            argmaxs∈S P(c|s) · P(s)
            P(c|s)= πCj∈cP(Cj|s)

        Result:
            The product of the probabilities (word count/feature count) are multiplied together and then with the a priori probability.
             if a value is not available, then it is smoothed according to Ng(1997)

            This product is the final value of the naive bayes.

    :param
        :type str
            the sentence to identified.

        :type tuple
            'probabilities': is a tuple which contains the frequency of the feature and the probability results

    :return
        :rtype dict
            'freq': the frequency of said features.

        :rtype dict
            'prob_results': the probability of the each word having a certain feature.
    """

    def calculate (text):
        """

        :param text:
        :return:
        """

        prior_prob, prob_results = probabilities[1], probabilities[0]
        feat_1_prob, feat_2_prob = prob_results["LIT"], prob_results["ORAL"]
        feat_1_total_prob = feat_1_prob / (feat_1_prob + feat_2_prob)
        feat_2_total_prob = feat_2_prob / (feat_1_prob + feat_2_prob)

        n_training_data = sum(prob_results.values()) ** 2
        feature_1_smooth = feat_1_prob / n_training_data
        feature_2_smooth = feat_2_prob / n_training_data

        word_feat_prob = dict()

        for word in text:
            if bool(prior_prob.get(word)):
                word_feat_prob[word] = prior_prob.get(word)
            else:
                word_feat_prob[word] = feature_1_smooth, feature_2_smooth

        for word in word_feat_prob:
            feat_1_total_prob *= word_feat_prob[word][0]
            feat_2_total_prob *= word_feat_prob[word][1]

        print(feat_2_total_prob, feat_1_total_prob)
        if feat_1_total_prob > feat_2_total_prob:
            print(f" The text '{text[:7]}...'is LIT.")
            return "LIT"
        elif feat_2_total_prob > feat_1_total_prob:
            print(f" The text '{text[:7]}...' is ORAL.")
            return "ORAL"
        else:
            return "UNK"

    while True:
        options = "enter a sentence", "enter a document",  "return to main menu"
        for number, choice in enumerate(options):
            print(number, choice)
        print("")
        user = input("Would you like to analyze a sentence, collection of sentences or a document?:")
        print("")

        if user == "0":
            # Sentence Analysis
            sentence = input ("Please enter the sentence: ").split()
            calculate(sentence)
            input("Please press enter to return to the main menu...")

        elif user == "1":
            collective_res = dict()
            # Collection of Sentences from a document
            text= get_text(file_finder())
            content=analyze_content(text)
            tagger_results = spacy_tagger(content)

            for corpus_sentence_id in tagger_results:
                sub_sentences = tagger_results[corpus_sentence_id]
                sentence_info = DiscourseAnalysis.LanguageIndependentAnalysis(sub_sentences)
                sentence = sentence_info.sentence_reconstruction()[1]
                tokens = sentence.split()
                bayes=calculate(tokens)
                collective_res[bayes] = collective_res.get(bayes,0)+1
            print("The results of the analysis are as follows:")

            per = sum(collective_res.values())
            for i in collective_res:
                print(i,collective_res[i],collective_res[i]/per)

        elif user == "3":
            break
        else:
            print(f"{user} is not a valid option. Please enter a valid option.")

#########################
# Main program
#########################


def run_program(default_doc, default_train,system_evaluation):
    """
    This function contains all other functions listed within this script. The functions
    can be selected
    It automatically loads the two standard files, but these can be changed dynamically by the user
    while the script is running.

    :parameter
        :type str
        'default_doc' the path file name for the app_common_default_docs document

        :type str,
        default_doc' the path file name for the app_common_default_docs training file
    :return
        :type None
            This function has no return value
    """

    # The loading time here is assumed to be less than one minute i.e. less than 60 seconds.
    stop = timeit.default_timer()
    execution_time = round(stop - start)
    print(f"All libraries were loaded {execution_time} seconds. The program can now start.\n")

    # This is the menu from which the user can dynamically select an option by entering the respective menu option number.
    main_menu = {
        "load .xml or .txt file": get_text,
        "load training file": get_database,
        "analyze contents": analyze_content,
        "classify sentence": document_classificaiton,
        "clear error log file": clear_log,
        "evaluation": evaluation,
        "about program": about_program,
        "end program": end_program
        }

    # app_common_default_docs data files
    doc = get_text(default_doc)
    database = default_train

    if system_evaluation:
        print("You are currently running the system in evaluation mode.")
        print("To turn this function off, please set system_evaluation to 'False'.\n")

    print("You are currently using the app_common_default_docs files:\n")
    print(f"Default Text: '{default_doc}'")
    print(f"Default Training: '{default_train}'")
    print(" \nIf you wish to proceed with other files, please load them from respective directories.")

    while True:
        """
        The loop is broken once the user has selected an option from the menu. 
        after the desired function has been executed, the user is returned to the main menu 
        unless the program has been terminated by the respective function.
        """

        print("")
        # Text menu message prompt
        banner = "~ Teki - French Discourse Analyzer ~ ", "#### Main Menu ####"
        for word in banner:
            print(word.center(50))

        # Listing the menu options
        for menu_number, menu_item in enumerate(main_menu, start=1):
            print(f'{menu_number}: {menu_item}')

        # Standard message prompts
        choice_str = input('\nPlease enter the number of your entry: ')
        main_message = "Please the enter key to return to the main menu.\n"

        # Executes the function as specified by the user via the number
        if choice_str.isdigit():
            choice_num = int(choice_str)

            # Only menu options that are within the scope of the main menu are allowed
            if 0 < choice_num <= len(main_menu):
                function_values = list(main_menu.values())
                function_number = choice_num - 1
                function_name = str(function_values[function_number]).split()[1]


                # Functions that required parameters are executed here.
                if function_number in list(range(5)):

                    if function_name == "get_text":
                        try:
                            path_name = file_finder()
                            doc = get_text(path_name)
                        except Exception as error:
                            input(f"You did not select a file. {main_message}")
                            logging.exception(f"No txt/xml selection: {error}")

                    elif function_name == "get_database":
                        try:
                            database = get_database()
                        except Exception as error:
                            input(f"You did not select a file. {main_message}")
                            logging.exception(f"No database selection: {error}")

                    elif function_name == "analyze_content":
                        try:
                            content = analyze_content(doc)
                            if content:
                                #  Other functions will be carried out if bool(content) is True
                                collective_results_tagged = spacy_tagger(content)
                                sentence_identification(collective_results_tagged, database, system_evaluation)

                        except Exception as error:
                            print(f"An unknown error occurred. {main_message}")
                            logging.exception(f"Main Menu: {error}")

                    elif function_name == "document_classificaiton":
                        freq = get_feat_count(database)
                        probs = get_probs(freq)
                        document_classificaiton(probs)

                    elif function_name == "clear_log":
                        clear_log('teki_error.log')
                else:
                    # executes functions that do not need argument
                    function_values[function_number]()


if __name__ == "__main__":

    #########################
    # Error Logger
    #########################
    log_file = 'teki_error.log'
    logging.basicConfig(filename=log_file,
                        level=logging.DEBUG,
                        format="""\n%(levelname)s_TIME: %(asctime)s\nFILE_NAME: %(filename)s\nMODULE: %(module)s
                        \nLINE_NO: %(lineno)d\nERROR_SCOPE %(message)s\n"""
                        )


    #########################
    # Program Execution
    #########################
    """
    The main program will only run if all of the necessary files are available and 
    if all of the main libraries have been installed.  This can be overridden by the user, 
    but it is not advised as it can lead to the program becoming unstable.  
    """
    system_evaluation = False
    try:
        default_doc = r"app_resources/app_common_default_docs/mueller_oral.txt"
        default_train = r"app_resources/app_common_default_docs/default_training.csv"
        if bool(core_file_missing) is False and bool(library_error) is False:
            run_program(default_doc, default_train,system_evaluation)
        else:
            message = "An error has occurred because either files, libraries or directories are missing."
            if core_file_missing:
                for i in core_file_missing:
                    print(i)
                print("")

            if library_error:
                for i in library_error:
                    print(i)
            print("Please also consult the error log if this does not solve your provide you with a solution.\n")
            continue_program(message)
            run_program(default_doc, default_train,system_evaluation)

    except Exception as error:
        print("An unexpected error occurred. Please check the error log.")
        logging.exception(f" 'if __name__ == __main__': is due to '{error})'")