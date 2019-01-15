import itertools

global debug
debug = True

global BINARY_OPERATORS
BINARY_OPERATORS = ['and', 'or', 'if', 'iff']
global UNARY_OPERATORS
UNARY_OPERATORS = ['not']

class Node:
        
    def __init_(self, s=""):
        self.stringRep = s
        self.left = None
        self.right = None

class Tree:
    
    def __init__(self, box=None, stringRep="", n=None):
        self.root = n
        self.box = box
        if box == None:
            self.stringRep = stringRep
        else:
            self.stringRep = box.get().strip()

    def getLeaves(self):
        leafs = []
        def _get_leaf_nodes(node):
            if node is not None:
                if node.left == None and node.right == None:
                    leafs.append(node.stringRep)
                _get_leaf_nodes(node.left)
                _get_leaf_nodes(node.right)
        _get_leaf_nodes(self.root)
        return set(leafs)

    def getOps(self):
        ops = []
        def _get_op_nodes(node):
            if node is not None:
                if node.left != None or node.right != None:
                    ops.append(node.stringRep)
                _get_op_nodes(node.left)
                _get_op_nodes(node.right)
        _get_op_nodes(self.root)
        return set(ops)


class TreeBuilder:

    
    @classmethod    
    def makeList(self, s):
        if debug:
            print "making list"
        l = s.split(' ')
        for i in xrange(len(l)):
            l[i] = l[i].split('(')
            for j in xrange(len(l[i])):
                if len(l[i][j]) == 0:
                    l[i][j] = '('
        chain = itertools.chain.from_iterable(l)
        l = list(chain)
        for i in xrange(len(l)):
            l[i] = l[i].split(')')
            for j in xrange(len(l[i])):
                if len(l[i][j]) == 0:
                    l[i][j] = ')'
        chain = itertools.chain.from_iterable(l)
        l = list(chain)
        if debug:
            print "list is:"
            print l
            print "done making list"
        return l
    
    
       
    @classmethod
    def BuildTree(self, box=None, s =""):
        if box != None:
            s = box
        if debug:
            print "building tree"
        tree = Tree(stringRep=s)
        l = self.makeList(s.strip())
        tree.root = self.getOperator(l)
        if debug:
            print "done building tree"
        return tree


    @classmethod
    def getOperator(self, l):
        if debug:
            print "print getting operator for:"
            print l
        p = 0
        for i in xrange(len(l)):
            if p == 0 and l[i] in BINARY_OPERATORS:
                n = Node()
                n.stringRep = l[i]
                n.left = self.getOperator(l[:i])
                n.right = self.getOperator(l[i+1:])
                return n
            if p == 0 and l[i] in UNARY_OPERATORS:
                n = Node()
                n.stringRep = l[i]
                n.left = None
                n.right = self.getOperator(l[i+1:])
                return n
            if l[i] == '(':
                p += 1
            if l[i] == ')':
                p -= 1
        if len(l) > 1:
            if p == 0 and l[0] == '(' and l[len(l)-1] == ')':
                return self.getOperator(l[1:-1])
        elif len(l) == 1:
            n = Node()
            n.stringRep = l[0]
            n.left = None
            n.right = None
            return n
        else:
            print "NO OPERATORS AT TOP LEVEL"
            return None