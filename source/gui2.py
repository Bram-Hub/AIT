from Tkinter import *
from tester import *
from gtmap import *
from treestuff import *

class GUI:
	def __init__(self, master, trees=[]):
		self.master = master
		
		master.title = "AIT GUI"
		master.minsize(width=800, height=600)
		
		self.headFrame = Frame(master)
		self.headFrame.pack(side=TOP, anchor=N)


		genButton = Button(self.headFrame, text="Generate Tables")
		genButton.pack(side=RIGHT, anchor=N)
		genButton.bind("<Button-1>", self.genTables)

		addButton = Button(self.headFrame, text="Add")
		addButton.pack(side=RIGHT, anchor=N)
		addButton.bind("<Button-1>", self.addEntry)

		self.varBox = Entry(self.headFrame, width=2)
		self.varBox.pack(side=RIGHT, anchor=N)

		self.addBox = Entry(self.headFrame, width=30)
		self.addBox.pack(side=RIGHT, anchor=N)

		self.refFrame = Frame(self.headFrame)
		self.refFrame.pack(side=LEFT, anchor=N)

		self.controller = Controller(self.refFrame, self.headFrame)

	def addEntry(self, master):
		fr = Frame(self.headFrame)
		fr.pack(side=LEFT, anchor=N)
		self.controller.addFrame(fr, self.addBox.get())
		self.addBox.delete(0, END)

	def genTables(self, master):
		self.controller.generate(int(self.varBox.get()))
		self.controller.initVarCols()
		self.controller.initRefCols()
		self.controller.update()

root = Tk()
gui = GUI(root)
root.mainloop()
try:
	root.destroy()
except Exception, e:
	pass

