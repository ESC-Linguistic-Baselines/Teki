import os
import sys
app_user_resources = f"{os.getcwd()}/app_user_resources"

path = os.getcwd()+"/app_user_resources/sentence_results"
print(os.path.exists(path))

# FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\chris\\Desktop\\Bachleorarbeit/app_user_resources/sentence_result/manual_feat_selection_06_08_2021_20_44_23.csv'