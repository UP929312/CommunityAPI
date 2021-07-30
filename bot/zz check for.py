import os

find = "MASTER_ITEM_DICT.json"

folders = [f.path for f in os.scandir("./") if f.is_dir()]

def find_it(folder, ext):
    for file in folder:
        if file.endswith(".py") and file != "zz check for.py":
            with open(ext+file, "r", encoding="utf-8") as a:
                try:
                    for line in a.readlines():
                        if find in line:
                            print(file, " contained "+find)
                except Exception as e:
                    print(e)
                    pass

for folder in folders:
    if folder == "":
        find_it(os.listdir(), "")
    else:
        find_it(os.listdir(folder), folder+"/")
