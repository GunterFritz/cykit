from helper.mime import mime
from PyQt5.QtWidgets import QTreeWidget 
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

class variableTreeWidget(QTreeWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.dragItem = None

	def mouseMoveEvent(self, event):
		super().mouseMoveEvent(event)
		if self.dragItem is not None:
			print("mouseMoveEvent", self.dragItem.getName())
			mimeData = mime()
			mimeData.setData(self.dragItem)
			
			#mimeData = QMimeData()
			#mimeData.setText(self.dragItem.getId())
			#mimeData.setData("CyTreeItem", self.dragItem)
			#drag = QDrag(self)
			#drag.setMimeData(mimeData)
			#dropAction = drag.exec_(Qt.MoveAction)
		

	def mousePressEvent(self, event):
		super().mousePressEvent(event)
		if event.button() == Qt.LeftButton:
			self.dragItem = self.itemAt(event.pos())
		else:
			self.dragItem = None
			print("NONE") 
