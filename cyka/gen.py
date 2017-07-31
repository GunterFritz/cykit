from random import shuffle
import sys
import numpy as np

class Person:
	def __init__(self, name):
		self.name = name
		self.priorityList = []

	def random(self, num):
		for i in range(1, num + 1):
			self.priorityList.append(i)

		shuffle(self.priorityList)

	def out(self):
		print(self.name, self.priorityList)

class CyKaAlg:
	def __init__(self, themen=6, persons=12):
		self.numThemen = themen
		self.numPersons = persons
		self.persons = []

	def random_init(self):
		for i in range(0, self.numPersons):
			name = "P_" + str(i).zfill(2)
			p = Person(name)
			p.random(6)
			self.persons.append(p)

	def print(self):
		for p in self.persons:
			p.out()

	def print_stat(self):
		tnp = np.zeros((self.numThemen, self.numThemen), int)
		themen = [0]*self.numThemen
		for i in range(self.numThemen):
			for p in self.persons:
				#themen number starts with 1
				t = p.priorityList[i] - 1
				themen[t] = themen[t] + 1
				tnp[t][i] = tnp[t][i] + 1

		print()
		print(tnp)
		for t in themen:
			print(t)	

if __name__ == '__main__':
	#names = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M" ]
	#
	#for p in names:
	#	p1 = Person(p)
	#	p1.random(6)
	#	p1.out()
	
	c = CyKaAlg()
	c.random_init()
	c.print()
	c.print_stat()

