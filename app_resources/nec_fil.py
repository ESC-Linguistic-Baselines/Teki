import os,json

dev= os.listdir(os.getcwd()+"\\app_dev\\dev_files")
test=os.listdir(os.getcwd()+"\\app_test\\test_files")
compressed=os.listdir(os.getcwd()+"\\compressed_data")
files={"dev":dev,
       "test":test,
       "compressed":compressed}

out=r"C:\Users\chris\iCloudDrive\Documents\Academic Documents\RUB UNI\0 - Files\Lingustik PL\B.A\Bachleorarbeit\req_files.json"
out_file = open(out, "w+")

json.dump(files,out_file,indent = 2)


