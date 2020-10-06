import numpy as np 
import random

limit  =  4000.0
clearance = 50.0
life      =   15
thresh    = -0.1

class Turbine:
	def __init__(self):
		self.dna = []
		for i in range(0, life):
			x, y = random.uniform(clearance, limit-clearance), random.uniform(clearance, limit-clearance)
			self.dna.append([x, y])
		self.fitness = 1.0
		self.loss    = 0.0

	def calcFitness(self):
		if self.loss < thresh:
			self.fitness += self.loss
		elif self.loss > thresh:
			self.fitness -= self.loss

	def mutate(self, p1, p2):
		weight = random.randint(0, life)
		self.dna[0:weight] = p1[0:weight]
		self.dna[weight+1:life] = p2[weight+1:life]
