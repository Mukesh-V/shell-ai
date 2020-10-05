import numpy as np 
import random

limit  =  4000.0
clearance = 50.0
life      =   50

class Turbine:
	def __init__(self):
		self.dna = []
		for i in range(0, life):
			x, y = random.uniform(clearance, limit-clearance), random.uniform(clearance, limit-clearance)
			self.dna.append([x, y])
		self.fitness = 100.0
		self.loss    = 0.0

	def calcFitness(self, avg):
		if self.loss < avg:
			self.fitness += self.loss
		elif self.loss > avg:
			self.fitness -= self.loss

	def mutate(self, p1, p2):
		weight = random.uniform(0, 1)
		for i in range(0, life):
			self.dna.append([elem1 * weight for elem1 in p1[i]] + [elem2 * (1-weight) for elem2 in p2[i]])
