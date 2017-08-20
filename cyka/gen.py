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
		print("ERROR 1")
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

	def print_static(self):
		print(self.name)
		print(" ", self.topic_A.name, self.rang_A)
		print(" ", self.topic_B.name, self.rang_B)

	def satisfaction(self):
		return self.rang_A + self.rang_B

	def getRank(self, index):
		for i in range(len(self.priorityList)):
			if self.priorityList[i] == index:
				return i + 1

	def switchIfBetter(self, p2):
		current = self.satisfaction() + p2.satisfaction()
		
		tmp = self.getRank(p2.topic_A.index) + self.getRank(p2.topic_B.index)
		tmp = tmp + p2.getRank(self.topic_A.index) + p2.getRank(self.topic_B.index)

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

class Topic:
	def __init__(self, name, index):
		self.name = name
		self.index = index
		self.persons = []
		self.color = None

	def assignPerson(self, p):
		self.persons.append(p)
		p.assignToTopic(self)
	
	def assignPersons(self, pl):
		for p in pl:
			self.assignPerson(p)

	#returns n persons who like topic most	
	def nPersonsLikeTopic(self, persons, num):
		retval = []
		count = 0
		for i in range(len(persons[0].priorityList)):
			for p in persons:
				if self.index == p.priorityList[i]:
					retval.append(p)
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

	def build(self, topics, persons, num_ring_topics, num_missing = 0):
		#do not change original
		_topics = topics[:]
		_persons = persons[:]

		#select least popular topic as center
		self.head = Topic.getLeastPopular(_topics, _persons)
		_topics.remove(self.head)
		#TODO if num_missing > 1 increment num_ring_topics
		#select persons who likes center topic most
		self.pers = self.head.nPersonsLikeTopic(_persons, num_ring_topics)
		self.head.assignPersons(self.pers)

		for p, t in self.selectStarTopics(_topics, self.pers, self.head):
			#select topics to already choosed people
			self.ring.append(t)
			_topics.remove(t)
			print("r1 assign:", p.name)
			t.assignPerson(p)
			_persons.remove(p)

		for p, t1, t2 in self.selectRingPersons(self.ring, _persons):
			#select people to already selectd ting topics
			print("r2 assign:", p.name)
			t1.assignPerson(p)
			t2.assignPerson(p)
			self.pers.append(p)
			_persons.remove(p)
			

	#sorts a list of topics into a ring(4 or 5 topics) and build the struts
	def selectRingPersons(self, topics, persons, joker = False):
		_topics = topics[:]
		_persons = persons[:]
		retval = []
		#start with least popular topic
		lp = Topic.getLeastPopular(_topics, _persons)
		_topics.remove(lp)

		tmp = lp

		while len(_topics) > 0:
			#select persons for topic
			p = tmp.nPersonsLikeTopic(_persons, 1)[0]
			_persons.remove(p)
			tmp_next = p.getMostBeautyfulTopic(_topics)
			retval.append((p,tmp,tmp_next))
			tmp = tmp_next
			_topics.remove(tmp)

		#close last connection
		p = Person.getMostSatisfied(_persons, lp, tmp)
		retval.append((p,tmp,lp))

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
		self.sat = topics
		for t in topics:
			p = Person.getMostSatisfied(_persons, center, t)
			print("s1 assign:", p.name)
			t.assignPerson(p)
			print("s2 assign:", p.name)
			center.assignPerson(p)
			self.pers.append(p)
			print("s1 remove:", p.name)
			_persons.remove(p)
			
		

class Ikosaeder:
	def __init__(self, persons = 30):				
		self.numTopics = 12
		self.numPersons = persons

class Oktaeder:
	def __init__(self, persons = 12):
		self.numTopics = 6
		self.numPersons = persons
		self.topics = None
		self.persons = None

	def build(self, topics, persons):
		self.topics = deepcopy(topics)
		self.persons = deepcopy(persons)

		#build ring
		ring = Ring()
		ring.build(self.topics, self.persons, 4)

		#remove objects, that next step uses only remainig
		self.topics.remove(ring.head)
		for t in ring.ring:
			self.topics.remove(t)
		for p in ring.pers:
			print("Remove:", p.name)
			self.persons.remove(p)

		star = Star()
		star.build(self.topics[0], ring.ring, self.persons)

		self.ring = ring
		self.star = star

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
		for p in self.ring.pers:
			p.print_static()
			sat = sat + p.satisfaction()
			i = i + 1
		for p in self.star.pers:
			p.print_static()
			sat = sat + p.satisfaction()
			i = i + 1

		print("Satisfaction:", sat/i)



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
		for p in self.persons_stat:
			p.print_static()
			sat = sat + p.satisfaction()
			i = i + 1

		print("Satisfaction:", sat/i)

	def calculate(self):
		o = Oktaeder()
		o.build(self.topics, self.persons)
		o.printStructure()
		o.printSatisfaction()
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
