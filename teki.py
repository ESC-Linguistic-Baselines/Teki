# -*- coding: utf-8 -*-

if __name__ == '__main__':
    print("Please wait while libraries and files are being imported...")
    print("This could take a while depending on your system resources.\n")

#########################
#Importing standard python libraries
#########################
import importlib,os,sys,traceback,csv,json,logging,pickle

#########################
#Program description
#########################
"""
This program's function is to access the literate and oral nature of French chat data
by using markers that can identify said features.
"""

#########################
#Program continuation function
#########################

def continue_program(*args):
    """
    input:

    function

    output:
    """

    #Displays the error prompt messages.
    for message in args:
        print(message)
    print("")

    while True:
        #The while-loop remains in place until the user provides an appropriate response
        user = input("Would you still like to continue with the program (y/n) ?: ").lower()

        #Yes answer
        if user=="y":
            user=input("Are you sure? Program stability cannot be guaranteed (y/n)?: ").lower()

            #Yes answer
            if user=="y":
                break
                #The program will be continued even though there is no stability.
            else:
                sys.exit("The program will now be terminated.")

        #No answer
        elif user=="n":
            sys.exit("The program will now be terminated.")

        #Incorrect answer
        else:
            print(f"{user} is not a valid response. Please enter a valid response.\n")

def missing_files(file_list,path):
    """
    This function is make sure that all of the necessary files are available.
    Without all of the files, the stability of the program cannot be ensured.
    """

    missing = list()

    #This checks to make sure that the files are available.
    for root in os.listdir(path):
        if root not in file_list:
            missing.append(root)

    #If not all files are available, then a list of said files are returned.
    if missing:
        return missing
    #False is the desired result. This means that all files are available i.e. not missing
    else:
        return False

#########################
#Importing pip libraries
#########################
"""
The libraries are iteratively imported. 
The libraries that are missing will be saved in a list that will be referenced against later.
"""

pip_lib = "bs4", "spacy", "lxml"
missing_libraries=[]

for lib in pip_lib:
    #Iteratively loads the libraries using importlib
        try:
            globals()[lib] = importlib.import_module(lib)
        except ModuleNotFoundError as error:
            missing_libraries.append(lib)

#If no libraries are missing, then the necessary modules will be imported.
if missing_libraries==False:

    #Spacy imports
    from spacy.lang.fr import French
    from spacy.tokenizer import Tokenizer
    from bs4 import BeautifulSoup

#########################
#Importing custom files and modules
#########################
"""
A program-wide check is performed. 
The program can still be started if any of the necessary files are missing, 
but the program stability will be greatly compromised. 
"""

#Necessary file names stored in json format
data=open("app_resource_files.json", mode="r", encoding="utf-8")
necessary_files=json.load(data)

if os.path.exists("app_resources"):
    missing_doc_files = missing_files(necessary_files["docs"], "app_resources/app_docs")#Text files
    missing_dev_files = missing_files(necessary_files["dev"], "app_resources/app_dev/dev_files")#Development and training data
    missing_test_files = missing_files(necessary_files["test"], "app_resources/app_test/test_files") #Test Data
    missing_compressed_respostiory = missing_files(necessary_files["compressed"], "app_resources/compressed_data")#Compressed repository
else:
    message="The app resource directory is either missing or has been renamed."
    continue_program(message)

#This lets the program know if files are missing.
core_files = missing_dev_files, missing_doc_files, missing_test_files, missing_compressed_respostiory
core_file_missing=sum([bool(i) for i in core_files])

#########################
#Custom modules
#########################
"""
These are custom modules that are quality of life improvements.
They are stored in the app_resource directory. 
"""

if core_file_missing==False:
    try:
        from app_resources.auxilary_functions import (
            program_description,
            author_information,
            menu,
            clear_log,
            file_finder,
            sentence_tokenizer,
            program_end)
    except ImportError as error:
        pass

#########################
#Main Program Functions
#########################

def get_text(document):
    """
    This reads in the file to be analyzed. The function separates the files into two types:
    .xml and other. The program assumes that other file type is some variant of a normal .txt file.
    """

    if ".xml" in document:
        with open(document, mode="r", encoding="utf-8") as file:
            soup = bs4.BeautifulSoup(file, "lxml")
            return soup

    else:
        with open(document, mode="r", encoding="utf-8") as file:
            text=file.read()
            return text

def get_database():
    """
    This function reads in the training file saved in the progam.
    It will be used with the naive bayes classifier.
    """

    database=r"C:\Users\chris\Desktop\Bachleorarbeit\sandbox\cl_2.csv"

    return database

