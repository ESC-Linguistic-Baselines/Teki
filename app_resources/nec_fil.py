import os,json
#Gen
doc=os.listdir(os.getcwd()+"\\app_docs")
dev= os.listdir(os.getcwd()+"\\app_dev\\dev_files")
test=os.listdir(os.getcwd()+"\\app_test\\test_files")
compressed=os.listdir(os.getcwd()+"\\compressed_data")


files={"docs":doc,
       "dev":dev,
       "test":test,
       "compressed":compressed}

out=r"C:\Users\chris\iCloudDrive\Desktop\CodingProjects\Github\Bachleorarbeit\app_resource_files.json"
out_file = open(out, "w+")

json.dump(files,out_file,indent = 2)

print("updated")
