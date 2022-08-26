import random
import sys
import os
# m files
# min p nodes
# n level
# modularize
 
def generateChild(first,minNodes,level):
    while random.randint(0, 1) or first ==True or level >0 or minNodes>0:
        first = False
        level = level -1
        minNodes =minNodes -1
        d = {"Name": str(random.randint(0, 20)),"BirthYear":str(random.randint(1500, 3000)) ,"DeathYear": str(random.randint(1500, 3000))}
        child = generateChild(False,minNodes,level)
        if len(child) > 0:
            if "Members" in d:
                d["Members"] = d["Members"]+  [child]
            else:
                d["Members"] = [child]
        return d
    else:
        return []
    
def generateLineage(fileCount,dir, minNodes,level):
    for i in range(fileCount):
        f = open(dir+"/"+str(i)+".json","w+")
        data = {"lineage": {"FamilyTree": str("Some Family Tree "+str(i))}}
        data["lineage"]["Members"] = [generateChild(True, minNodes,level)]
        print(data)
        f.write(str(data))

def performValidations():
    if len(sys.argv) != 5:
        print("The number of arguments passed is not correct.Kindly check and retry")
        return False
    try:
        n,m,l = int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
        if n<=0 or m<=0 or l<=0:
            raise Exception
    except:
        print("Something went wrong.The program is expecting the 1st, 2nd  and 3rd argumets to be +ve int type.Kindly check")
        return False
    if not os.path.isdir(sys.argv[4]):
        print("The path defined for storing the files does not exist. Kindly check")
        return False
    return True

def help():
    print("The program takes 4 arguments:")
    print("1. The number of lineage files to be generated")
    print("2. Number of min nodes/members to present in the lineage")
    print("3. The level: atleast one family will be there of same length")
    print("4. path, where the created lineage will be saved")

if __name__ == '__main__':
    n = len(sys.argv)
    if not performValidations():
        print("calling Help...")
        help()
        exit()
    print("Total arguments passed:", n)
     
    # Arguments passed
    print("\nName of Python script:", sys.argv[0])
     
    print("\nArguments passed:", end = " ")

    for i in range(1, n):
        print(sys.argv[i], end = " ")
    print()
    #performValidations()
    fileCount = int(sys.argv[1])

    minNodes = int(sys.argv[2])
    level = int(sys.argv[3])
    path = sys.argv[4]

    generateLineage(fileCount,path, minNodes,level)

