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


	#return the side where the point intersect rectangle
	#return the angle that side of point is top
	def getAngle(self, point, rect):
		#line starts at top side
		if point.y() == rect.topLeft().y():
			return "top", 0
		#line starts at left side
		elif point.x() == rect.topLeft().x():
			return "left", 90
		#line starts at bottom side
		elif point.y() == rect.bottomLeft().y():
			return "bottom", 180
		#line starts at right side
		elif point.x() == rect.topRight().x():
			return "right", 270
		return None, 0

	"""
	Calculates all lines from one rectangle to another, without intersecting
	one of the rectangle

	parmeters
	---------
	start: QPointF
	       first point of lines
	s_rect: QRectF 
               first rectangle( start intersects s_rect)
	end: QPointF
	       last point of lines
	s_rect: QRectF 
               second rectangle( end intersects e_rect)
	
	return
	---------
	List of QLineF
	"""
	def rectToRect(self, start, s_rect, end, e_rect):
		side, angle = self.getAngle(start, s_rect)
		s = self.turnPoint(start, angle)
		e = self.turnPoint(end, angle)
		s_r = self.turnRect(s_rect, angle)
		e_r = self.turnRect(e_rect, angle)
		
		return self.topToRect(s, s_r, e , e_r)

	def topToRect(self, start, s_rect, end, e_rect):
		side, angle = self.getAngle(end, e_rect)
		if side == "top":
			#draw from upper to lower rect
			if s_rect.topLeft().y() < e_rect.topLeft().y():
				return self.topTop(start, s_rect, end, e_rect)
			else:
				return list(reversed(self.topTop(end, e_rect, start, s_rect)))
		if side == "left":
			return self.topLeft(start, s_rect, end, e_rect)

	"""
	draw connection from upper side of rect1 to upper side of rect2
	start, QPointF (start point)
	upper, QRectF (upper rect)
	end, QPointF (end point)
	bottom, QRectF (bottom rect)
	""" 
	def topTop(self, start, upper, end, bottom):
		if (end.x() < upper.topLeft().x() or
			end.x() > upper.topRight().x()):
			return self.uLine(start, end, "bottom", self.grid * 2)
		#bottom rect is neath upper rect
		lines = []
		p1 = QPointF(start.x(), start.y() - 2*self.grid)
		p2 = QPointF(end.x(), end.y() - 2*self.grid)
		lines.append(QLineF(start, p1))
		if start.x() > end.x():
			op = "right"
			length = start.x() - upper.topLeft().x() + 2*self.grid
		else:
			op = "left" 
			length = upper.topRight().x() -start.x() + 2*self.grid
		lines = lines + self.uLine(p1, p2, op, length)
		lines.append(QLineF(p2, end))
		return lines

	"""
	Draws lines from top of first rect to left side of an second rectangle

	parmeters
	---------
	start: QPointF
	       first point of lines
	s_rect: QRectF 
               first rectangle( start intersects s_rect)
	end: QPointF
	       last point of lines
	s_rect: QRectF 
               second rectangle( end intersects e_rect)
	
	return
	---------
	List of QLineF
	"""
	def topLeft(self, start, s_rect, end, e_rect):
		lines = []
		if end.x() > start.x() and end.y() < start.y():
			#end is above and left from start
			return self.lLine(start, end, "H")
		
		#add line of grid length from start
		p1 = QPointF(start.x(), start.y() - 2*self.grid)
		lines.append(QLineF(start, p1))
		if s_rect.topRight().x() < end.x() + 2*self.grid:
			#end is right from s_rect
			return lines + self.zLine(p1, p2, "H", start.x() + end.x() - s_rect.topRight().x())
		#add line of 2 grid length from end
		p2 = QPointF(min(end.x(),s_rect.topLeft().x()) - 2*self.grid, end.y())
		length = 2*self.grid 
		if e_rect.topRight().y() < start.y():
			length = length + start.y() - e_rect.topRight().y()
		lines = lines + self.uLine(p1, p2, "bottom", length)
		lines.append(QLineF(p2, end))
		return lines
		
	
	def rectToPoint(self, start, rect, point):
		side, angle = self.getAngle(start, rect)
		start = self.turnPoint(start,angle)
		point = self.turnPoint(point,angle)
		rect = self.turnRect(rect,angle)
		return self.turnLines(self.topToPoint(start, rect, point), -angle)
		
	def topToPoint(self, start, rect, point):
		#end point is above start point
		if point.y() < start.y() + self.grid:
			return self.lLine(start, point, 'H')
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
			
	"""
	Calculates a line in form of "L" 

	parmeters
	---------
	start: QPointF
	       first point of lines
	end: QPointF
	     last point of lines
	direction: String 
               	   direction of second line, 
		   H (horizontal)
		   V (verticla)
	return
	---------
	List of QLineF (2lines)
	"""
	def lLine(self, start, end, direction):
		lines = []
		if start.x() == end.x() or start.y() == end.y():
			#both points are on same axis, draw single line
			lines.append(QLineF(start, end))
			return lines

		if direction == 'H':
			#second line is horizontal
			p2 = QPointF(start.x(), end.y())
		else:
			#second line is vertical
			p2 = QPointF(end.x(),start.y())
		
		#create lines
		lines.append(QLineF(start, p2))
		lines.append(QLineF(p2, end))
		
		return lines

	def zLine(self, start, end, direction, length = 0):
		lines = []
		if direction == 'H':
			#second line is horizontal
			y = (start.y() + end.y())/2 if length == 0 else length
			p2 = QPointF(start.x(), y)
			p3 = QPointF(end.x(), y)
		else:
			#second line is vertical
			x = (start.x() + start.x())/2 if length == 0 else length
			p2 = QPointF(x,start.y())
			p3 = QPointF(x,end.y())
		
		#create lines
		lines.append(QLineF(start, p2))
		lines.append(QLineF(p2, p3))
		lines.append(QLineF(p3, end))
		
		return lines
	"""
	draw U from start to end
	start QPointF
	end QPointF
	opening, side whithout line (top, right, left, bottom)
	length, lenght of first line
	"""
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
