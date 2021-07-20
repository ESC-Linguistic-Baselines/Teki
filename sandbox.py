import os

def missing_files(file_list,path):
    missing = list()

    # Text files
    for root in os.listdir(path):
            if root not in app_text_files:
                missing.append(root)
    if missing:
        return  missing
    else:
        return False

app_text_files = [
    "app_docs/program_description.txt",
    "program_description.txt",
    "author_information.json",
    "missing_lib.txt"
]
missing_text_files = missing_files(app_text_files,"app_resources/program_text_files")

print(missing_text_files)