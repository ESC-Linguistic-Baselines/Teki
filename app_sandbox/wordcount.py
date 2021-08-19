import docx2txt
from datetime import datetime
import re

datetime_object = datetime.now()

#Loads the word document
doc=r"C:\Users\chris\Desktop\B.A\Teki\app_program_documentation\Chandler_Linguistik_B_A_Theisis_SoSe2021 V5.docx"
my_text = docx2txt.process(doc)

result = re.findall('\(.*?\)', my_text)
for i in result:
    print(i)