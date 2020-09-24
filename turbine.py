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
		if loss > avg-0.3:
			self.loss    = loss
			self.fitness = 0
