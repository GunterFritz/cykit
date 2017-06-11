from helper.singleton import singleton
from model.cyvariable import CyVariable

class CyController(metaclass=singleton):
	def __init__(self):
		self.varDict = {}
		self.num = 0

	#creates a new CyVariable, adds it to dict
	#return created CyVariable
	def createVar(self):
		cyid = "A" + str(self.num + 1)
		self.num += 1
		var = CyVariable(cyid)
		self.varDict[cyid] = var
		return var

	#returns CyVariable with cyid
	def getVar(self, cyid):
		if cyid in self.varDict:
			return self.varDict[cyid]
		else:
			return None
