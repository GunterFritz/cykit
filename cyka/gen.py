from copy import deepcopy
from random import shuffle
import sys
import operator
import numpy as np

class Person:
	def __init__(self, name):
		self.name = name
		self.priorityList = []
		self.topic_A = None
		self.topic_B = None
		self.strut = None
		self.rang_A = 0
		self.rang_B = 0

	def random(self, num):
		for i in range(1, num + 1):
			self.priorityList.append(i)

		shuffle(self.priorityList)
	
	#returns the most beautiful topic from a list of topics
	def getMostBeautyfulTopic(self, topics):
		#iterate through topic list
		for prio in self.priorityList:
			for t in topics:
				if t.index == prio:
					return t
		print("ERROR 1", self.name)
		return None

	def out(self):
		print(self.name, self.priorityList)

	def assignToTopic(self, topic):
		if self.topic_A == None:
			self.topic_A = topic
			self.rang_A = self.getRank(topic.index)
		elif self.topic_B == None:
			self.topic_B = topic
			self.rang_B = self.getRank(topic.index)
		else:
			print("ERROR 2", self.name)
			out

	def removeAssignment(self, topic):
		if self.topic_A == topic:
			self.topic_A = None
			self.rang_A = 0
		elif self.topic_B == topic:
			self.topic_B = None
			self.rang_B = 0 
		else:
			print("ERROR 3", self.name)
			out

	def print_static(self):
		print(self.name)
		print(" ", self.topic_A.name, self.rang_A)
		print(" ", self.topic_B.name, self.rang_B)

	def satisfaction(self):
		return self.rang_A + self.rang_B

	def getNext(self, topic):
		if self.topic_A == topic:
			return self.topic_B
		elif self.topic_B == topic:
			return self.topic_A
		return None

	def getRank(self, index):
		for i in range(len(self.priorityList)):
			if self.priorityList[i] == index:
				return i + 1

	def switchIfBetter(self, p2):
		current = self.satisfaction() + p2.satisfaction()
		
		tmp = self.getRank(p2.topic_A.index) + self.getRank(p2.topic_B.index)
		tmp = tmp + p2.getRank(self.topic_A.index) + p2.getRank(self.topic_B.index)

		if tmp < current:
			print("--SWITCH__")
			tmp_a = p2.topic_A
			tmp_b = p2.topic_B
			tmp_a.removeAssignment(p2)
			tmp_b.removeAssignment(p2)
			self.topic_A.assignPerson(p2)
			self.topic_B.assignPerson(p2)
			self.topic_A.removeAssignment(self)
			self.topic_B.removeAssignment(self)
			tmp_a.assignPerson(self)
			tmp_b.assignPerson(self)
			


	@staticmethod
	def getMostSatisfied(persons, topic1, topic2):
		rank = 1000
		pers = None
		for p in persons:
			r = p.getRank(topic1.index) + p.getRank(topic2.index)
			if r < rank:
				pers = p
				rank = r
		return pers
	
	#struts: tupple of Topics
	@staticmethod
	def getBest(persons, struts):
		retval = []
		for s in struts:
			p = getMostSatisfied(persons, s[0], s[1])
			retval.append((p, s[0], s[1]))