def analyze_content(text_object,abbr):

    def read_contents():
        """
        This function simply displays the contents of the xml file in console.
        """

        print(text_object)

    def extract_xml():
        """
        This function extracts the entries from the respective .xml. files
        """
        soup=text_object
        msg="The text has been parsed into sentences. Press enter to continue."

        while True:
            corpus = "eBay", "SMS", "Wikiconflit"
            for num, cor in enumerate(corpus, start=1):
                print(num, cor)

            corpus_search = input("\nFrom which corpus are you extracting the message?")

            xml_tag_id = list()

            if corpus_search == "1":
                #eBay listing
                for tag in soup.select("div[id]"):
                    xml_tag_id.append(tag["id"])

            elif corpus_search in ("2", "3"):
                #SMS, Wikiconflict
                for tag in soup.select("post"):
                    xml_tag_id.append(tag["xml:id"])
            else:
                print("You did not enter a valid corpus number.\n")

            while True:
                print(f"There are {len(xml_tag_id)} tags. Please enter a number from 0 - {len(xml_tag_id)}.")
                corpus_tag_choice = input("Please enter a valid tag: ")

                try:
                    choice = int(corpus_tag_choice)

                    if corpus_search == "1":
                        corpus_text = soup.find("div", id=xml_tag_id[choice]).getText().strip().split()
                        results = sentence_tokenizer(corpus_text, abbr)

                        input(msg)
                        return (results,xml_tag_id[choice])

                    else:
                        corpus_text = soup.find("post", {"xml:id": xml_tag_id[choice]}).getText().strip().split()
                        results = sentence_tokenizer(corpus_text, abbr)
                        input(msg)

                        return (results, xml_tag_id[choice])

                except Exception as error:
                    print(error)
                    logging.exception(error)
                    print(f"{corpus_tag_choice} is not a valid choice. Please try again.\n")

    def extract_text():

        tokens=text_object.split()
        results=sentence_tokenizer(tokens, abbr)
        msg=input("The text has been parsed into sentences. Press enter to continue.")
        return (results,"NO_TAG")

    def quit():
        #Returns false to break the loop in the menu.
        return False

    output_menu={"read file":read_contents,
                 "extract XML":extract_xml,
                 "extract txt":extract_text,
                 "quit":quit
                }

    #Submenu
    menu_name="option menu"
    menu_information="How would you like to proceed with the file:"
    mn=menu(output_menu,menu_name,  menu_information)

    return mn

def spacy_tagger(corpus_content):
    """
    After the the texts have been parsed into sentences,
    the respective sentences will then be tokenized
    """

    print("The individual sentences are now being tagged for parts of speech. Please wait...")

    print(corpus_content)
    corpus=corpus_content[0][0]
    tag=corpus_content[1]
    result = {sen: list() for sen in range(len(corpus))}
    nlp = spacy.load("fr_core_news_sm")

    for i in range(len(corpus)):
        s = "".join(corpus[i])
        doc = nlp(s)
        for token in doc:
            sentence_results = token.text, token.pos_, token.dep_
            result[i].append((sentence_results))

    input("The sentences have been succesfully tagged. Please press enter to continue...")
    return (result,tag)

def identify_oral_literal(sentence_results,database):
    """
    input:

    function

    output:
    """

    analysis_results = database
    fnames = "token_text", "token_pos", "token_dep", "token_id","sen_no", "oral_literate"

    def res(sen_info, feature, ID,sen_no):

        with open(analysis_results, mode="a", encoding="utf-8", newline="") as analysis:
            writer = csv.DictWriter(analysis, fieldnames=fnames)

            for entry in sen_info:

                tok_txt = entry[0]
                tok_pos = entry[1]
                tok_dep = entry[2]

                writer.writerow(
                    {"token_text": tok_txt,
                     "token_pos": tok_pos,
                     "token_dep": tok_dep,
                     "token_id": ID,
                     "sen_no":f"SEN:{sen_no}",
                     "oral_literate": feature
                     })

    sentence_info = sentence_results[0]

    id = sentence_results[1]
    sen_no=0
    pos = {}

    for entry in sentence_info:
        sen_no+=1
        for i in sentence_info[entry]:
            POS = i[1]

            # counting POS
            if POS not in pos:
                pos[POS] = 1
            else:
                pos[POS] += 1

        res(sentence_info[entry], "ORAL", id,sen_no)

def get_freq(file):
    """
    This function gets the counter for ORAL and LIT in the training file.
    It returns the frequency of the features and the entries from the csv files.
    """

    with open(file, mode="r", encoding="utf-8") as file_data:
        csv_reader = csv.reader(file_data, delimiter=",")
        file_data = [row for row in csv_reader]
        freq = {"ORAL": 0, "LIT": 0}

        sentence_id={(row[3],row[4],row[5]) for row in file_data}
        for sentence in sentence_id:
            entry=sentence[2]
            freq[entry] = freq.get(entry) + 1

        return freq,file_data

def get_probs(csv_results):
    """
    input:

    function

    output:
    """

    results = dict()

    freq = csv_results[0]
    csv_data = csv_results[1]

    lit_freq,oral_freq = dict(),dict()
    lit_tokens,oral_tokens=list(),list()
    vocabluary = set()
    ng_smooth=sum(freq.values()) ** 2

    for element in csv_data:
        word,feat = element[0],element[5]
        vocabluary.add(word)

        if feat == "ORAL":
            oral_tokens.append((word, feat))
            oral_freq[element[0]] = oral_freq.get(element[0], 0) + 1

        elif feat == "LIT":
            lit_tokens.append((word, feat))
            lit_freq[element[0]] = lit_freq.get(element[0], 0) + 1


    for element in vocabluary:
        if lit_freq.get(element, 0) > 0:
            lit = lit_freq.get(element) / freq["LIT"]

        else:
            lit = freq["LIT"] / (ng_smooth)

        if oral_freq.get(element, 0) > 0:
            oral = oral_freq.get(element) / freq["ORAL"]

        else:
            oral = freq["ORAL"] / (ng_smooth)

        results[element] = oral,lit
    return results,freq

