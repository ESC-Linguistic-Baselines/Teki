# -*- coding: utf-8 -*-

#########################
#Importing standard python libraries
#########################
import importlib,os,sys,traceback,csv,json

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
    This is an error prompt to give the user the ability to continue or terminate the program.
    The corresponding error messages can be passed to the function.
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

print("Please wait while libraries and files are being imported...")
print("This could take a while depending on your system resources.\n")

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

def error_log():
    """
    This logs all of the error files that occur within the program.
    This will only be activated if the variable debug is set to true.
    Some errors are intentionally, while others might occur
    due to improper file types.
    """
    with open("app_resources/app_docs/error.log", mode="a") as log:
        error=traceback.format_exc()
        log.write(f"{error}\n")

#########################
#Importing pip libraries
#########################
"""
The libraries are iteratively imported. 
The libraries that are missing will be saved in a list that will be referenced against later
"""

pip_lib = "bs4", "spacy", "lxml"
missing_libraries=[]

for lib in pip_lib:
    #Iteratively loads the libraries using importlib
        try:
            globals()[lib] = importlib.import_module(lib)
        except ModuleNotFoundError as error:
            missing_libraries.append(lib)

if missing_libraries==False:
    #If no libraries are missing, then the necessary modules will be imported.

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

    #Text files
    missing_doc_files = missing_files(necessary_files["docs"], "app_resources/app_docs")

    #Development and training data
    missing_dev_files = missing_files(necessary_files["dev"], "app_resources/app_dev/dev_files")

    #Test Data
    missing_test_files = missing_files(necessary_files["test"], "app_resources/app_test/test_files")

    #Compressed repository
    missing_compressed_respostiory = missing_files(necessary_files["compressed"], "app_resources/compressed_data")
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
            file_finder,
        program_end)
    except:
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
            read=file.read()
            return read

def get_database():
    '''
    This function reads in the training file saved in the progam.
    It will be used with the naive bayes classifier.
    '''

    database="app_resources/train_files/training_res.csv"
    csv_data=list()

    with open (database,mode="r",encoding="utf-8") as data:
        csv_reader=csv.reader(data,delimiter=",")
        for row in csv_reader:

            #Skips empty lines
            if row:
                csv_data.append(row)

    return csv_data

def analyze_content(soup):

    def read_soup():
        """
        Reads in the .xml soup
        """

        if str(type(soup))=="<class 'bs4.BeautifulSoup'>":
            print(soup)
            return False

    def extract_text():
        """
        This function extracts the entries from the respective .xml.
        """

        while True:
            corpus="Ebay","Sms","Wikiconflit"
            for num,cor in enumerate(corpus,start=1):
                print(num,cor)

            corpus_search=input("\nFrom which corpus are you extracting the message?")

            xml_tag_id=list()

            if corpus_search=="1":
                for tag in soup.select("div[id]"):
                    xml_tag_id.append(tag["id"])

            elif corpus_search=="2":
                pass
            elif corpus_search=="3":
                pass
            else:
                print("You did not enter a valid corpus number.\n")

            while True:
                print(f"There are {len(xml_tag_id)} tags. Please enter a number from 0 - {len(xml_tag_id)}.")
                corpus_tag_choice = input("Please enter a valid tag: ")

                try:
                    choice=int(corpus_tag_choice)
                    corpus_text = soup.find("div", id=xml_tag_id[choice]).getText().strip().split()
                    return {xml_tag_id[choice]:" ".join(corpus_text)}
                except:
                    print(f"{corpus_tag_choice} is not a valid choice. Please try again.\n")

    def text_extract():
        pass

    def quit():
        #Returns false to break the loop in the menu.
        return False

    output_menu={"read file":read_soup,
                 "extract entry":extract_text,
                 "quit":quit
                }

    #Submenu
    menu_name="option menu"
    menu_information="How would you like to proceed with the file:"
    mn=menu(output_menu,menu_name,  menu_information)

    return mn

def tagger(corpus_content):
    """
    This function relies on the Spacy module for assessing the linguistic properties of a given sentence or a batch of sentences.
    """

    print("The sentence is being tagged... Please wait...")
    nlp = spacy.load("fr_core_news_sm")

    doc=nlp(*corpus_content.values())

    sentence_results={}
    i=0

    for token in doc:
        sentence_results[str(i)]=token.text, token.pos_, token.dep_,*corpus_content
        i+=1

    return sentence_results

def identify_oral_literal(sentence_results):
    """
    This function has the goal of assessing orality and literacy in a tag.
    """

    analysis_results="app_resources/train_files/training_res.csv"
    fnames ="token_text","token_pos","token_dep","token_id","oral_literate"

    sentence=""
    pos={}

    #Tagger using criteria
    for word in sentence_results:
        line=sentence_results[word]

        #Reconstructing the sentence
        sentence+=line[0]+" "

        #counting POS
        if line[1] not in pos:
            pos[line[1]]=1
        else:
            pos[line[1]]+=1

    def res(feature):
        with open(analysis_results, mode="w", encoding="utf-8") as analysis:
            writer = csv.DictWriter(analysis, fieldnames=fnames)

            for word in sentence_results:
                line = sentence_results[word]
                writer.writerow(
                    {"token_text": line[0],
                     "token_pos": line[1],
                     "token_dep": line[2],
                     "token_id": line[3],
                     "oral_literate": feature
                     })

    if pos["NOUN"] > 2:
        res("litereate")

    #Tagger using simplified criteria