class Topic:
	def __init__(self, name, index):
		self.name = name
		self.index = index
		self.persons = []
		self.color = None

	def assignPerson(self, p):
		self.persons.append(p)
		p.assignToTopic(self)

	def removeAssignment(self, p):
		self.persons.remove(p)
		p.removeAssignment(self)
	
	def assignPersons(self, pl):
		for p in pl:
			self.assignPerson(p)

	#returns n persons who like topic most
	#list is reverse sorted (person who dislike most is at first position)
	def nPersonsLikeTopic(self, persons, num):
		retval = []
		count = 0
		for i in range(len(persons[0].priorityList)):
			for p in persons:
				if self.index == p.priorityList[i]:
					retval.insert(0, p)
					count = count + 1
				if count == num:
					return retval


	def print(self):
		print("------------------")
		print(self.color, ":")
		print("  Name:", self.name)
		print("  Members:")
		for p in self.persons:
			print("    ", p.name, ",", p.getRank(self.index))

	#calculates least popular topic	
	@staticmethod
	def getLeastPopular(topics, persons):
		#sizeof array y= remaining topics, x = num of topics plus column for topic index
		numTopics = len(persons[0].priorityList)
		count = np.zeros((len(topics), numTopics+1), int)
		row = -1
		for t in topics:
			#write index into first column
			row = row + 1
			count[row][0] = t.index
			for p in persons:
				#iterate through the prioritylist of each person
				#and increment the topic at position of priority 
				for pindex in range(len(p.priorityList)):
					if p.priorityList[pindex] == t.index:
						count[row][pindex+1] = count[row][pindex+1] + 1
						break
		il = count[:,0]
		accu = np.cumsum(count[:,1:],1)

		#calculate popularity
		pop = np.cumsum(accu,1)[:,numTopics-1]
		least_pop = il[np.argmin(pop)]

		pop = np.vstack([il,pop]).transpose()
		print(pop)
		print("Least Popular Topic:", least_pop)
		
		for t in topics:
			if t.index == least_pop:
				retval = t
				return t

		return None


class Structure:
	def __init__(self):
		self.structure = []
		#Oktaeder
		#self.colors = [("white", 1), ("green", 2), ("blue", 3), ("yellow", 4), ("red", 5), ("black", 6)]
		self.colors = {"white" : 1, "green": 2, "blue": 3, "yellow": 4, "red": 5, "black": 6}
		self.colors = {1 : "white", 2: "green", 3:"blue", 4:"yellow", 5:"red", 6:"black"}
		self.connections = [(1,2),(1,3),(1,4),(1,5),(2,3),(3,4),(4,5),(5,2),(6,2),(6,3),(6,4),(6,5)]
		self.translate()

	def translate(self):
		self.struts = []
		for s in self.connections:
			self.struts.append((self.colors[s[0]],self.colors[s[1]]))
			
	#def color(self):

	def print_empty(self):
		for k,v in self.colors.items():
			print("Edge: -", v)
			for s in self.strut_search(v):
				print("  -", s)

	def strut_search(self, color):
		retval = []
		for s in self.struts:
			if s[0] == color or s[1] == color:
				retval.append(s)

		return retval

	def match(self):
		if len(self.structure) != len(self.colors):
			print("configuration error")
			return None

		#for t in self.structure:
		#	t
			
