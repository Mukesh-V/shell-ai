import numpy as np 
import random

class Turbine:
	def __init__(self, x, y):
		self.dna = {
			'x': x,
			'y': y
		}
		self.fitness = 1
		self.loss    = 0.0

	def calcFitness(self, loss, avg):
		self.loss = loss
		if loss > avg+0.2:
			self.fitness = 0