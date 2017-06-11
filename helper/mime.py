from helper.singleton import singleton

class mime(metaclass=singleton):
	def __init__(self):
		self.obj = None

	def setData(self, obj):
		self.obj = obj
	
	def getData(self):
		return self.obj