class Ring:
	def __init__(self):
		self.head = None
		self.pers = []
		self.ring = []

	def connect(self, rhs, persons):
		_persons = persons[:]
		_startpoint = Topic.getLeastPopular(self.ring + rhs.ring, _persons)
		if _startpoint in self.ring():
			_ring = self.ring[:]
		else:
			_ring = rhs.ring[:]
		_pers = _startpoint.nPersonsLikeTopic(_persons, 2)

		while tmp is not _ring[0]:
			do
			
		
		#TODO : V connection than N
		# close ring

	def build(self, topics, persons, num_ring_topics, num_missing = 0):
		#do not change original
		_topics = topics[:]
		_persons = persons[:]

		#select least popular topic as center
		self.head = Topic.getLeastPopular(_topics, _persons)
		self.head.color ="white"
		_topics.remove(self.head)
		#TODO if num_missing > 1 increment num_ring_topics
		#select persons who likes center topic most
		self.pers = self.head.nPersonsLikeTopic(_persons, num_ring_topics)
		self.head.assignPersons(self.pers)

		for p, t in self.selectStarTopics(_topics, self.pers, self.head):
			#select topics to already choosed people
			self.ring.append(t)
			_topics.remove(t)
			t.assignPerson(p)
			_persons.remove(p)

		self.closeRing(_persons)

	def closeRing(self, persons):
		_persons = persons[:]
		#select for sorting
		ring_persons = []
		for p, t1, t2 in self.selectRingPersons(self.ring, persons):
			#select people to already selectd ting topics
			t1.assignPerson(p)
			t2.assignPerson(p)
			ring_persons.append(p)
			self.pers.append(p)
			_persons.remove(p)

		#sort ring
		t = ring_persons[0].topic_A
		#TODO sorting

	#sorts a list of topics into a ring(4 or 5 topics) and build the struts
	def selectRingPersons(self, topics, persons, joker = False):
		_topics = topics[:]
		_persons = persons[:]
		retval = []
		#start with least popular topic
		lp = Topic.getLeastPopular(_topics, _persons)
		_topics.remove(lp)
		
		#optimization, add two person two least pop
		pers = lp.nPersonsLikeTopic(_persons, 2)
		#process first person
		end = pers[0].getMostBeautyfulTopic(_topics)
		retval.append((pers[0],lp,end))
		_topics.remove(end)
		_persons.remove(pers[0])
		#process second person
		tmp = pers[1].getMostBeautyfulTopic(_topics)
		retval.append((pers[1],lp,tmp))
		_topics.remove(tmp)
		_persons.remove(pers[1])
			
		#process further ring
		while len(_topics) > 0:
			#select persons for topic
			p = tmp.nPersonsLikeTopic(_persons, 1)[0]
			_persons.remove(p)
			tmp_next = p.getMostBeautyfulTopic(_topics)
			retval.append((p,tmp,tmp_next))
			tmp = tmp_next
			_topics.remove(tmp)

		#close last connection
		p = Person.getMostSatisfied(_persons, end, tmp)
		retval.append((p,tmp,end))

		return retval


	#assign a star around a topic (persons already included)
	def selectStarTopics(self, topics, persons, center = None):
		topics = topics[:]

		#sort by center
		if center is not None:
			persons.sort(key=operator.methodcaller("getRank", center.index), reverse=True)

		assignment = []
		for p in persons:
			t = p.getMostBeautyfulTopic(topics)
			#topic no longer selectable
			topics.remove(t)
			assignment.append((p,t))

		return assignment

class Star:
	def __init__(self):
		num = None
		self.head = None
		self.sat = None
		self.pers = []

	def build(self, center, topics, persons):
		_persons = persons[:]
		self.head = center
		self.head.color ="black"
		self.sat = topics
		for t in topics:
			p = Person.getMostSatisfied(_persons, center, t)
			t.assignPerson(p)
			center.assignPerson(p)
			self.pers.append(p)
			_persons.remove(p)
		

class Ikosaeder:
	def __init__(self, persons = 30):				
		self.numTopics = 12
		self.numPersons = persons

	def build(self, topics, persons):
		self.topics = deepcopy(topics)
		self.persons = deepcopy(persons)
		
		#build upper ring/pentagon
		upper = Ring()
		upper.build(self.topics, self.persons, 5)

		#remove objects, that next step uses only remainig
		self.topics.remove(upper.head)
		self.clear(upper.ring, upper.pers)
		
		#build lower ring/pentagon
		lower = Ring()
		lower.build(self.topics, self.persons, 5)

		#remove objects, that next step uses only remainig
		self.topics.remove(upper.head)
		self.clear(lower.ring, lower.pers)

