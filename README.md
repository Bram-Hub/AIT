# AutomatedIndependenceTester
## Authors
2016:
Konner Atkin

## About
To Run:
	Start application using dist/AIT.exe

To Add Axiom:
	Type axiom using english operators ('and', 'or', 'not', 'if', 'iff')
	Press Add

To Generate Tables:
	Make sure you have filled in the number of variables in the small textbox next to 'Add' Button

	Click 'Generate'

To Manipulate Variable Assignments:
	Click on Buttons under operators on left side
	Values will be automatically updated in the table


Here are 2 Axiom Systems for copy-pasting if desired:

Lukasiewicz
(p if (q if r)) if ((p if q) if (p if r))
(not p if not q) if (q if p)
p if (q if p)

Kleene
p if (q if p)
(p if (q if r)) if ((p if q) if (p if r))
(p if q) if ((p if not q) if not p)
(not (not p)) if p
(p and q) if p
(p and q) if q
p if (q if (p and q))
p if (p or q)
q if (p or q)
(p if r) if ((q if r) if ((p or q) if r))

Known Bugs:
	Double Negations need to be written like (not (not p))
