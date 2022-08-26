
class BTreeNode:
    def __init__(self,Name,birthYear=0,deathYear=0,generationNo=0, leaf=False):
        self.leaf = leaf
        self.Name = Name
        self.birthYear = int(birthYear)
        self.deathYear = int(deathYear)
        self.age = self.deathYear-self.birthYear
        self.keys = []
        self.child = []
        self.generationNo = generationNo