class Oktaeder:
	def __init__(self, persons = 12):
		self.numTopics = 6
		self.numPersons = persons
		self.topics = None
		self.persons = None

	def build(self, topics, persons):
		#current architecture: 
		# 1 create a star with ring
		# 2 create a star and connect to ring

		#TODO second variant:
		# 1 create two stars and connect it
		# 2 close the ring
		
		#Build both and select better

		self.topics = deepcopy(topics)
		self.persons = deepcopy(persons)

		#build ring
		ring = Ring()
		ring.build(self.topics, self.persons, 4)

		#remove objects, that next step uses only remainig
		self.topics.remove(ring.head)
		self.clear(ring.ring, ring.pers)

		star = Star()
		star.build(self.topics[0], ring.ring, self.persons)

		self.ring = ring
		self.star = star

		self.optimize()

	def clear(self, topics, pers):
		if topics is not None:
			for t in topics:
				self.topics.remove(t)
		if pers is not None:
			for p in pers:
				self.persons.remove(p)

	def getSatisfaction(self):
		self.persons = self.ring.pers + self.star.pers
		sat = 0
		i = 0
		for p in self.persons:
			sat = sat + p.satisfaction()
			i = i + 1

		self.satisfaction = sat/i
		return self.satisfaction

	def optimizeRing(self):
		#self.persons = self.ring.pers + self.star.pers
		self.persons = self.star.pers
		self.persons.sort(key=operator.methodcaller("satisfaction"), reverse=True)

		print("Optimize")
		print(" Satisfaction 1:", self.getSatisfaction())

		for p1 in self.persons:
			for p2 in self.persons:
				if p1 == p2:
					continue
				p1.switchIfBetter(p2)

	def optimize(self, pers = None):
		if pers is None:
			pers = self.ring.pers + self.star.pers
		
		pers.sort(key=operator.methodcaller("satisfaction"), reverse=True)

		for p1 in pers:
			for p2 in self.persons:
				if p1 == p2:
					continue
				p1.switchIfBetter(p2)

	def printStructure(self):
		print("-Oktaeder--------------------------------------------")
		self.ring.head.print()	
		for t in self.ring.ring:
			t.print()
		self.star.head.print()	
		print("-----------------------------------------------------")
		
	def printSatisfaction(self):	
		sat = 0
		i = 0
		print("Ring:")
		for p in self.ring.pers:
			p.print_static()
			sat = sat + p.satisfaction()
			i = i + 1
		print("-------------------------------")
		print("Star:")
		for p in self.star.pers:
			p.print_static()
			sat = sat + p.satisfaction()
			i = i + 1

		self.satisfaction = sat/i
		print("Satisfaction:", self.satisfaction)



