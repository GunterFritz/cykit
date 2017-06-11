from objects.cytreeitem import CyTreeItem, RoundedRect
from PyQt5.QtWidgets import QGraphicsLineItem
     
class Connection():
	def __init__(self):
		self.fromItem = None
		self.toItem = None
		#self.line = QGraphicsLineItem()

	def update(self):
		if self.fromItem is None or self.toItem is None:
			return
		coordinates = QLineF(self.fromItem.getLinePoint(self.toItem.center()),
			self.toItem.getLinePoint(self.fromItem.center()))
		self.line.setLine(coordinates)

	def connect(f, t, l):
		self.line = l
		self.fromItem = f
		self.toItem = t
		self.update()
		
		self.fromItem.addOutput(self)
		self.toItem.addInput(self)