def get_freq(csv_reader):
    freq={"ORAL":0,  "LIT":0}
    feat_1="ORAL"
    feat_2="LIT"

    for row in csv_reader:

        if row[4]==feat_1:
            freq[feat_1]=freq.get(feat_1)+1
        else:
            if row[4]==feat_2:
                freq[feat_2] = freq.get(feat_2) + 1
    return freq


def get_probs(freq,csv_reader):
    lit=dict()
    oral=dict()

    vocabluary=set()
    lit_tokens=list()
    oral_tokens=list()

    res=dict()
    for word in csv_reader:
        voc=word[0]
        feat=word[4]
        vocabluary.add(voc)

        if feat=="ORAL":
            oral_tokens.append((voc,feat))
        else:
            lit_tokens.append((voc,feat))

    for word in csv_reader:
        if word[4]=="ORAL":
            lit[word[0]]=lit.get(word[0],0)+1
        else:
            oral[word[0]] = oral.get(word[0], 0)+1

    for word in vocabluary:

        if lit.get(word,0) > 0:
            tr=lit.get(word)/freq["LIT"]
        else:
            tr=freq["LIT"]/(sum(freq.values())**2)

        if oral.get(word,0) > 0:
            fl=oral.get(word)/freq["LIT"]
        else:
            fl=freq["LIT"]/(sum(freq.values())**2)

        res[word]=tr,fl
    return res

def classify(text,probs,prior_prob):

    true = prior_prob["ORAL"] / (prior_prob["ORAL"] + prior_prob["LIT"])
    false = prior_prob["LIT"] / (prior_prob["ORAL"] + prior_prob["LIT"])
    true_smooth = prior_prob["ORAL"] / (sum(prior_prob.values()) ** 2)
    false_smooth = prior_prob["LIT"] / (sum(prior_prob.values()) ** 2)

    s = dict()

    for word in text:
        if bool(probs.get(word)):
            s[word] = probs.get(word)
        else:
            s[word] = true_smooth, false_smooth

    for word in s:
        true *= s[word][0]

        false *= s[word][1]

    res = true, false
    ans = 1

    system_results = {"TP": 0, "FP": 0, "FN": 0}

    if true > false:
        ans = 0

        print(f" is true with {true}")
    else:
        print(f" ' {text} ' is false with ", false)

    for word in s:
        system = s[word][ans]
        max_arg = max(s[word])

        if system == max_arg:
            system_results["TP"] = system_results.get("TP") + 1

        elif system == s[word][1]:
            system_results["FP"] = system_results.get("FP") + 1

        elif system == s[word][0]:
            system_results["FN"] = system_results.get("FN") + 1

    TP, FP, FN = system_results["TP"], system_results["FP"], system_results["FN"]

    precision = TP / (TP + FP)
    recall = TP / (TP + FN)

    system_prob = 1
    values = list()
    for i in s:
        values.append(max(s[i]))

    for i in values:
        system_prob *= i

#########################
#Main program
#########################
def run_program(debug):

    """
    This is the main function of the program. It incorporates all other functions from this file
    as well as the from the secondary python file.
    It is executed under the if __name__ statement.
    """

    menu_option = {
                   "import file": get_text,
                    "analyze contents":analyze_content,
                    "load training file": get_database,
                    "classify string": classify,
                    "author information": author_information,
                    "program description": program_description,
                    "end program": program_end}
    while True:
            print()
            banner = "~ Teki - French Chat Analyzer ~ ", "#### Main Menu ####"
            for word in banner: print(word.center(50))
            for num, elem in enumerate(menu_option, start=1):
                print(f'{num}: {elem}')

            choice_str = input('\nPlease enter the number of your entry: ')
            main_message="Please the enter key to return to the main menu."

            #Executes the function as specified by the user via the number
            if choice_str.isdigit():
                choice_num = int(choice_str)

                if 0 < choice_num and choice_num <= len(menu_option):
                    func_list = list(menu_option.values())
                    function_number = choice_num - 1
                    func_name=str(func_list[function_number]).split()[1]

                    arg=list(range(4))
                    if function_number in arg:

                        if func_name == "get_text":
                            doc = get_text(file_finder())

                        elif func_name == "read_content":
                            try:
                                content = analyze_content(doc)

                                #Other functions will be carried out if conent comes back as True
                                if content:

                                    tagged = tagger(content)
                                    identify_oral_literal(tagged)
                            except:
                                input(f"An unexpected error occurred. {main_message} ")
                                if debug: error_log()

                        elif func_name=="classify":
                            '''
                            This calls up the naive bayes function to classifiy the texts.
                            '''

                            text = input("Enter the sentence that you would like to classify: ")

                            #The training corpus
                            train=get_database()

                            #This gets the frequency of ORAL and LIT (the features) of the data set.
                            freq=get_freq(train)

                            #This returns the MLE prob of the features.
                            probs = get_probs(freq, train)

                            #Naive bayes
                            classify(text, probs, freq)

                    else:
                        #executes functions that do not need argument
                        func_list[function_number]()

#########################
#dev_documentation Execution
#########################

if __name__ == "__main__":
    """
    The main program will only run if all of the necessary files are available and if all of the main libraries have been installed. 
    This can be overridden by the user, but it is not advised as it can lead to the program becoming unstable.  
    """

    debug=True
    if bool(core_file_missing) == False and bool(missing_libraries) == False:
        print("All libraries have been successfully loaded. The program will now start.")
        run_program(debug)
    else:
        message = "An error has occurred because either files or directories are missing."
        continue_program(message)
        run_program(debug)