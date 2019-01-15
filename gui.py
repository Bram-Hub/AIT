from Tkinter import *
from tester import *

class GUI:
	def __init__(self, master, trees=[]):
		self.master = master
		self.trees = trees
		master.title = "AIT GUI"
		master.minsize(width=600, height=600)

		self.headFrame = Frame(master)
		self.headFrame.pack(side=TOP)

		genButton = Button(self.headFrame, text="Generate Tables")
		genButton.pack(side=RIGHT)
		genButton.bind("<Button-1>", self.genTables)

		addButton = Button(self.headFrame, text="Add")
		addButton.pack(side=RIGHT)
		addButton.bind("<Button-1>", self.addEntry)

		self.addBox = Entry(self.headFrame)
		self.addBox.pack(side=RIGHT)

		self.refFrame = Frame(self.headFrame)
		self.refFrame.pack(side=LEFT)

	def addEntry(self, master):
		fr = Frame(self.headFrame)
		fr.pack(side=LEFT)
		ent = Entry(fr)
		ent.insert(0, self.addBox.get())
		ent.pack(side=TOP, padx=5)
		ent.configure(state='disabled', justify='center')
		self.trees.append(TreeBuilder.BuildTree(box=self.addBox.get()))
		self.addBox.delete(0, END)


	def buttonClick(self):
		print "totdo"
		


	def genTables(self, master):
		table = Table()
		table.makeTableFromTrees(self.trees)
		table.initVarCols()
		table.initRefCols()
		table.update()
		for table in table.refTable:
			fr = Frame(self.refFrame)
			fr.pack(side=LEFT)
			for col in xrange(len(table)):
				row = 0
				temp=StringVar()
				temp.set(table[col][0])
				width = len(table[col][0])
				ent = Entry(fr, textvariable=temp, width=width)
				ent.grid(column=col, row=row)
				for cell in table[col][1]:
					row += 1
					if col == len(table) - 1:
						button=Button(fr, text=cell, width=width)
						button.grid(column=col, row=row)
						button.bind("<Button-1>", self.buttonClick)
					else:
						t2 = StringVar()
						t2.set(cell)
						ent=Entry(fr, textvariable=t2, width=width)
						ent.grid(column=col, row=row)









root = Tk()
gui = GUI(root)
root.mainloop()
try:
	root.destroy()
except Exception, e:
	pass

