import sys
import math

#from objects.connection import Connection
from helper.geometry import Geometry
from model.cyvariable import CyVariable
from gui.editvardialog import EditVarDialog
from PyQt5.QtWidgets import QTreeWidgetItem, QGraphicsObject, QGraphicsItem, QGraphicsLineItem
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QLinearGradient, QPolygonF, QPainterPath 
from PyQt5.QtCore import Qt, QRectF, QPoint, QPointF, QSizeF, QLineF 


class CyTreeItem(QTreeWidgetItem):
	def __init__(self, var):
		QGraphicsObject.__init__(self)
		QTreeWidgetItem.__init__(self, [var.getName()])

		self.cyvar = var
		self.diagrammRep = None

	def getName(self):
		return self.cyvar.getName()
	
	def getId(self):
		return self.cyvar.getId()

	def getText(self):
		return self.cyvar.getText()

	#call edit dialog
	def edit(self):
		var, ok = EditVarDialog.editVar(self.cyvar)
		if ok:
			self.update()

	#update gui events
	def update(self):
		self.setText(0, self.cyvar.getName())
	
	#methods for drawing objects

	#event is called, when rectangled is moved
	def itemChange(self, change, value):
		print("item change")
		return super().itemChange(change, value)

	#called, when item has to be drawed
	def initPaint(self, pos):
		if self.diagrammRep is not None:
			return None
		self.diagrammRep = RoundedRect(pos, self)
		return self.diagrammRep

#Synchronization:
#Variante 1, mittels Singleton dictionary
#Variante 2, Mehrfachvererbung
#Variante 3, Connector, der beide enthält

class RoundedRect(QGraphicsObject):
	def __init__(self, pos, item):
		super().__init__()
		self.color = Qt.blue
		self.text = ""
		self.parent = item

		self.inputs = []
		self.outputs = []

		self.setFlag(QGraphicsItem.ItemIsMovable)
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self.setPos(pos)

	def mouseDoubleClickEvent(self, event):
		print("E: ", sys._getframe().f_code.co_name, self.parent.getName())	
		self.parent.edit()
	
	#event is called, when rectangled is moved
	def itemChange(self, change, value):
		print("item change XX")
		#item is moved, update lines(connections)
		for o in self.outputs:
			o.update()
		for i in self.inputs:
			i.update()
		return super().itemChange(change, value)

	#appends a connection as output
	def addOutput(self, o):
		self.outputs.append(o)

	#appends a connection as input
	def addInput(self, i):
		self.inputs.append(i)

	def center(self):
		return QPointF(self.pos().x() + 60, self.pos().y() + 30)

	#returns rect at position
	def getPositionalRect(self):
		return QRectF(self.pos(), QSizeF(120, 60))

	def getLinePoint(self, end):
		#rect = QRectF(self.pos(), QPoint(self.pos().x()+120, self.pos().y()+60))
		rect = QRectF(self.pos(), QSizeF(120, 60))
		#calculate center points 
		left = QPointF(rect.topLeft().x(), rect.center().y())
		right = QPointF(rect.bottomRight().x(), rect.center().y())
		top = QPointF(rect.center().x(), rect.topLeft().y())
		bottom = QPointF(rect.center().x(), rect.bottomRight().y())
		
		if rect.topLeft().x() < end.x():
		#point is not left from rect
			if rect.bottomRight().x() < end.x():
				y1 = GeoHelper.getY(-1, rect.bottomRight().x(), rect.topLeft().y(), end.x())
				if end.y() < y1:
					return "top", top
				y1 = GeoHelper.getY(1, rect.bottomRight().x(), rect.bottomRight().y(), end.x())
				if end.y() < y1:
					return "right", right
				return "bottom", bottom
			elif rect.center().y() < end.y():
				return "bottom", bottom
			else:
				return "top", top
		else:
		#point is left from rect
			y1 = GeoHelper.getY(1, rect.topLeft().x(), rect.topLeft().y(), end.x())
			if end.y() < y1:
				return "top", top
			y1 = GeoHelper.getY(-1, rect.topLeft().x(), rect.bottomRight().y(), end.x())
			if end.y() < y1:
				return "left", left
			return "bottom", bottom
	"""
	calculates the intersection Point to the rect with shortest distance to pos
	"""
	def getNearestPoint(self, pos):
		rect = self.getPositionalRect()
		
		print(rect.topLeft(), rect.bottomRight(), pos)
		
		m1 = GeoHelper.pointline(rect.topLeft(), rect.bottomRight(), pos)
		m2 = GeoHelper.pointline(rect.bottomLeft(), rect.topRight(), pos)
		if m1 == 1:
			if m2 == 1:
				return "top", QPointF(pos.x(),rect.topLeft().y())
			else:
				return "right", QPointF(rect.topRight().x(), pos.y())
		else:
			if m2 == 1:
				return "left", QPointF(rect.topLeft().x(), pos.y())
			else:
				return "bottom", QPointF(pos.x(),rect.bottomLeft().y())
				
	
	def mousePressEvent(self, event):
		print(sys._getframe().f_code.co_name, self.text)

	def setColor(self, color):
		self.color = color

	def boundingRect(self):
		#todo add pen/2
		return QRectF(QPointF(0,0), QSizeF(120, 60))

	def paint (self, painter, option, widget = None):
		if self.isSelected():
			painter.setPen(QPen(Qt.red, 3))
		rect = self.boundingRect()
		#rect = self.getPositionalRect()
		gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
		gradient.setColorAt(0.0, self.color)
		gradient.setColorAt(0.4, Qt.white)
		gradient.setColorAt(0.7, self.color)
		painter.setBrush(gradient)
		painter.drawRoundedRect(rect, 10.0, 10.0)
		painter.drawText(rect, Qt.AlignCenter, self.parent.getName())

