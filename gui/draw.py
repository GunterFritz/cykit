from helper.mime import mime
from model.cyvariable import CyVariable
from model.cycontroller import CyController
from gui.editvardialog import EditVarDialog
#from objects.connection import Connection
from objects.cytreeitem import CyTreeItem, RoundedRect, Arrow
import sys, random
from functools import partial
from PyQt5.QtWidgets import QWidget, QApplication, QGraphicsItem, QGraphicsObject, QGraphicsView, QGraphicsEllipseItem, QGraphicsScene, QTreeWidgetItem, QGraphicsLineItem, QFrame 
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QLinearGradient, QTransform
from PyQt5.QtCore import Qt, QRectF, QPoint, QLineF
import gui.draw_ui

class MyScene(QGraphicsScene):
	#editor lost focus
	#mark selected
	#delete items
	def __init__(self, parent=None):
		super().__init__(parent)
		#drawing lines (Connections between variables)
		self.connect = False
		self.line = None
		self.fromItem = None
		self.setSceneRect(0, 0, 300, 500)

	def dragEnterEvent(self, e):
		print("A: ", sys._getframe().f_code.co_name)	
		if e.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
			e.accept()
		else:
			e.ignore() 
	
	def dropEvent(self, e):
		print("B: ", sys._getframe().f_code.co_name)	
		item = mime().getData()
		#accept only CyTreeItems
		if type(item) is not CyTreeItem:
			return
		self.drawItem(e.scenePos(), item)

	def dragEnterEvent(self, e):
		e.acceptProposedAction()

	def dragMoveEvent(self, e):
		e.acceptProposedAction()

	#self.connect is true, if drawLine button is checked
	def setConnect(self, val):
		self.connect = val

	#Paste the item to scene, is called after drop event
	def drawItem(self, pos, item):
		graphic = item.initPaint(pos)
		if graphic is not None:
			self.addItem(graphic)

	def drawLine(self, event):
		toItem = self.itemAtType(event.scenePos(), RoundedRect)
		if toItem is self.fromItem:
			return
		elif toItem is not None:
			self.line.drawLine(event.scenePos(), toItem)
			return
		"""
		toItem = self.itemAtType(event.scenePos(), RoundedRect)
		if toItem is None:
			coordinates = QLineF(self.fromItem.getLinePoint(event.scenePos()), event.scenePos())
		elif toItem is self.fromItem:
			#don't draw line when mouse is over startItem
			coordinates = QLineF()
		else:
			coordinates = QLineF(self.fromItem.getLinePoint(toItem.center()),
				toItem.getLinePoint(self.fromItem.center()))
		"""
		#line not yet added to scene, add it	
		if self.line is None:
			self.line = Arrow(self.fromItem)
			self.addItem(self.line)
		self.line.drawLine(event.scenePos(), None)

	#returns Item at Position, including a typecheck
	#if there is no item at this position or typecheck fails
	#None is returned
	def itemAtType(self, pos, t):
		retval = self.itemAt(pos, QTransform())
		if type(retval) is not t:
			return None
		return retval
	
	def mousePressEvent(self, event):
		print("scene mouse press event")
		#draw line button is activated
		if self.connect:
			self.fromItem = self.itemAtType(event.scenePos(), RoundedRect)
		super().mousePressEvent(event)
	
	def mouseMoveEvent(self, event):
		print("scene mouse move event", event.pos())
		if self.connect and self.fromItem is not None:
			self.drawLine(event)
			print("self.connect", self.fromItem)
			#self.calculateLine(event)
		else:
			print("super")
			super().mouseMoveEvent(event)
	
	def mouseReleaseEvent(self, event):
		#mouseReleaseEvent while drawing a line
		if self.connect and self.line is not None:
			toItem = self.itemAtType(event.scenePos(), RoundedRect)
			if toItem is None or toItem is self.fromItem:
				#line doesn't end at an item, remove it
				self.removeItem(self.line)
				self.line = None
				self.fromItem = None
			else:
				#Connection().connect(self.fromItem,toItem,self.line)
				self.line.drawLine(event.scenePos(), toItem)
				self.line.connect(toItem)
				#Todo add connection
				self.line = None
		super().mouseReleaseEvent(event)

		


class MyView(QWidget, gui.draw_ui.Ui_Form):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)

		self.scene = MyScene(self.graphicsView)

		#self.graphicsView.setFrameShape(QFrame.NoFrame)
		self.graphicsView.setScene(self.scene)
		
		self.setupEvents()
		self.changeToolbox()

	def dropEvent(self, e):
		print("drop")

	def mouseDoubleClickEvent(self, event):
		print("double!")
		super().mouseDoubleClickEvent(event)

	def mousePressEvent(self, event):
		print("hallo")
		super().mousePressEvent(event)

	def itemDoubleClicked(self, item, column):
		print("double item clicked")
		item.edit()

	def setupEvents(self):
		self.addVarButton.clicked.connect(self.addTreeItem)
		self.connectButton.clicked.connect(self.changeToolbox)
		self.treeWidget.itemDoubleClicked.connect(self.itemDoubleClicked)
	#self.scene.customContextMenuRequested.connect(self.openMenu)

	def changeToolbox(self):
		self.scene.setConnect(self.connectButton.isChecked())

	def addTreeItem(self):
		var, ok = EditVarDialog.editVar(None)
		if not ok:
			return
		print(var.getName())
		item = CyTreeItem(var)
		self.treeWidget.addTopLevelItem(item)
		#item.setFlags(item.flags() | Qt.ItemIsEditable)
		#self.treeWidget.editItem(item)

	def openMenu(self, position):
		menu = QtWidgets.QMenu()
		item = self.scene.itemAt(position)
		if item is not None:
			menu.addAction("Delete", self.delete)
			menu.addAction("Edit", self.edit)
		else:
			menu.addAction("Create Variable", partial(self.addItem, position))


if __name__ == '__main__':
	app = QApplication(sys.argv)
	view = MyView()
	view.show()
	sys.exit(app.exec_())


