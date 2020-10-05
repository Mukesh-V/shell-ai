from turbine import Turbine 
from utils import *

import random
import csv
import sys

limit  =  4000.0
clearance = 50.0

num       =   50
life      =   15

sys.setrecursionlimit(10**8)

class Pop:
	def __init__(self):
		self.config = config()
		self.idx    = 0
		self.coords = []
		self.pop    = []
		self.losses = []
		self.pool   = []
		self.thresh = 0

		for i in range(0, num):
			obj = Turbine()
			self.pop.append(obj)

	def init(self):
		for i in range(0, num):
			self.coords.append(self.pop[i].dna[self.idx])

	def run(self):
		for i in range(0, num):
			self.coords[i] = self.check(i)
			self.pop[i].dna[self.idx] = self.coords[i]

	def check(self, i):
		if indivCheckConstraints(self.coords[i], self.coords, self.config['dia']):
			return self.coords[i]
		else:
			x, y = random.uniform(clearance, limit-clearance), random.uniform(clearance, limit-clearance)
			self.coords[i] = [x, y]
			return self.check(i)

	def eval(self):
		avg = np.mean(self.losses)
		for i in range(0, num):
			self.pop[i].loss = self.losses[i]
			self.pop[i].calcFitness(avg)

	def selection(self):
		fitness_arr = np.asarray([pop.fitness for pop in self.pop])
		self.thresh = np.mean(fitness_arr)
		print('selection : ', self.thresh)
		print(fitness_arr)
		for i in range(0, num):
			if self.pop[i].fitness >= self.thresh:
				self.pool.append(self.pop[i])

	def crossover(self):
		print('crossover : ', len(self.pool))
		pool_len = len(self.pool)
		for i in range(0, num):
			if self.pop[i].fitness < self.thresh:
				p1, p2 = random.randint(0, pool_len-1), random.randint(0, pool_len-1)
				if p1 == p2:
					p1, p2 = random.randint(0, pool_len-1), random.randint(0, pool_len-1)
				self.pop[i].mutate(self.pool[p1].dna, self.pool[p2].dna)

	def nullify(self):
		print('nullify')
		self.coords = []
		self.pool   = []
		self.losses = []	

	def writeCSV(self, name):
		with open(name,'w') as file:
			cursor = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			cursor.writerow(['x','y'])
			for i, record in enumerate(self.coords):
				cursor.writerow(record)
		file.close()