def classify(text, res):
    """
    input:

    function

    output:
    """

    probs,prior_prob=res[0],res[1]

    oral_prob,lit_prob=prior_prob["ORAL"],prior_prob["LIT"]
    orality = oral_prob/ (oral_prob + lit_prob)
    literality = lit_prob / (oral_prob + lit_prob)
    ng=sum(prior_prob.values()) ** 2
    orality_smooth = oral_prob/ ng
    literacy_smooth = lit_prob / ng

    sentence_prob = dict()

    for word in text:
        if bool(probs.get(word)):
            sentence_prob[word] = probs.get(word)

        else:
           sentence_prob[word] = orality_smooth, literacy_smooth

    for word in sentence_prob:

        orality *= sentence_prob[word][0]
        literality *= sentence_prob[word][1]

    if literality > orality :
        print(f" {text} is literal {literality}")
    else:
        print(f" '  {text} ' is oral {orality}")
    print(sentence_prob)
    input()
######


#########################
#Main program
#########################
def run_program(debug):
    """
    input:

    function

    output:
    """

    menu_option = {
                   "import file": get_text,
                    "load training file": get_database,
                    "analyze contents":analyze_content,
                    "classify string": classify,
                    "clear log file":clear_log,
                    "author information": author_information,
                    "program description": program_description,
                    "end program": program_end
                    }

    while True:
        print("")
        banner = "~ Teki - French Chat Analyzer ~ ", "#### Main Menu ####"
        for word in banner: print(word.center(50))
        for num, elem in enumerate(menu_option, start=1):
            print(f'{num}: {elem}')

        choice_str = input('\nPlease enter the number of your entry: ')
        main_message="Please the enter key to return to the main menu.\n"

        #Executes the function as specified by the user via the number
        if choice_str.isdigit():
            choice_num = int(choice_str)

            if 0 < choice_num and choice_num <= len(menu_option):
                func_list = list(menu_option.values())
                function_number = choice_num - 1
                func_name=str(func_list[function_number]).split()[1]

                if function_number in list(range(5)):

                    if func_name == "get_text":

                        try:
                            d=r"C:\Users\chris\Desktop\Bachleorarbeit\app_resources\app_test\test_files\ebayfr-e05p.xml"
                            doc = get_text(d)
                        except:
                            input(f"You did not select a file. {main_message}")

                    elif func_name=="get_database":
                        try:
                            train=get_database()
                        except:
                            input(f"You did not select a file. {main_message}")

                    elif func_name == "analyze_content":

                        try:
                            abbr="app_resources/app_docs/abbrev.lex"
                            content = analyze_content(doc,abbr)

                            #Other functions will be carried out if bool(content) == True
                            if content:
                                tagged = spacy_tagger(content)
                                identify_oral_literal(tagged,train)

                        except Exception as error:
                            print("An unknown error occured.")
                            input(f"{main_message} ")
                            logging.exception(error)

                    elif func_name=="classify":
                        """
                        This calls up the naive bayes function to classifiy the texts.
                        """

                        #text = input("Enter the sentence that you would like to classify: ")
                        text="a seat at the bar which serves up surprisingly"

                        #This gets the frequency of ORAL and LIT (the features) of the data set.
                        freq=get_freq(train)

                        #This returns the MLE prob of the features.
                        probs = get_probs(freq)

                        #Naive bayes classifier
                        classify(text.split(), probs)

                    elif func_name=="clear_log":
                        clear_log('app_resources/app_docs/error.log')


                else:
                    #executes functions that do not need argument
                    func_list[function_number]()

#########################
#Debugger
#########################
"""
This logs all of the error files that occur within the program.
This will only be activated if the variable debug is set to true.
Some errors are intentionally, while others might occur due to improper file types.
"""
f='app_resources/app_docs/error.log'

logging.basicConfig(filename=f,
                    level=logging.DEBUG,
                    format="\n%(levelname)s_TIME: %(asctime)s\nFILE_NAME: %(filename)s\nMODULE: %(module)s\nLINE_NO: %(lineno)d\nERROR_NAME: %(message)s\n"
                    )

#########################
#dev_documentation Execution
#########################

if __name__ == "__main__":
    """
    The main program will only run if all of the necessary files are available and if all of the main libraries have been installed. 
    This can be overridden by the user, but it is not advised as it can lead to the program becoming unstable.  
    """

    try:
        debug=True
        if bool(core_file_missing) == False and bool(missing_libraries) == False:
            print("All libraries have been successfully loaded. The program will now start.")
            run_program(debug)
        else:
            message = "An error has occurred because either files or directories are missing."
            continue_program(message)
            run_program(debug)
    except Exception as error:
        logging.exception("Main Exception in "+str(error))