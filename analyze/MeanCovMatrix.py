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


	def __init__(self, tablesize):		
		self.tablesize = tablesize
		'''
		for i in range(tablesize):
			self.table[0].append(0)
			self.table[1].append(0)
			self.table[2].append(0)
		'''

	def addmp3ToTable(self, index, mp3):
		self.table[0].append(mp3)


	def addToTable(self, index, mean, cov):
		self.table[1].append(mean)
		self.table[2].append(cov)


	def recallfromTable(self, index):
		return self.table[1][index], self.table[2][index]