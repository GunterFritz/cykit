#cyVariable contains data of a variable

class CyVariable():
	def __init__(self, sid):
		self.sid = sid
		self.name = "" 
		self.desc = ""

	def getName(self):
		return self.name

	def getId(self):
		return self.sid

	def getDesc(self):
		return self.desc

	def setName(self, name):
		self.name = name

	def setDesc(self, desc):
		self.desc = desc
