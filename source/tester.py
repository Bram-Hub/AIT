from treestuff import *


class Ref:
    def __init__(self, op, vPair, value):
        self.op = op
        self.vPair = vPair
        self.value = value


class Table:

    def __init__(self, trees=[], varTable=[], numVars=0, axiomTable=[], numAxioms=0, refTable=[], numRefs=0):
        self.varTable = varTable
        self.numVars = numVars
        self.axiomTable = axiomTable
        self.numAxioms = numAxioms
        self.refTable = refTable
        self.numRefs = numRefs
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
        self.trees = trees


    def makeTableFromTrees(self, trees):
        self.trees = trees
        if debug:
            print "making table"
        vrs = []
        ops = []

        #extract operators and terminal values from the tree
        for tree in trees:
            s = tree.getLeaves()
            op = tree.getOps()
            for i in s:
                vrs.append(i)
            for i in op:
                ops.append(i)

        #make sets to remove duplicates
        vrs = set(vrs)
        ops = set(ops)

        #set numbers
        self.numVars = len(vrs)
        self.numAxioms = len(trees)
        self.numRefs = len(ops)
        numCols = pow(self.numVars, self.numVars)

        #initialize tables
        for vr in vrs:
            self.varTable.append([vr, ['_'] * numCols])
        for tree in trees:
            self.axiomTable.append([tree.stringRep, [''] * numCols])
        if debug:
            print "table has " + str(numCols) + "rows"
        for op in ops:
            if op != "not":
                self.refTable.append([["left", [''] * pow(self.numVars, 2)],
                    ["right", [''] * pow(self.numVars, 2)],
                    [op, [''] * pow(self.numVars, 2)]])
            else:
                self.refTable.append([["right", [''] * self.numVars],
                    ["not", [''] * self.numVars]])


    def initRefCols(self):
        
        for table in self.refTable:
            cur = 0
            if len(table) == 3:
                for j in xrange(len(table[0][1])):
                    #self.varTable[i][j][1]
                    cur = int(j/self.numVars)
                    table[0][1][j] = self.alphabet[cur]
                cur = 0
                for j in xrange(len(table[1][1])):
                    #self.varTable[i][j][1]
                    cur = j % self.numVars
                    table[1][1][j] = self.alphabet[cur]
                cur = 0
                for i in xrange(len(table[2][1])):
                    table[2][1][i] = self.alphabet[cur]
            else:
                for i in xrange(len(table[0][1])):
                    table[0][1][i] = self.alphabet[cur]
                    cur += 1
                cur = self.numVars-1
                for i in xrange(len(table[1][1])):
                    table[1][1][i] = self.alphabet[cur]
                    cur -= 1

    def initVarCols(self):
        for i in xrange(len(self.varTable)):
            cur = 0
            for j in xrange(len(self.varTable[i][1])):
                #self.varTable[i][j][1]
                cur = int(j/pow(self.numVars, self.numVars-1-i)) % self.numVars
                self.varTable[i][1][j] = self.alphabet[cur]

    def printTable(self):
        print "VARS"
        for row in self.varTable:
            print row
        print "AXIOMS"
        for row in self.axiomTable:
            print row
        print "REFS"
        for row in self.refTable:
            print row

    def makePairs(self, v):
        pairs = []
        keys = []
        for i in v:
            keys.append(i)
        for i in xrange(len(keys)):
            for j in xrange(i, len(keys)):
                pairs.append((keys[i], keys[j]))
        return pairs

    def update(self):
        #FOR EACH ROW IN VARIABLE TABLE
        for i in xrange(len(self.varTable[0][1])):
            #MAKE DICTIONARY OF VARIABLE VALUES FOR EASY LOOK UP
            vars = {}
            for var in self.varTable:
                vars[var[0]] = var[1][i]
            #FOR EACH AXIOM, EXAMINE TREE
            for tree in xrange(len(self.trees)):
                #DEFINE RECURSIVE FUNCTION
                def setValue(node):
                    #IF NOT LEAF GET VALUES OF LEFT/RIGHT
                    #IF LEAF RETURN VALUE FROM DICTIONARY
                    if node.left != None:
                        leftChild = setValue(node.left)
                    if node.right != None:
                        rightChild = setValue(node.right)
                    if node.left == None and node.right == None:
                        return vars[node.stringRep]
                    else:
                        #LOOK FOR APPROPRIATE REF TABLE FOR NODE
                        for table in self.refTable:
                            if len(table) > 2:
                                if table[2][0] == node.stringRep:
                                    #IF FOUND LOOK FOR CORRECT ROW OF REF TABLE
                                    for j in xrange(len(table[0][1])):
                                        if table[0][1][j] == leftChild:
                                            if table[1][1][j] == rightChild:
                                                return table[2][1][j]
                            else:
                                if table[1][0] == node.stringRep:
                                    for j in xrange(len(table[0][1])):
                                        if table[1][0] in UNARY_OPERATORS:
                                            if table[0][1][j] == rightChild:
                                                return table[1][1][j]

                self.axiomTable[tree][1][i] = setValue(self.trees[tree].root)



if __name__ == '__main__':
    trs = []
    while True:
        c = raw_input("enter some shit\n")
        if c == "make":
            table = Table()
            table.makeTableFromTrees(trs)
            table.initRefCols()
            table.initVarCols()
            table.update()
            table.printTable()
            trs = []
        else:
            tree = TreeBuilder.BuildTree(c.strip())
            trs.append(tree)
            