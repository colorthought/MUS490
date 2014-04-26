"""
The MIT License

Copyright (c) 2014 Jacob Reske
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.
"""
import sys, os
import stats
import numpy as np

class MeanCovMatrix:

	tablesize = None
	table = [[] for k in range(3)]
	defaultMean = np.array([1, 2, 3])
	defaultCov = np.array([1, 2, 3])

	def __init__(self, tablesize):		
		self.tablesize = tablesize	
		for i in range(tablesize):
			self.table[1].append(self.defaultMean)
			self.table[2].append(self.defaultCov)


	def addmp3ToTable(self, index, mp3):
		self.table[0].append(mp3)


	def addToTable(self, index, mean, cov):
		#print(mean)							#[DEBUG]
		self.table[1][index] = mean
		self.table[2][index] = cov


	def recallfromTable(self, index):
		return self.table[1][index], self.table[2][index]