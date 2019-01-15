from Tkinter import *
from treestuff import *


class AxiomFrame:
    def __init__(self, tree=None, frame=None, headEnt=None):
        self.tree = tree
        self.frame = frame
        self.headEnt = headEnt
        self.cells = []

    def addRow(self):
        ent = Entry(self.frame, font=("Arial", 6), width=30)
        ent.pack(side=TOP, padx=5, anchor=N)
        self.cells.append(ent)

class RefFrame:
    def __init__(self, left=None, right=None, op=None, operator=None):
        self.leftFrame = left
        self.left = None
        if left != None:
            self.left = []
        self.rightFrame = right
        self.right = []
        self.opFrame = op
        self.op = []
        self.width = 3
        self.operator = operator

    def addRow(self):
        if self.leftFrame != None:
            ent = Entry(self.leftFrame, width=self.width, font=("Arial", 10))
            ent.pack(side=TOP)
            self.left.append(ent)
        
        ent = Entry(self.rightFrame, width=self.width, font=("Arial", 10))
        ent.pack(side=TOP)
        self.right.append(ent)
        
        but = Button(self.opFrame, width=self.width, pady=0, height=1, borderwidth=0.5, font=("Arial", 8))
        but.pack(side=TOP)
        self.op.append(but)






global ALPHABET
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
global CP
CP = ['green', 'yellow', 'red', 'blue', 'orange']
class Controller:
    def __init__(self, refFrame, headFrame):
        self.frames = []
        self.varTable = []
        self.refFrame = refFrame
        self.refFrames = []
        self.headFrame = headFrame
        self.numVars = 0

    def addFrame(self, frame, text):
        
        ent = Entry(frame, width=20)
        ent.insert(0, text)
        ent.pack(side=TOP, padx=5, anchor=N)
        ent.configure(state='disabled', justify='center')
        tree = TreeBuilder.BuildTree(box=text)
        self.frames.append(AxiomFrame(tree, frame, ent))



    def generate(self, n):
        if debug:
            print "making table"
        vrs = []
        ops = []

        #extract operators and terminal values from the tree
        for frame in self.frames:
            s = frame.tree.getLeaves()
            op = frame.tree.getOps()
            for i in s:
                vrs.append(i)
            for i in op:
                ops.append(i)

        #make sets to remove duplicates
        vrs = set(vrs)
        ops = set(ops)
        self.numVars = n
        #set numbers
        numVars = len(vrs)
        numAxioms = len(self.frames)
        numRefs = len(ops)
        numCols = pow(n, numVars)


        #initialize tables
        for vr in vrs:
            self.varTable.append([vr, ['_'] * numCols])
        for frame in self.frames:
            for i in xrange(0, numCols):
                frame.addRow()
                i += 1

        w = 5
        for op in ops:
            fr = None
            if op != "not":
                #LEFT
                fr = Frame(self.refFrame)
                fr.pack(side=LEFT, anchor=N)
                ent = Entry(fr, width=w)
                ent.pack(side=TOP)
                ent.configure(justify='center')
                ent.insert(0, "left")

            #RIGHT
            fr1 = Frame(self.refFrame)
            fr1.pack(side=LEFT, anchor=N)
            ent = Entry(fr1, width=w)
            ent.insert(0, "right")
            ent.pack(side=TOP)
            ent.configure(justify='center')

            #OP
            fr2 = Frame(self.refFrame)
            fr2.pack(side=LEFT, anchor=N)
            ent = Entry(fr2, width=w)
            ent.insert(0, op)
            ent.pack(side=TOP)
            ent.configure(justify='center')
            temp = RefFrame(fr, fr1, fr2, op)
            if op != "not":
                for i in xrange(0, pow(n, 2)):
                    temp.addRow()
            else:
                for i in xrange(0, n):
                    temp.addRow()
            self.refFrames.append(temp)


    def initVarCols(self):
        for i in xrange(len(self.varTable)):
            cur = 0
            for j in xrange(len(self.varTable[i][1])):
                #self.varTable[i][j][1]
                cur = int(j/pow(self.numVars, len(self.varTable)-1-i)) % self.numVars
                self.varTable[i][1][j] = ALPHABET[cur]

        for i in self.varTable:
            print i


    def initRefCols(self):
        for frame in self.refFrames:
            cur = 0
            if frame.left != None:
                for i in xrange(len(frame.left)):
                    cur = int(i/self.numVars)
                    frame.left[i].insert(0, ALPHABET[cur])
                cur = 0
                for i in xrange(len(frame.right)):
                    cur = i % self.numVars
                    frame.right[i].insert(0, ALPHABET[cur])
                cur = 0
                for i in xrange(len(frame.op)):
                    frame.op[i]["text"] = ALPHABET[cur]
                    frame.op[i]["bg"] = CP[cur]
                    self.setButtonClick(frame.op[i])
            else:
                for i in xrange(len(frame.right)):
                    frame.right[i].insert(0, ALPHABET[cur])
                    cur += 1
                cur = len(frame.op) - 1
                for i in xrange(len(frame.op)):
                    frame.op[i]["text"] = ALPHABET[cur]
                    frame.op[i]["bg"] = CP[cur]
                    self.setButtonClick(frame.op[i])
                    cur -= 1

    def update(self):
        #FOR EACH ROW IN VARIABLE TABLE
        for i in xrange(len(self.varTable[0][1])):
            #MAKE DICTIONARY OF VARIABLE VALUES FOR EASY LOOK UP
            vars = {}
            for var in self.varTable:
                vars[var[0]] = var[1][i]
            #FOR EACH AXIOM, EXAMINE TREE
            for fr in xrange(len(self.frames)):
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
                        for frame in self.refFrames:
                            if frame.operator == node.stringRep:
                                for i in xrange(len(frame.right)):
                                    if frame.right[i].get() == rightChild:
                                        if frame.left != None:
                                            if frame.left[i].get() == leftChild:
                                                return frame.op[i]["text"]
                                        else:
                                            return frame.op[i]["text"]
                self.frames[fr].cells[i].delete(0, END)
                temp = setValue(self.frames[fr].tree.root)
                self.frames[fr].cells[i].insert(0, temp)
                for c in xrange(len(ALPHABET)):
                    if ALPHABET[c] == temp:
                        self.frames[fr].cells[i]["bg"] = CP[c]


    def setButtonClick(self, b):
        b["command"] =lambda: self.buttonClick(b)

    def buttonClick(self, but):
        print but["text"]
        cur = 0
        for i in xrange(len(ALPHABET)):
            if but["text"] == ALPHABET[i]:
                cur = i
        cur += 1
        if cur % self.numVars == 0:
            cur = 0

        but["text"] = ALPHABET[cur]
        but["bg"] = CP[cur]
        self.update()