class GeoHelper():
	"""
	calculates a line between p1 and p2 and returns:
	-1 if p3 is under the line
	0 if p3 is on the line
	1 if p3 is over the line
	"""
	@staticmethod
	def pointline(p1, p2, p3):
		a = (p1.y() - p2.y())/(p1.x() - p2.x())
		b = p1.y() - a*p1.x()
		y = a*p3.x() + b
		if y < p3.y():
			return -1
		if y > p3.y():
			return 1
		return 0

	"""calculates a function ax+b and returns the f(x1)"""
	@staticmethod
	def getY(a, x, y, x1):
		#y = ax + b
		#b = y - ax
		b = y - a*x
		return a*x1+b
	
	"""
	returns the direction of a vertical or horizontal line
	p1 is the beginning and p2 the end
	"""
	@staticmethod
	def getIntersection(line, rect):
		if line.p1().x() == line.p2().x():
		#vertical line
			if line.p1().y() < line.p2().y():
				#line goes down, return upper side of rect
				side = QLineF(rect.topLeft(), rect.topRight())
			else:
				#line goes up, return bottom side of rect
				side = QLineF(rect.bottomLeft(), rect.bottomRight())
		else:
		#horizontal line
			if line.p1().x() < line.p2().x():
				#line goes from left to rigth, return left side
				side = QLineF(rect.topLeft(), rect.bottomLeft())
			else:
				#line goes from right to left , return right side
				side = QLineF(rect.topRight(), rect.bottomRight())
		#calculate intersection
		intersectPoint = QPointF()
		print(side)
		if line.intersect(side, intersectPoint) == QLineF.BoundedIntersection:
			return intersectPoint
		return None

