import os
import concurrent.futures
import json
from BTreeFile import BTreeFile

#actual work to be done or the operations to be performed on the BTree
def performperations(filename,inputDirectory,outputDirectory):
    print("processing file:", filename)
    f = open(inputDirectory+"/"+filename, "r")
    x  = f.read()
    #file  = open(outputDirectory+"/"+filename.split(".")[0]+".txt","w+")
    # load the json file
    tree = json.loads(x.replace("'","\""))
    print("the file to be created as output")
    print("out = ",outputDirectory+"/"+filename.split(".")[0]+".txt")
    B = BTreeFile(tree["lineage"]["FamilyTree"],outputDirectory+"/"+filename.split(".")[0]+".txt")
    B.createTree(tree["lineage"]["Members"])
    B.printTree(B.root)
    B.getAllFamilyLines()
    B.printAges()
    B.getSortedAges()
    B.getLinaegeActivePeriod()
    B.getMeanAges()
    B.getMedianAge()
    B.getIQRMiddle50()
    B.getShortestLngestLived()

#function used for making multi-threaded call 
def performUsingThread(threadPoolSize):
    # ask user to insert input and ouput directory
    inputDirectory = input("enter input directory : ")
    outputDirectory = input("enter output directory : ")
    # validating directory
    if not os.path.isdir(inputDirectory) or  not os.path.isdir(inputDirectory):
        print("either the input or ouput directory doesn't exist ")
        exit()
    #using multi-threading: give each file to a perticular thread
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for filename in os.listdir(inputDirectory):
            if filename.endswith(".json"):
                futures.append(executor.submit(performperations, filename,inputDirectory,outputDirectory))
        for future in concurrent.futures.as_completed(futures):
            future.result()


if __name__ == '__main__':
    threadCount = input("enter number of threads to be used : ")
    try:
        threadCount = int(threadCount)
    except:
        print("threadCount should be a number")
        exit()
    if threadCount <=0:
        print("threadCount should be >=0")
        exit()
    performUsingThread(threadCount)