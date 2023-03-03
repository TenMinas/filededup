import os
import shutil
import csv
import datetime
from datetime import datetime
import yaml


###################################################################################################
###################################################################################################
def getlistdata(yaml_config, ind):
    paramlist = []
    tempind = yaml_config[ind]
    if type(tempind) == list:
        paramindex = len(tempind)
        for pi in range(paramindex):
            paramlist.append(tempind[pi])

    return(paramlist)
###################################################################################################
###################################################################################################
def hash_calc(file):
    import hashlib

    f = open(file, "rb")
    data = f.read()
    hash_value = hashlib.sha256(data).hexdigest()
    return(hash_value)

###################################################################################################
###################################################################################################
def get_config(path_config):


    with open(path_config, 'r') as f:
        fdd_config = yaml.safe_load(f)

    dir_list_a = getlistdata(fdd_config, "dir_list_a")
    dir_list_b = getlistdata(fdd_config, "dir_list_b")
    fdd_results_path = fdd_config["fdd_results"]

    pathdict = {"dir_list_a" : dir_list_a, "dir_list_b" : dir_list_b, "fdd_results_path" : fdd_results_path}

    return(pathdict)
###################################################################################################
###################################################################################################
def build_filedict(dir_list):
    import os
    filedict = {}
    filedict.update({"fnum" : 0})
    for d in range(len(dir_list)):
        dir_temp = dir_list[d]

        for root, dirs, files in os.walk(dir_temp):
            for fname in files:
                filePath = root + "/" + fname
                los = (os.stat(filePath))
                h = hash_calc(filePath)

                filedict.update({filedict["fnum"] : {"full_file_path" : filePath, "path_wo_fname" : root, "fname" : fname, "last_update" : los.st_mtime, "size" : los.st_size, "hash" : h}})
                filedict["fnum"] +=1
    return(filedict)

###################################################################################################
###################################################################################################


###################################################################################################
###################################################################################################
def fcompare(filedicta, filedictb):
    fcresults_same = []
    fcresults_same.append(["KEEP FILE PATH", "DUPLICATE FILE PATH"])
    fcresults_unique = []
    fcresults_unique.append(["UNIQUE FILE PATH"])

    for a in range(filedicta["fnum"]):
        aval = filedicta.get(a)
        ahash = aval["hash"]

        for b in range(filedictb["fnum"]):
            bval = filedictb.get(b)
            bhash = bval["hash"]

            if ahash == bhash:
    # Not sure I understand why it is looking for files with different "full_file_path"
    # Should have done the comment earlier
                if filedicta[a]["full_file_path"] != filedictb[b]["full_file_path"]:
                    fcresults_same.append([filedicta[a]["full_file_path"], filedictb[b]["full_file_path"]])


    for b in range(filedictb["fnum"]):
        in_list = False
        # c = 1
        # while c < (len(fcresults_same)):
        for c in range(len(fcresults_same)):
            b_file = filedictb.get(b)
            b_ffp = b_file.get("full_file_path")
            c_same = fcresults_same[c][1]
            if b_ffp == c_same:
                in_list = True
                break
            # c +=1

        if not in_list:
            fcresults_unique.append([b_ffp])

    return(fcresults_same, fcresults_unique)



###################################################################################################
###################################################################################################

def savedata(filePath, sym, data):

    dtstr = (datetime.now()).strftime('%Y.%m.%d--%H.%M.%S')
    fname = filePath + "/" + "FC" + " - " + sym + " - " + dtstr + ".csv"
    with open(fname, 'w+') as f: 
        write = csv.writer(f)
        write.writerows(data) 


###################################################################################################
###################################################################################################
### Main code

# getFileList from fdd_config.yaml
path_config = "/home/gary/coding/filededup/fdd_config.yaml"
pathdict = get_config(path_config)
dir_list_a = pathdict["dir_list_a"]
dir_list_b = pathdict["dir_list_b"]
fdd_results_path = pathdict["fdd_results_path"]

print("-- 1. Building list 'A' file dictionary")
filedicta = build_filedict(dir_list_a)
# print(filedicta)

print("-- 2. Building list 'B' file dictionary")
filedictb = build_filedict(dir_list_b)
# print(filedictb)

print("-- 3. Comparing the file dictionaries")
fcresults = fcompare(filedicta, filedictb)
if len(fcresults[0]) <= 1:
    fcresults[0].append(["none", "none"])

if len(fcresults[1]) <= 1:
    fcresults[1].append(["none"])

print("-- 4. Saving the results")
savedata(fdd_results_path, "S", fcresults[0])
savedata(fdd_results_path, "U", fcresults[1])
print("-- !!  DONE  !!")



###################################################################################################
###################################################################################################


###################################################################################################
###################################################################################################