class Arrow(QGraphicsLineItem):
	def __init__(self, start):
		super().__init__()
		self.fromItem = start
		self.startPoint = None
		self.toItem = None
		self.endPoint = None
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self.color = Qt.black
		self.pen = QPen(self.color, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
		self.arrowHead = QPolygonF()
		self.fromItem.addOutput(self)
		#self.toItem.addInput(self)
		
		self.lines = []

	"""
	We need to reimplement this function because the arrow is larger 
	than the bounding rectangle of the QGraphicsLineItem. The graphics
	scene uses the bounding rectangle to know which regions of the scene to update
	"""
	def boundingRect(self):
		extra = (self.pen.width() + 20)/ 2.0
		rect = self.calcRect()
		return rect.normalized().adjusted(-extra, -extra, extra, extra)

	"""
	The shape function returns a QPainterPath that is the exact shape
	of the item. The QGraphicsLineItem::shape() returns a path with a
	line drawn with the current pen, so we only need to add the arrow
	head. This function is used to check for collisions and selections
	with the mouse.
	"""
	def shape(self):
		#path = super().shape()
		path = QPainterPath()
		path.addRect(self.calcRect())
		path.addPolygon(self.arrowHead)

		return path
	
	#redraw, due to moving an object	
	def update(self):
		if self.fromItem is None or self.toItem is None:
			return
		coordinates = QLineF(self.fromItem.getLinePoint(self.toItem.center()),
			self.toItem.getLinePoint(self.fromItem.center()))
		#self.setLine(coordinates)

	def drawLine(self, point, item):
		self.setPoint2(point)
		if item is not None:
			self.setItem(item)
		#trigger paint to update/ redraw
		self.setLine(self.lines[-1])
		#super().update(self.boundingRect())

	def setPoint2(self, point):
		if self.startPoint is None:
			s1, self.startPoint = self.fromItem.getNearestPoint(point)
			print("--------------------")
			print(s1)
			print("--------------------")
		g = Geometry()
		self.lines = g.rectToPoint(self.startPoint, self.fromItem.getPositionalRect(), point) 

	#called to draw the line temporarly
	def setPoint(self, point):
		#clear
		self.lines = []
		self.toItem = None

		side, p1 = self.fromItem.getLinePoint(point)
		if side == "top" or side == "bottom":
			p2 = QPointF(p1.x(),point.y())
		else:
			p2 = QPointF(point.x(), p1.y())
		
		self.addOrAppend(0, QLineF(p1,p2))
		if p2 != point:
			self.addOrAppend(1, QLineF(p2,point))

	def setItem(self, end, pos):
		s2, self.endPoint = end.getNearestPoint(pos)

	def setItem(self, end):
		rect = end.getPositionalRect()
		lines = []
		print("set Item")
		#calculate intersection
		for l in self.lines:
			d = GeoHelper.getIntersection(l, rect)
			if d is not None:
				lines.append(QLineF(l.p1(), d))
				break
			lines.append(l)
		self.lines = lines

	def connect(self, end):
		self.toItem = end
		self.toItem.addInput(self)

	def calcRect(self):
		minX = self.lines[0].p1().x()
		minY = self.lines[0].p1().y()
		maxX = self.lines[0].p1().x()
		maxY = self.lines[0].p1().y()

		for l in self.lines:
			minX = min(minX, l.p2().x())
			minY = min(minY, l.p2().y())
			maxX = max(maxX, l.p2().x())
			maxY = max(maxY, l.p2().y())

		return QRectF(QPointF(minX, minY), QPointF(maxX, maxY))
	
	def addOrAppend(self, i, line):
		if len(self.lines) > i:
			self.lines[i] = line
		else:
			self.lines.append(line)

	def paint (self, painter, option, widget = None):
		arrowSize = 10
		#pen = self.pen()
		painter.setPen(self.pen)
		painter.setBrush(self.color)
		#calculate line
		#coordinates = QLineF(self.fromItem.getLinePoint(self.toItem.center()),
		#	self.toItem.getLinePoint(self.fromItem.center()))
		#self.setLine(coordinates)

		#calculate points of arrow
		line = self.lines[-1]
		angle = math.acos(line.dx() / line.length())
		if line.dy() >= 0:
			angle = (math.pi * 2) - angle

		p1 = line.p2() - QPointF(math.sin(angle + math.pi / 3) * arrowSize,
			math.cos(angle + math.pi / 3) * arrowSize)
		p2 = line.p2() - QPointF(math.sin(angle + math.pi -math.pi / 3) * arrowSize,
			math.cos(angle + math.pi - math.pi / 3) * arrowSize)

		self.arrowHead.clear()
		self.arrowHead.append(line.p2())
		self.arrowHead.append(p1)
		self.arrowHead.append(p2)
		for l in self.lines:
			painter.drawLine(l)
		painter.drawPolygon(self.arrowHead)

		if self.isSelected():
			for line in self.lines:
				painter.setPen(QPen(self.color,1, Qt.DashLine))
				l = line
				l.translate(0, 4.0)
				painter.drawLine(l)
				l.translate(0, -8.0)
				painter.drawLine(l)


