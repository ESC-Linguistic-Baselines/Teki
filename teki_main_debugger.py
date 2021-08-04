import os, csv
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

words = list()
file = get_text(r"app_resources/app_common_default_docs/validation_data.csv")

for sentence in file:
    for word in sentence[0].split():
        words.append(word)

print(words)