import numpy as np
from BTreeNode import BTreeNode
class BTreeFile:
    def __init__(self, FamilyTree,file):
        self.root = BTreeNode(FamilyTree)
        self.lineageStartDate = -1
        self.lineageEndDate = -1
        self.shortestLived = ("",0)
        self.longestLived = ("",0)
        self.shortestGenerationNo = -1
        self.longestGenerationNo = -1
        self.file = open(file,"w+")

    #Write the whole family tree(members) in a file
    def printTree(self, x, l=0):
        # at which level the node/member belongs to
        self.file.write("\nAt Level "+ str(l)+ " ")#,  end=":")
        count = 1
        #write the details in a file
        self.file.write(x.Name)
        self.file.write("\n Childs  = ")#,end = " ")
        #find the childs
        for i in x.keys:
            self.file.write(i+ " ")
        self.file.write("\n")
        l =l+ 1
        #iterate through the childs and keep getting lineages
        if len(x.child) > 0:
            for i in x.child:
                count = count +self.printTree(i, l)
        return count

    
    #crete tree from scratch, when there is no member present    
    def createTree(self,tree):
        self.createTreeFromJson(tree,self.root)
        
    #create various generations, keep ading nodes/child to a perticular parent
    def createTreeFromJson(self,members,parent=None):
        #if no child
        if len(members) ==0:
            return 0
            #createTreeFromJson(members,self.root)
        else:
            #iterate ver the childs
            for i in members:
                addedMember = self.insert_key(i,parent)
                # if th
                if "Members" in i and addedMember != None:
                    self.createTreeFromJson(i["Members"],addedMember)
                elif addedMember != None:
                    addedMember.leaf = True
                    if addedMember.deathYear> self.lineageEndDate:
                        self.lineageEndDate = addedMember.deathYear
                    if addedMember.birthYear < self.lineageStartDate or self.lineageStartDate ==-1:
                        self.lineageStartDate = addedMember.birthYear
                    self.setShortestLngestLived(addedMember)
                    self.setGenerationNo(addedMember)
    
    # getter menthod for getting shortest and longest lived
    def getShortestLngestLived(self):
        self.file.write("\n ============================")
        self.file.write("\n i) Who lived longest (name and age) in this lineage?  Who died the younges")
        self.file.write("\nshortest lived with age = "+str(self.shortestLived))
        self.file.write("\nLongest Lived with age = "+str(self.longestLived))
    
    # setter menthod for shortest and longest lived
    def setShortestLngestLived(self,addedMember):
        if self.shortestLived[0] == "" or self.shortestLived[1] > addedMember.age:
            self.shortestLived = (addedMember.Name,addedMember.age)
        if self.longestLived[0] == "" or self.shortestLived[1] < addedMember.age:
            self.longestLived = (addedMember.Name,addedMember.age)
        #self.longestLived = ("",0)

    # setter menthod for shortest and longest genrations count
    def setGenerationNo(self,addedMember):
        if self.shortestGenerationNo == -1 or self.shortestGenerationNo > addedMember.generationNo:
            self.shortestGenerationNo = addedMember.generationNo
        if self.longestGenerationNo == -1 or self.longestGenerationNo < addedMember.generationNo:
            self.longestGenerationNo = addedMember.generationNo
        #self.longestLived = ("",0)
    
    #validations to be performed
    def performValidations(self,member,parent):
        #check if same name child is already present
        if member['Name'] in parent.keys:
            self.file.write("\n not taking"+member['Name']+ " as 2 siblings can't have same name")
            return False
        #check if age >=0 or not
        if int(member['DeathYear']) -int(member['BirthYear']) <=0:
            self.file.write("\n not taking"+member['Name']+ " as age can't be -ve or zero")
            return False
        #one more validation of parent should be born befor child is done on insert_key
        if int(parent.birthYear) -int(member['BirthYear']) >0:
            self.file.write("\n not taking"+member['Name']+ " as parent should be born before the child")
            return False
        return True
    
    #insert the child to the parents 
    def insert_key(self,member,parent):
        #Perform Validations
        if not self.performValidations(member,parent):
            return None
        
        #cretae new node
        newMember = BTreeNode(member['Name'],member['BirthYear'],member['DeathYear'],parent.generationNo+1)        
        i = len(parent.keys) - 1
        parent.child.append(newMember)
        parent.keys.append("")
        #parent.child.append(None)
        #validatig the child should be born after the parent
        while i >= 0 and newMember.birthYear < parent.child[i].birthYear:
            parent.child[i + 1] = parent.child[i]
            i -= 1
        parent.child[i + 1] = newMember
        parent.keys[i + 1] = newMember.Name        
        return newMember
    
    # the period i.e ehnr first member was borned to death of last member
    def getLinaegeActivePeriod(self):
        self.file.write("\n ============================")
        self.file.write("\n e) The range of period this lineage was active - ie., first ancestor birth year to the death year last member:")
        self.file.write("\n from  "+str(self.lineageStartDate)+" to "+str(self.lineageEndDate)+ "total = "+ str(self.lineageEndDate - self.lineageStartDate))
        return self.lineageEndDate - self.lineageStartDate
    
    # get Ages of all Members
    def getAges(self, parent = None, age = []):
        if parent ==None:
            parent =self.root
        age = [(parent.age,parent.Name)]
        if len(parent.child) > 0:
            for i in parent.child:
                age =age +self.getAges(i, age)
        return age

    #print all the ages of members in the lineage
    def printAges(self):
        self.file.write("\n==============")
        self.file.write("\nc) Print all family members and their age\n")
        self.file.write(str(self.getAges()[1:]))

    
    #/* Insert non full condition */
    def insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append((None, None))
            while i >= 0 and k[0] < x.keys[i][0]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k[0] < x.keys[i][0]:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self.split(x, i)
                if k[0] > x.keys[i][0]:
                    i += 1
            self.insert_non_full(x.child[i], k)

    def getMeanAges(self):
        ages = self.getAges()
        self.file.write("\n=======")
        mean =sum(i for i, j in ages)/len(ages)
        self.file.write("\n f)Mean age for this lineage= "+str(mean))        
        return mean
    
    # get all the members f the lineage in sorted order of their age
    def getSortedAges(self,printInFile = True):
        ages = sorted(self.getAges(),key=lambda x: x[0])[1:]
        if printInFile:
            self.file.write("\n=======")
            self.file.write("\nd) Order age of family members in ascending order\n")
        
            self.file.write(str(ages))
        return ages
    
    #find median age of all members 
    def getMedianAge(self):
        ages = self.getSortedAges(False)[1:]
        # if odd number of members
        if len(ages)%2 != 0:
            median= ages[int(len(ages)-1/2)][0]
        else:
            #if even number of members
            if int(int(len(ages)+1)/2)< len(ages)and int((len(ages)-1)/2)<len(ages):
                median = (ages[int(int(len(ages)+1)/2)][0]+ages[int((len(ages)-1)/2)][0])/2
            else:
                #if only one person in family
                if len(ages) == 1:
                    median = ages[0]
                
                else:
                    #in case no member id present in the lineage
                    #can occur in the case, if the first member itself is invalid
                    median =-1
        self.file.write("\n ============================")
        self.file.write("\n g) Find the median age for this lineage="+str(median))
        return median
    
    #calculate getIQRMiddle50 and get middle 50% of mambers
    def getIQRMiddle50(self):
        self.file.write("\n ============================")
        self.file.write("\nh) Group and print middle 50% of members (name and age) of this lineage using IQR (Interquartile Range) ")
        #calculate interquartile range 
        sortedAgesNames= self.getSortedAges(False)[1:]
        if len(sortedAgesNames) ==0:
            return
        sortedAges = [i[0] for i in sortedAgesNames]
        q3, q1 = np.percentile(np.array(sortedAges), [75 ,25])
        self.file.write("\n iqr="+str(q3-q1))
        self.file.write("\n middle elemnts are:")
        for i in sortedAgesNames:
            if i[0] < q3 and i[0]>q1:
                self.file.write("\n"+str(i))
    
    #function to find all the linages
    def getAllFamilyLines(self):
        self.file.write("\n ============================")
        self.file.write("\n b)The various family lines are as follows:\n")
        shortest = -1
        longest =-1
        shortest_index = -1
        longest_index =-1
        linages = self.getDecendents(self.root)
        print("All Linages are as follows:")
        print(self.longestGenerationNo,self.shortestGenerationNo)
        #print all family lines
        for i in linages:
            i = i[1:]
            #check if longest
            if len(i) == self.longestGenerationNo:
                print("The below is longest(or one of the longest) lineage")
                print(i)
            #written like this, so that can handle the case where shortest = longest
            else:
                #check if shortest
                if len(i) == self.shortestGenerationNo:
                    print("The below is shortest(or one of the shortest) lineage")
                    print(i)
                else:
                    #print("nothing")
                    print(i)

    #functin will return list of all family lines started/originated from x
    def getDecendents(self,x):
        currentlLineage = []
        if x.leaf == True:
            return [[x.Name]]
        else:
            for i in x.child:
                childLineages = self.getDecendents(i)
                for y in childLineages:
                    currentlLineage = currentlLineage + [[x.Name] + y]
            return currentlLineage  


        

