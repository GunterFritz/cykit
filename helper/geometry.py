from PyQt5.QtCore import QRectF, QPoint, QPointF, QLineF 

class Geometry:
	def __init__(self):
		self.grid = 5

	def calcConnector(x1, y1, dir1, rect1, x2, y2, dir2, rect2):
		lines = []
		if dir2 == "down":
			if y1 > y2 and x1 == x2:
				#direct connection
				lines.append(QLineF(QPointF(x1,y1), QPointF(x2,y2)))
			elif y1 > (y2 + 2*self.grid):
				#z-connection
				return zLine(x1, y1, x2, y2, 'H')
			elif (rect2.topLeft().x() > (rect1.topRight().x() + 2 * grid) or 
					rect1.topLeft().x() > (rect2.topRight().x() + 2 * grid)):
				#enough place to draw a line between both rects
				p1 = QPointF(x1,y2+2*grid)
				p2 = QPointF(x2,y2-2*grid)
				lines.append(QLineF(QPointF(x1,y1), p1))
				lines += zLine(p1.x(),p1.y(),p2.x(),p2.y(),'V')
				lines.append(QLineF(QPointF(x2,y2), p2))
			else:
				#round both
				start = QPointF(x1, y1-2*grid)
				end = QPointF(x2, y2+2*grid)
				line.append(QLineF(start, QPointF(x1, y1)))
				if x1 > x2:
					length = x1 - rect2.topLeft.x() + 2*grid
					lines += uLine(start, end, "right")
				else:
					length = rect2.topRight.x() - x1 + 2*grid
					lines += uLine(start, end, "left")
				line.append(QLineF(end, QPointF(x2, y2)))

	def rectToPoint(self, start, rect, point):
		#line starts at top side
		if start.y() == rect.topLeft().y():
			return self.topToPoint(start, rect, point)
		#line starts at left side
		elif start.x() == rect.topLeft().x():
			angle = 90
		#line starts at bottom side
		elif start.y() == rect.bottomLeft().y():
			angle = 180
		#line starts at right side
		elif start.x() == rect.topRight().x():
			angle = 270
		start = self.turnPoint(start,angle)
		point = self.turnPoint(point,angle)
		rect = self.turnRect(rect,angle)
		return self.turnLines(self.topToPoint(start, rect, point), -angle)
		
	def topToPoint(self, start, rect, point):
		#end point is above start point
		if point.y() < start.y() + self.grid:
			return self.zLine(start, point, 'H')
		#end point is above start point, but near to rect
		elif point.y() < start.y():
			return self.uLine(start, point, "bottom", self.grid * 2)
		#end point is left or right from rect
		elif (point.x() < rect.topLeft().x() or
			point.x() > rect.topRight().x()):
			return self.uLine(start, point, "bottom", self.grid * 2)
		#end point is neath rect
		else:
			sp = QPointF(start.x(), start.y() - 2*self.grid)
			lines = []
			lines.append(QLineF(start, sp))
			if start.x() > point.x():
				op = "right"
				length = start.x() - rect.topLeft().x() + 2*self.grid
			else:
				op = "left" 
				length = rect.topRight().x() -start.x() + 2*self.grid
			return lines + self.uLine(sp, point, op, length)
			
	def zLine(self, start, end, direction):
		lines = []
		if direction == 'H':
			#second line is horizontal
			y = (start.y() + end.y())/2
			p2 = QPointF(start.x(), y)
			p3 = QPointF(end.x(), y)
		else:
			#second line is vertical
			x = (start.x() + start.x())/2
			p2 = QPointF(x,start.y())
			p3 = QPointF(x,end.y())
		
		#create lines
		lines.append(QLineF(start, p2))
		lines.append(QLineF(p2, p3))
		lines.append(QLineF(p3, end))
		
		return lines

	def uLine(self, start, end, opening, length):
		angle = 0
		lines = []
		if opening == "right":
			angle = 180
		elif opening == "bottom":
			angle = 90
		elif opening == "top":
			angle = 270
		
		start = self.turnPoint(start, angle)
		end = self.turnPoint(end, angle)
		p2 = QPointF(start.x() + length, start.y())
		p3 = QPointF(start.x() + length, end.y())
		lines.append(self.turnLine(QLineF(start, p2), -angle))
		lines.append(self.turnLine(QLineF(p2, p3), -angle))
		lines.append(self.turnLine(QLineF(p3, end), -angle))

		return lines

	def turnPoint(self, p, angle):
		if angle == 90 or angle == -270:
			return QPointF(-p.y(),p.x())
		if angle == 180 or angle == -180:
			return QPointF(-p.x(),-p.y())
		if angle == -90 or angle == 270:
			return QPointF(p.y(),-p.x())
		else:
			return p
		
	def turnLine(self, line, angle):
		p1 = self.turnPoint(line.p1(), angle)
		p2 = self.turnPoint(line.p2(), angle)
		return QLineF(p1,p2)

	def turnLines(self, lines, angle):
		retval = []
		for l in lines:
			retval.append(self.turnLine(l, angle))
		return retval
	
	def turnRect(self, rect, angle):
		p1 = self.turnPoint(rect.topLeft(), angle)
		p2 = self.turnPoint(rect.bottomRight(), angle)
		topLeft = QPointF(min(p1.x(), p2.x()), min(p1.y(), p2.y()))
		bottomRight = QPointF(max(p1.x(), p2.x()), max(p1.y(), p2.y()))
		return QRectF(topLeft, bottomRight)
