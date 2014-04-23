"""
The MIT License

Copyright (c) 2014 Jacob Reske
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.
"""
import sys, os
import stats
import numpy as np

class DivMatrix(np.ndarray):

	length = None

	def __init__(self, length):		
		self.length = length
		self = np.zeros(shape=(length, length))
		print self.ndim

	def check(self):
		for row in xrange(length):
			for col in xrange(length):
				if divMatrix[row][col] != divMatrix[col][row]:
					print("exception found, divergence matrix asymmetric!")
				if col == row and divMatrix[row][col] != 0:
					print("exception found, MFCC KL Divergence to self is not 0!")

if __name__ == '__main__':
	length = 13
	m = DivMatrix(length)
	m.add(0, 0, 10)
	print(m.recall(0,0))
	m.check()	
