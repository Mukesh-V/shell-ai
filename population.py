from turbine import Turbine 
from utils import *

import random
import csv
import sys

limit = 4000.0
clearance = 50.0

sys.setrecursionlimit(10**8)

class Pop:
	def __init__(self, n):
		self.config = config()
		self.pop = []
		self.coords = []
		self.losses = []
		self.pool = []
		c = 0

		while(True):
			x, y = random.uniform(clearance, limit+clearance), random.uniform(clearance, limit+clearance)
			dna = {'x': x, 'y': y}
			obj = self.spawn(dna)
			if obj:
				self.coords.append([x, y])
				self.pop.append(obj)
				c += 1
			if c == n:
				break

	def spawn(self, dna):
		x, y = dna['x'], dna['y']
		obj = Turbine(x, y)
		if indivCheckConstraints(obj, self.coords, self.config['dia']):
			return obj
		else:
			del obj	
			return 0	

	def run(self, n):
		print('Running : ', n)
		i = 0
		while(True):
			self.pop[i].calcFitness(self.losses[i], np.mean(self.losses))
			if self.pop[i].fitness:
				self.pool.append(self.pop[i])
			i += 1
			if i == 50:
				break
		i = 0
		while(True):
			if not(self.pop[i].fitness):
				del self.pop[i]
				del self.coords[i]
				self.losses = np.delete(self.losses, i)
				self.mutate()
			i += 1
			if i == 50:
				self.pool = []
				self.losses = []
				break

	def mutate(self):
		num = len(self.pool)
		p1, p2 = random.randint(0, num-1), random.randint(0, num-1)
		if p1 == p2:
			return self.mutate()
		else:
			crossedDNA = self.crossover(p1, p2)
			obj = self.spawn(crossedDNA)
			if obj:
				self.pop.append(obj)
				self.losses = np.append(self.losses, 0)
				self.coords.append([obj.dna['x'], obj.dna['y']])
			else:
				return self.mutate()

	def randomSpawn(self):
		x, y = random.uniform(clearance, limit+clearance), random.uniform(clearance, limit+clearance)
		dna = {'x': x, 'y': y}
		obj = self.spawn(dna)
		if obj:
			self.pop.append(obj)
			self.losses = np.append(self.losses, 0)
			self.coords.append([x, y])
		else:
			self.randomSpawn()

	def crossover(self, p1, p2):
		weight = random.uniform(0, 2)
		if self.pool[p1].loss < self.pool[p2].loss:
			if weight < 0.5:
				weight = 2 - weight
		crossed = {
			'x' : weight * self.pool[p1].dna['x'] + (1-weight) * self.pool[p2].dna['x'],
			'y' : weight * self.pool[p1].dna['y'] + (1-weight) * self.pool[p2].dna['y']
		}
		return crossed


	def writeCSV(self, name):
		with open(name,'w') as file:
			cursor = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			cursor.writerow(['x','y'])
			for i, record in enumerate(self.coords):
				cursor.writerow(record)
		file.close()

