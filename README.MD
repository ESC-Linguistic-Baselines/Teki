# Téki:  A Naïve Bayesian French Discourse Analyzer

 ![Version Nubmer](https://img.shields.io/badge/Version-1.0.0-brightgreen)
 ![Project Size](https://img.shields.io/badge/Project_Size-25mb-yellow)
![Version Date](https://img.shields.io/badge/Last_Updated-August_2021-blue)
 [![License: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](https://opensource.org/licenses/MIT)

___
The name 'Teki' pronounced as /Tɛki/ comes from a literal transcription of the informal phrase  t'es qui' - 'Who are you'.
It is reminiscent of Stromae's 2013 song - Papoutai - Papa ou t'es - lit. Father, you are where?
It there contrasts with the more formal phrase "Qui es-tu". The spelling of the name is meant to represent this. 
This form of topicalization is actually quite common in French even if it is not necessarily exclusive to the language itself. 

The name was chose to reflect the process of researching the conceptual and medial representation of the French language. 
Message and intent are often communicated either through text or speech. However, these two only represent the medium of the language. 
The difference between the conceptual and medial representation of language is often overlooked when assessing language. 
The phrase "someone writes how they speak" reflects this mentality. The train of thought is translated into a written medium, but
the words actually reflect a stream of consciousness if you will. 

Teki is a naive Bayesian classifier that is used to tag French chat data according to their literacy and orality. 
Since there was no training data available for the naive bayes, a scoring system was developped that tagged sentences according to 
their literacy and orality. Then, using this newly acquiered training data, the naive bayes was trained so that it could decide 
if a sentence was literal or oral. 

For more information on this topic, please consult the documentation  
 
## Academic Formalities
Information  | Description
------------- | -------------
Name | Christopher Michael Chandler
Matrikelnummer | 108017107247
 Erstfach | Linguistik B.A, 6. Semester
Zweitfach | Romanische Philologie Franzoesisch B.A, 9. Semester
Titel  | From T’es Qui to Qui Es-Tu: A Naïve Bayesian Approach to Assessing Literate and Oral Discourse in Nonstandard French Language Data
Kurs   | Schriftliche Hausarbeit für die Bachelorprüfung der Fakultät für Philologie an der Ruhr-Universität Bochum (Gemeinsame Prüfungsordnung für das Bachelor/Master-Studium im Rahmen des 2-Fach-Modells an der RUB vom 03. November 2016)
___

# License 
MIT License

Copyright (c) 2021 Christopher Chandler

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
_____

# Inspiration
The layout of this program is partly inspired by a project that I did with a partner in the summer semester of 2021. 
The inspiration is limited to the dynamic menu system that is sued within this program.  


# Requirements 

## Python Version
This program was created and designed with **python 3.9.6** in mind. Therefore, that is the recommended version for teki. 
It is possible to run the program using any version **above 3.6**, but program stability cannot be guaranteed. 
You can download the latest python version [ here](https://www.python.org/downloads/).  

## Pip Modules

The following pip packages must be installed in order for the program to run properly:

```
bs4>=0.0.1
beautifulsoup4>=4.9.3
nltk>=3.5
lxml>=4.6.1
pandas~=1.1.5
sklearn~=0.0
scikit-learn~=0.24.2
spacy>=2.3.5
```

There are three ways to install the *requirements.txt* file:

* 1) Install all modules individually via pip.
<br><br>
* 2) install all modules with pip using the requirements.txt without specifying the version number:
```
pip install -r requirements.txt
```
<br>

* 3) install with pip using the requirements.txt with specifying the version number:
```
pip3.9 install -r requirements.txt
```

<br>
Additionally, the following for spacy must also be installed separately:

```
python -m spacy download fr_core_news_sm
```

# Program

When starting the program, a check is performed to ensure that the directory **app_program_resources** and its files are all present. These files should not be changed in anyway. If you decide to add databases or corpora to this program, they should be placed in **app_user_resources**.


Once the modules, files and libraries, have been successfully loaded, then you will be greeted with the following a menu system:

```
1: load .XML or .TXT file
2: load training file
3: analyze contents
4: document classification
5: clear error log file
6: restore default database
7: evaluation
8: about program
9: end program
```

This is a dynmaic menu to which you can return. Should an error arise in the program, you will automatically be returned to this menu. 


#  load .XML or .TXT file


