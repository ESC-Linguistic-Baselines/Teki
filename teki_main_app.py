# -*- coding: utf-8 -*-

#########################
#Documentation description
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
        user = input("Would you still like to continue with the program?  y/n").lower()

        if user=="y":

            user=input("Are you sure. Program stability cannot be guaranteed y/n").lower()

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

#########################
#Importing standard python libraries
#########################

import importlib,zipfile,re,os,shutil,tkinter,sys,time,datetime

#########################
#Importing pip libraries
#########################

pip_lib = "bs4", "spacy", "spellchecker", "matplotlib", "nltk","lxml"
missing_libraries=[]

for lib in pip_lib:
        try:
            globals()[lib] = importlib.import_module(lib)
        except ModuleNotFoundError as error:
            missing_libraries.append(lib)

if missing_libraries==False:
    pass

else:
    with open ("app_resources/program_text_files/missing_lib.txt", mode="w", encoding="utf-8") as missing:
        for lib in missing_libraries:
            missing.write(lib+"\n")

#########################
# Importing custom files and modules
#########################

'''
A program-wide check is performed. 
The program can still be started if any of the necessary files are missing, 
but the program stability will be greatly compromised. 
'''

if os.path.exists("app_resources"):

        custom_text_files=[
            "program_text_files/program_description.txt"
        ]
        missing_text_files=list()

        # Text files
        for root in os.walk("app_resources/program_text_files"):
            for dir in root:
                if dir not in custom_text_files:
                    missing_text_files.append(dir)

        custom_training_files=[
            "program_text_files/program_description.txt"
        ]
        missing_training_files = list()

        # Training data files
        for root in os.walk("app_resources/app_test_data/app_training_data_test_files"):
            for dir in root:
                if dir not in custom_training_files:
                    missing_training_files.append(dir)

        custom_test_files=[
            "program_text_files/program_description.txt"
        ]
        missing_test_files = list()

        for root in os.walk("app_resources/app_test_data/app_test_data_test_files"):
            for dir in root:
                if dir not in custom_test_files:
                    missing_test_files.append(dir)

        # Compressed repository
        compressed_respostiory=os.path.exists("app_resources/compressed_language_data/cmr-88milsms-tei-v1.zip")
else:
    message="The app resource directory is either missing or has been renamed."
    continue_program(message)

#########################
# Custom modules
#########################
sys.path.append("app_resources")

from auxilary_functions import author_information, program_description, file_finder, program_end

#########################
# MainMaster check
#########################

core_files_available=True
missing_libraries=False

if core_files_available == True and missing_libraries==False:
    print("All libraries have been successfully loaded. The program will now start.")
else:
    message="An error has occured"
    continue_program(message)

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

def read_content(content):
    print(content)

#########################
# MainDocumentation
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
                    "end program": program_end
                    }

    while True:
            print()
            banner = "~ Teki - French Chat Analyzer ~ ", "#### Main Menu ####"
            for word in banner: print(word.center(50))
            for num, elem in enumerate(menu_option, start=1):
                print(f'{num}: {elem}')

            choice_str = input('\nPlease enter the number of your entry: ')

            #Executes the function as specified by the user via the number
            if choice_str.isdigit():
                choice_num = int(choice_str)
                if 0 < choice_num and choice_num <= len(menu_option):
                    func_list = list(menu_option.values())
                    function_number = choice_num - 1
                    func_name=str(func_list[function_number]).split()[1]

                    try:
                        #Executes functions that do not require arguments
                        func_list[function_number]()
                    except:

                        # Loads the file into  memory
                        if func_name  ==  "get_text":
                            doc=get_text(file_finder())

                        elif func_name == "read_content":
                            read_content(doc)

                else:
                    input("You have entered an incorrect number. You can return the menu by pressing the enter key.")

            else:
                input("Please enter the number, not the name of the entry.")


#########################
#Documentation Execution
#########################

if __name__ == "__main__":
    '''
    The main program will only run if all of the necessary files are available and if all of the main libraries have been installed. 
    This can be overridden by the user, but it is not advised as it can lead to the program becoming unstable.  
    '''
    if core_files_available==True and missing_libraries==False:
        run_program()