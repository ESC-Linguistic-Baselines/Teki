# -*- coding: utf-8 -*-

#########################
# 0 - Documentation description
#########################

'''
This program's function is to access the literate and oral nature of French chat data. 
'''

print("Please wait while libraries and files are being imported...")

#########################
# Importing standard python libraries
#########################
import importlib,zipfile


#########################
# Importing pip libraries
#########################
pip_libraries ="bs4","spacy","spellchecker","matplotlib"
missing_libraries=[]

for lib in pip_libraries:
        try:
            globals()[lib] = importlib.import_module(lib)
        except ModuleNotFoundError as error:
            missing_libraries.append(lib)

if missing_libraries==False:
    pass
else:
    with open ("app_ressources/program_text_files/missing_lib.txt", mode="w", encoding="utf-8") as missing:
        for lib in missing_libraries:
            missing.write(lib+"\n")


#########################
# Custom modules and files
#########################

from app_ressources.auxilary_functions import program_information

core_files_available=True
missing_libraries=False














#########################
# Main 0 - Documentation
#########################
def run_program():
    '''
    This is the main function of the program. It incorporates all other functions from this file
    as well as the from the secondary python file.
    It is executed under the if __name__
    '''
    menu_option = {"0 - Documentation information": program_information}
    while True:
         while True:
            print()
            banner = "~ Teki - French Chat Analyzer ~ ", "#### Main Menu ####"
            for word in banner: print(word.center(50))
            print("\n- The entry is not case sensitive- \n")
            for num, elem in enumerate(menu_option, start=1):
                print(f'{num}: {elem}')

            choice_str = input('\nPlease enter the number or the name of your entry: ').strip().lower()

            #Selects an option via the string
            if choice_str in menu_option:
                menu_option[choice_str]()

            #Selects an option via the number
            elif choice_str.isdigit():
                choice_num = int(choice_str)
                if 0 < choice_num and choice_num <= len(menu_option):
                         func_list = list(menu_option.values())
                         function_number = choice_num - 1

                         # Executes the function as specified by the user via the number
                         func_list[function_number]()
                else:
                    input("You have entered an incorrect number. You can return to the menu by pressing the enter key.")

            else:
                input("You have either entered an incorrect number or incorrect string. You can return the menu by pressing the enter key.")

#########################
# 0 - Documentation Execution
#########################

if __name__ == "__main__":
    '''
    The main program will only run if all of the necessary files are available and if all of the main libraries have been installed. 
    This can be overridden by the user, but it is not advised as it can lead to the program becoming unstable.  
    '''
    if core_files_available==True and missing_libraries==False:
        run_program()
