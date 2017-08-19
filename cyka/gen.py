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

	def random(self, num):
		for i in range(1, num + 1):
			self.priorityList.append(i)

		shuffle(self.priorityList)

	def out(self):
		print(self.name, self.priorityList)

	def assignToTopic(self, topic):
		if self.topic_A == None:
			self.topic_A = topic
			self.rang_A = self.getRang(topic.index)
		elif self.topic_B == None:
			self.topic_B = topic
			self.rang_B = self.getRang(topic.index)
		else:
			print("ERROR")

	def getRang(self, index):
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
			print("    ", p.name)

class CyKaAlg:
	def __init__(self, themen=6, persons=12):
		self.numTopics = themen
		self.numPersons = persons
		self.connections = 4
		self.persons = []
		self.topics = []
		self.structure = []
	
	def printStructure(self):
		for t in self.structure:
			t.print()	


	#init the person table with random priority list
	def random_init(self):
		for i in range(0, self.numPersons):
			name = "P_" + str(i).zfill(2)
			p = Person(name)
			p.random(6)
			self.persons.append(p)
		
		for i in range(1, self.numTopics + 1):
			name = "T_" + str(i).zfill(2)
			p = Topic(name, i)
			self.topics.append(p)

	def calculate(self):
		#step on getLeast popular topic and assign Persons to it
		lp = self.getLeastPopular()
		self.structure.append(lp)
		self.assignPersons(lp)
		
		self.assignRing(lp)
		self.printStructure()


	#assign n persons wich like topic most
	def assignPersons(self, topic, persons = None):
		#initialize
		if persons == None:
			persons = self.persons

		#take people who likes the topic
		count = 0
		for i in range(self.numTopics):
			for p in persons:
				if p.priorityList[i] == topic.index:
					topic.assignPerson(p)
					persons.remove(p)
					count = count + 1
				if count == self.connections:
					break
			if count == self.connections:
				break

	def hello(self):
		print("halle")

	#assign a ring around a top (persons already included)
	def assignRing(self, topic):
		persons = topic.persons
		persons.sort(key=operator.methodcaller("getRang", topic.index), reverse=True)
		#persons.sort(key=getRang(topic.index))

		for p in persons:
			self.hello()
			self.assignMostBeautyful(p)

	
	#assign topic which a person mostly like, from available topis		
	def assignMostBeautyful(self, person):
		#iterate through topic list
		for prio in person.priorityList:
			for t in self.topics:
				if t.index == prio:
					self.topics.remove(t)
					self.structure.append(t)
					t.assignPerson(person)
					return None
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
				topics.remove(t)
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

	test = np.array([4,9,9,7,8,2,2])
	print("test:", test)
	print(np.argmin(test))