class CyKaAlg:
	def __init__(self, themen=6, persons=12):
		self.numTopics = themen
		self.numPersons = persons
		self.connections = 4
		self.persons = []
		self.persons_stat = []
		self.topics = []
		self.structure = []
	
	def printStructure(self):
		print("-----------------------------------------------------")
		for t in self.structure:
			t.print()	
		print("-----------------------------------------------------")


	#init the person table with random priority list
	def random_init(self):
		for i in range(0, self.numPersons):
			name = "P_" + str(i).zfill(2)
			p = Person(name)
			p.random(6)
			self.persons.append(p)
			self.persons_stat.append(p)
		
		for i in range(1, self.numTopics + 1):
			name = "T_" + str(i).zfill(2)
			p = Topic(name, i)
			self.topics.append(p)

	def print_static(self):
		sat = 0
		i = 0
		print("-------------------------------")
		print("-------------------------------")
		for p in self.persons_stat:
			p.print_static()
			sat = sat + p.satisfaction()
			i = i + 1

		print("-------------------------------")
		print("-------------------------------")
		self.oktaeder.printSatisfaction()
		print("Satisfaction old        :", sat/i)
		print("Satisfaction Oktaeder:", self.oktaeder.satisfaction)

	def calculate(self):
		o = Oktaeder()
		o.build(self.topics, self.persons)
		o.optimize()
		o.printStructure()
		o.printSatisfaction()
		self.oktaeder = o
		#step on getLeast popular topic and assign Persons to it
		lp = Topic.getLeastPopular(self.topics, self.persons)
		self.topics.remove(lp)
		self.structure.append(lp)
		p = lp.nPersonsLikeTopic(self.persons, self.connections)
		lp.assignPersons(p)
		
		ring = self.assignRing(lp, self.topics)
		self.removeTopics(ring)
		#assign a ring to remaining topic
		#opposite of lp
		p = self.topics[0].nPersonsLikeTopic(self.persons, self.connections)
		self.topics[0].assignPersons(p)
		print("1-----------------------")
		for x in ring:
			print("T:", x.name)
		ring = self.assignRing(self.topics[0], ring)
		print("2-----------------------")
		for x in ring:
			print("T:", x.name)
		self.structure.append(self.topics[0])
		self.topics.remove(self.topics[0])

		self.closeRing(ring)

		self.printStructure()

	def closeRing(self, ring):
		for x in ring:
			print("T:", x.name)
		for x in self.persons:
			print("P:", x.name)
		t = Topic.getLeastPopular(ring, self.persons)
		pers = t.nPersonsLikeTopic(self.persons, 2)
		t.assignPersons(pers)
		ring.remove(t)

		tmp = []

		for p in pers:
			t = p.getMostBeautyfulTopic(ring)
			t.assignPerson(p)
			self.persons.remove(p)
			tmp.append(t)
			ring.remove(t)
	
		#todo -> more people	
		ring[0].assignPerson(self.persons[0])		
		ring[0].assignPerson(self.persons[1])

		m = max(self.persons[0].getRank(tmp[0].index),
			self.persons[0].getRank(tmp[1].index),
			self.persons[1].getRank(tmp[0].index),
			self.persons[1].getRank(tmp[1].index))

		#todo case of eaqul -> check min value
		if (self.persons[0].getRank(tmp[0].index) < m and
			self.persons[1].getRank(tmp[1].index) < m):
			tmp[0].assignPerson(self.persons[0])		
			tmp[1].assignPerson(self.persons[1])
		else:	
			tmp[0].assignPerson(self.persons[1])		
			tmp[1].assignPerson(self.persons[0])

		self.persons.remove(self.persons[1])
		self.persons.remove(self.persons[0])
		

	#assign a ring around a top (persons already included)
	def assignRing(self, topic, ring):
		ring = ring[:]
		persons = topic.persons
		persons.sort(key=operator.methodcaller("getRank", topic.index), reverse=True)
		#persons.sort(key=getRank(topic.index))

		ring_topics = []
		for p in persons:
			t = p.getMostBeautyfulTopic(ring)
			ring.remove(t)
			t.assignPerson(p)
			self.persons.remove(p)
			ring_topics.append(t)

		return ring_topics
		#t = self.getLeastPopular(self.persons, ring_topics)
		#print("------------------------------------")
		#t.print()

	#helper, to secure switch from stack to structure
	def removeTopics(self, ring):
		for t in ring:
			self.topics.remove(t)
			self.structure.append(t)		

	def createStatistics(self):
		self.tnp_count = np.zeros((self.numTopics, self.numTopics), int)
		#count votes
		for i in range(self.numTopics):
			for p in self.persons:
				#topic number starts with 1
				t = p.priorityList[i] - 1
				self.tnp_count[t][i] = self.tnp_count[t][i] + 1

		self.tnp_accu = np.cumsum(self.tnp_count,1)
		self.popularity = np.cumsum(self.tnp_accu,1)[:,self.numTopics-1]

	def print(self):
		for p in self.persons:
			p.out()

	def print_stat(self):
		print()
		print("single counted")
		print(self.tnp_count)
		print()
		print("accumulated")
		print(self.tnp_accu)
		print("Popularity")
		print(self.popularity)

if __name__ == '__main__':
	#names = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M" ]
	#
	#for p in names:
	#	p1 = Person(p)
	#	p1.random(6)
	#	p1.out()
	
	c = CyKaAlg()
	c.random_init()
	c.createStatistics()
	c.print()
	#c.print_stat()
	c.calculate()
	c.print_static()
	#s = Structure()
	#s.print_empty()
