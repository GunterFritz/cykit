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

	def random(self, num):
		for i in range(1, num + 1):
			self.priorityList.append(i)

		shuffle(self.priorityList)

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
			print("ERROR")

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

class Topic:
	def __init__(self, name, index):
		self.name = name
		self.index = index
		self.persons = []
		self.color = None

	def assignPerson(self, p):
		self.persons.append(p)
		p.assignToTopic(self)

	def print(self):
		print("------------------")
		print(self.color, ":")
		print("  Name:", self.name)
		print("  Members:")
		for p in self.persons:
			print("    ", p.name, ",", p.getRank(self.index))

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
		#step on getLeast popular topic and assign Persons to it
		lp = self.getLeastPopular()
		self.topics.remove(lp)
		self.structure.append(lp)
		self.assignPersons(lp)
		
		ring = self.assignRing(lp)
		self.removeTopics(ring)
		#assign a ring to remaining topic
		#opposite of lp
		self.assignPersons(self.topics[0])
		ring = self.assignRing(self.topics[0], ring)
		self.structure.append(self.topics[0])
		self.topics.remove(self.topics[0])

		self.closeRing(ring)

		self.printStructure()

	def closeRing(self, ring):
		for x in ring:
			print(x.name)
		for x in self.persons:
			print(x.name)
		t = self.getLeastPopular(self.persons, ring)
		pers = self.assignPersons(t, self.persons, 2)
		ring.remove(t)

		tmp = []

		for p in pers:
			t = self.assignMostBeautyful(p, ring)
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
		

	#assign n persons wich like topic most
	def assignPersons(self, topic, persons = None, num = None):
		#initialize
		if persons == None:
			persons = self.persons
		if num == None:
			num = self.connections

		#take people who likes the topic
		ass_pers = []
		count = 0
		for i in range(self.numTopics):
			for p in persons:
				if p.priorityList[i] == topic.index:
					topic.assignPerson(p)
					ass_pers.append(p)
					count = count + 1
				if count == num:
					return ass_pers

	#assign a ring around a top (persons already included)
	def assignRing(self, topic, ring = None):
		if ring is None:
			ring = self.topics
		persons = topic.persons
		persons.sort(key=operator.methodcaller("getRank", topic.index), reverse=True)
		#persons.sort(key=getRank(topic.index))

		ring_topics = []
		for p in persons:
			t = self.assignMostBeautyful(p, ring)
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
			#self.topics.remove(t)
			self.structure.append(t)		

	
	#assign topic which a person mostly like, from available topis		
	def assignMostBeautyful(self, person, topics):
		#iterate through topic list
		for prio in person.priorityList:
			for t in topics:
				if t.index == prio:
					return t
		print("ERROR")
		return None

	#calculates least popular topic
	def getLeastPopular(self, persons = None, topics=None):
		#initialize
		if persons == None:
			persons = self.persons
		if topics == None:
			topics=self.topics

		#sizeof array y= remaining topics, x = num of topics plus column for topic index
		count = np.zeros((len(topics), self.numTopics+1), int)
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
		pop = np.cumsum(accu,1)[:,self.numTopics-1]
		least_pop = il[np.argmin(pop)]

		pop = np.vstack([il,pop]).transpose()
		print(pop)
		print("Least Popular Topic:", least_pop)
		
		for t in topics:
			if t.index == least_pop:
				retval = t
				return t

		return None

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
