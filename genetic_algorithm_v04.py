#!/usr/bin/env python

import math
import random

TARGET = 10

POPULATION_SIZE = 100
CROSSOVER_PROBABILITY = 0.65
MUTATION_PROBABILITY = 0.02
ELITISM_SIZE = 2


class Chromosome:
	def __init__(self, alleles=None):
		if alleles is None:
			self.alleles = [random.random() for i in range(5)]
		else:
			self.alleles = alleles
	def output(self):
		return math.fsum(self.alleles)
	def fitness(self):
		return 1.0 / (TARGET - self.output())
	def crossover(self, otherChromosome):
		a = []
		for i in range(len(self.alleles)):
			if random.random() < CROSSOVER_PROBABILITY:
				a.append(self.alleles[i] + otherChromosome.alleles[i])
			else:
				a.append(self.alleles[i])
		return Chromosome(a)
	def mutate(self):
		for a in self.alleles:
			if random.random() < MUTATION_PROBABILITY:
				a += random.uniform(-1.0, 1.0)

class Population:
	def __init__(self, chromosomes):
		self.chromosomes = chromosomes
	def pick(self, excludeChromosome):
		aChromosomes = self.chromosomes[:]
		if excludeChromosome:
			aChromosomes.remove(excludeChromosome)
		r = random.uniform(0.0, math.fsum([c.fitness() for c in aChromosomes]))
		s = 0.0
		for c in aChromosomes:
			s += c.fitness()
			if s > r:
				return c
	def best(self):
		self.chromosomes.sort(key = lambda x: x.fitness(), reverse=True)
		return self.chromosomes[0]
	def iterate(self):
		offsprings = []
		for i in range(int(len(self.chromosomes) - ELITISM_SIZE)):
			c1 = self.pick(None)
			c2 = self.pick(c1)
			o = c1.crossover(c2)
			o.mutate()
			offsprings.append(o)
		self.chromosomes.sort(key = lambda x: x.fitness(), reverse=True)
		for i in range(ELITISM_SIZE):
			offsprings.append(self.chromosomes[i])
		self.chromosomes = offsprings
	
if __name__ == "__main__":
	p = Population([Chromosome() for i in range(POPULATION_SIZE)])

	for i in range(100):
		p.iterate()
		print i, p.best().alleles, p.best().output()

