import bs4
document=r"C:\Users\chris\iCloudDrive\Documents\Academic Documents\RUB UNI\0 - Files\Lingustik PL\B.A\Bachleorarbeit\app_resources\app_dev\dev_files\ebayfr-e05p.xml"

with open(document, mode="r", encoding="utf-8") as file:
    soup = bs4.BeautifulSoup(file, "lxml")

    print(type(soup))


# Python3 code to explain
# the type() function

# Class of type dict
class DictType:
    DictNumber = {1: 'John', 2: 'Wick', 3: 'Barry', 4: 'Allen'}


# Class of type list
class ListType:
    ListNumber = [1, 2, 3, 4, 5]


# Creating object of each class
d = DictType()
l = ListType()

