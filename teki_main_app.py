# -*- coding: utf-8 -*-

#########################
#dev_documentation description
#########################

'''
This program's function is to access the literate and oral nature of French chat data. 
'''

#########################
#Program continuation function
#########################

def continue_program(*args):
    '''
    This is an error prompt to give the user the ability to continue or terminate the program.
    The corresponding error messages can be passed to the function
    '''

    #Displays the error prompt messages.
    for message in args:
        print(message)
    print("")

    while True:
        '''
        The while-loop remains in place until the user provides an appropriate response
        '''
        user = input("Would you still like to continue with the program (y/n) ?: ").lower()

        if user=="y":

            user=input("Are you sure? Program stability cannot be guaranteed (y/n)?: ").lower()

            if user=="y":
                break
            else:
                print("The program will now be terminated.")
                raise SystemExit

        elif user=="n":
            print("The program will now be terminated.")
            raise SystemExit

        else:
            print(f"{user} is not a valid  response. Please enter a valid response.\n")

print("Please wait while libraries and files are being imported...")

def missing_files(file_list,path):
    missing = list()

    # files
    for root in os.listdir(path):
            if root not in file_list:
                missing.append(root)
    if missing:
        return  missing
    else:
        return False

#########################
#Importing standard python libraries
#########################
import importlib,os,sys,traceback

#########################
#Importing pip libraries
#########################
pip_lib = "bs4", "spacy", "spellchecker", "matplotlib", "lxml"
missing_libraries=[]

for lib in pip_lib:
        try:
            globals()[lib] = importlib.import_module(lib)
        except ModuleNotFoundError as error:
            missing_libraries.append(lib)

if missing_libraries==False:

    # Spacy imports
    from spacy.lang.fr import French
    from spacy.tokenizer import Tokenizer

#########################
# Importing custom files and modules
#########################

'''
A program-wide check is performed. 
The program can still be started if any of the necessary files are missing, 
but the program stability will be greatly compromised. 
'''

if os.path.exists("app_resources"):

    #Text files
    app_docs = [
        "app_docs/program_description.txt",
        "program_description.txt",
        "author_information.json",
        "missing_lib.txt"
    ]
    missing_text_files = missing_files(app_docs, "app_resources/app_docs")

    #Development and training data
    dev_files=[
            "gerstenberg-hewett-ebay-anon.xml"
        ]
    missing_dev_files = missing_files(dev_files, "app_resources/app_dev/dev_files")

    #Test Data
    test_files=[
            "dummy.txt"
        ]
    missing_test_files = missing_files(test_files, "app_resources/app_test/test_files")

    # Compressed repository
    compressed_respostiory=os.path.exists("app_resources/compressed_language_data/cmr-88milsms-tei-v1.zip")

else:
    message="The app resource directory is either missing or has been renamed."
    continue_program(message)

#########################
# Custom modules
#########################
from app_resources.auxilary_functions import (
    program_description,
    author_information,
    menu,
    file_finder)

#########################
# Main Program Functions
#########################

def get_text(document):
    '''
    This reads in the file to be analyzed. The function separates the files into two types:
    .xml and other.  The program assumes that other file type is some variant of a normal .txt file.
    '''

    if ".xml" in document:

        with open(document, mode="r", encoding="utf-8") as file:
            soup = bs4.BeautifulSoup(file, "lxml")
            return soup

    else:
        with open(document, mode="r", encoding="utf-8") as file:
            read=file.read()
            return read

def read_content(soup):

    def read_soup():
        '''
        Reads in the .xml soup
        '''
        if str(type(soup))=="<class 'bs4.BeautifulSoup'>":
            print(soup)
            return soup

    def extract_ebay():
        '''
        Extracts the eBay posting
        '''
        #sub_id="ebayfr-e17p"
        # corpus=soup.find("subcorpus",subcorpus_id=sub_id)

        tk=soup.find("div", id="e17p-300").getText().strip().split()

        return " ".join(tk)

    def extract_sms():
        # document = "app_resources/app_dev/dev_files/88milsms-tei-v1/cmr-88milsms-tei-v1.xml"
        #
        # i = 0
        # with open(document, mode="r", encoding="utf-8") as file, open(
        #         "app_resources/app_test/test_files/sms_44265_88522.xml", mode="w+", encoding="utf-8") as out:
        #     soup = bs4.BeautifulSoup(file, "lxml")
        #     text = soup.findAll("post")
        #
        #     for line in text:
        #         i += 1
        #
        #         if i > 44265:
        #             print(i, line)
        #
        #             out.write(str(line))
            pass

    def extract_wiki():
        i = 0
        document=0
        with open(document, mode="r", encoding="utf-8") as file, open(
                "app_resources/app_test/test_files/wikiconflits_79_159.xml", mode="w+", encoding="utf-8") as out:
            soup = bs4.BeautifulSoup(file, "lxml")
            text = soup.findAll("post")

            for line in text:
                i += 1

                if i > 79:
                    print(i, line)

                    out.write(str(line))

    def quit():
        return False

    output_menu={"read_soup":read_soup,
                 "extract_ebay":extract_ebay,
                 "quit":quit
    }

    # Submenu
    menu_name="option menu"
    menu_information="How would you like to proceed with the file:"
    mn=menu(output_menu,menu_name,  menu_information)

    return mn

def tokenizer():
    nlp = French()
    tokenizer = Tokenizer(nlp.vocab)

def tagger(content):
    nlp = spacy.load("fr_core_news_sm")
    doc=nlp(content)
    for token in doc:
        print(token.text, token.pos_, token.dep_)

def naive_bayes():
    pass

def gold_tager():
    pass

def evaluation():
    pass










#########################
# Main program
#########################
def run_program():

    '''
    This is the main function of the program. It incorporates all other functions from this file
    as well as the from the secondary python file.
    It is executed under the if __name__ statement.
    '''

    menu_option = {
                   "import file": get_text,
                   "read contents":read_content,

                    "author information": author_information,
                    "program description": program_description,
                    "end program": sys.exit}
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

                    if func_name=="function":
                        #Exits program
                        func_list[function_number]("The program has been successfully terminated.")

                    else:

                        try:
                            #Executes functions that do not require arguments
                            func_list[function_number]()

                        except:
                            #Loads the file into  memory
                            if func_name== "get_text":
                                doc=get_text(file_finder())

                            elif func_name=="read_content":
                                try:
                                    content=read_content(doc)
                                    tagger(content)

                                except Exception:

                                    input(f"You must first load the file into memory. {main_message} ")

                                    # Error Log from Except
                                    with open("app_resources/app_docs/file.log", mode="a") as log:
                                        log.write(traceback.format_exc())

                            with open("app_resources/app_docs/file.log", mode="a") as log:
                                log.write(traceback.format_exc())
                else:
                    input(f"You have entered an incorrect number. {main_message}")


#########################
#dev_documentation Execution
#########################

if __name__ == "__main__":
    '''
    The main program will only run if all of the necessary files are available and if all of the main libraries have been installed. 
    This can be overridden by the user, but it is not advised as it can lead to the program becoming unstable.  
    '''
    #########################
    # Main master check
    #########################
    core_files_missing = missing_dev_files, missing_text_files, missing_test_files, compressed_respostiory
    core_files_missing=False
    if bool(core_files_missing) == False and bool(missing_libraries) == False:
        print("All libraries have been successfully loaded. The program will now start.")
        run_program()
    else:
        message = "An error has occured because either files or directories are missing."
        continue_program(message)
        run_program()
