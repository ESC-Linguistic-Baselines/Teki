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
            print(f"{user} is not a valid  response. Please enter a valid response.\n")

print("Please wait while libraries and files are being imported...")

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
        log.write(traceback.format_exc()+"\n")

#########################
#Importing pip libraries
#########################

"""
The libraries are iteratively imported. 
The libraries that are missing will be saved
"""

pip_lib = "bs4", "spacy", "lxml"
missing_libraries=[]

for lib in pip_lib:
        try:
            globals()[lib] = importlib.import_module(lib)
        except ModuleNotFoundError as error:
            missing_libraries.append(lib)

if missing_libraries==False:
    """
    if no libraries are missing, then the necessary modules will  be imported
    """
    #Spacy imports
    from spacy.lang.fr import French
    from spacy.tokenizer import Tokenizer

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
            file_finder)
    except:
        pass

#########################
#Main Program Functions
#########################

def get_text(document):
    """
    This reads in the file to be analyzed. The function separates the files into two types:
    .xml and other.  The program assumes that other file type is some variant of a normal .txt file.
    """

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
        """
        Reads in the .xml soup
        """

        if str(type(soup))=="<class 'bs4.BeautifulSoup'>":  print(soup)

    def soup_extract():
        """
        This function extracts the entries from the respective .xml.
        """

        while True:
            corpus="Ebay","Sms","Wikiconflit"
            for num,cor in corpus:
                print(num,cor)

            corpus_search=input("\nFrom which corpus do you wish to extract the message?")

            xml_tag_id=list()
            if corpus_search=="1":
                for tag in soup.select("div[id]"):
                    xml_tag_id.append(tag["id"])

            elif corpus_search=="2":
                pass
            elif corpus_search=="3":
                pass
            else:
                print("You did not enter a valid corpus number.")

            print(f"There are {len(xml_tag_id)} tags. Please enter a number from 0 - {len(xml_tag_id)}.")
            corpus_tag_choice=input("Please choose a tag: ")

            while True:
                #Only digits are an accepted input.
                if corpus_tag_choice.isdigit()==False:
                    print("That is not a valid nubmer.")
                elif corpus_tag_choice.isdigit()==True:
                    tk = soup.find("div", id=xml_tag_id[int(corpus_tag_choice)]).getText().strip().split()
                    return " ".join(tk)

    def text_extract():
        pass

    def quit():
        return False

    output_menu={"Read soup":read_soup,
                 "Extract soup text":soup_extract,
                 "quit":quit
    }

    # Submenu
    menu_name="option menu"
    menu_information="How would you like to proceed with the file:"
    mn=menu(output_menu,menu_name,  menu_information)

    return mn

def tagger(content):
    """
    This function relies on the Spacy module for assessing the linguistic properties of a given sentence or a batch of sentences.
    """
    print("The sentence is being tagged... Please wait...")

    nlp = spacy.load("fr_core_news_sm")
    doc=nlp(content)

    print("p")

    res={}
    i=0
    for token in doc:
        res[str(i)]=token.text, token.pos_, token.dep_
        i+=1
    return res

def identify_oral_literal(tagged_res):
    """
    This function has the goal of assessing orality and literacy in a tag

    """
    sentence=None
    pos=None

    # Tagger using criteria
    for word in tagged_res:
        line=tagged_res[word]

    with open("app_resources/train_files/training_res.txt",mode="a+",encoding="utf-8") as training:
        for word in tagged_res:
            print(tagged_res[word][0])
            training.write(str(tagged_res[word][0])+"\n")
        print("file saved")


    # Tagger using simplified criteria


def evaluation():
    pass

#########################
# Main program
#########################
def run_program(debug):

    """
    This is the main function of the program. It incorporates all other functions from this file
    as well as the from the secondary python file.
    It is executed under the if __name__ statement.
    """

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
                                    tagged=tagger(content)
                                    identify_oral_literal(tagged)

                                except Exception:
                                    input(f"You must first load the file into memory. {main_message} ")
                                    # Error Log from second Try- Except
                                    if debug: error_log()

                            #Error Log from second Try-Except
                            if debug: error_log()

                else:
                    input(f"You have entered an incorrect number. {main_message}")


#########################
#dev_documentation Execution
#########################

if __name__ == "__main__":
    """
    The main program will only run if all of the necessary files are available and if all of the main libraries have been installed. 
    This can be overridden by the user, but it is not advised as it can lead to the program becoming unstable.  
    """
    #########################
    # Main master check
    #########################

    debug=True
    if bool(core_file_missing) == False and bool(missing_libraries) == False:
        print("All libraries have been successfully loaded. The program will now start.")
        run_program(debug)
    else:
        message = "An error has occurred because either files or directories are missing."
        continue_program(message)
        run_program(debug)
