"""
The MIT License

Copyright (c) 2014 Jacob Reske
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.
"""
import sys, os, random, logging
import numpy as np
from operator import itemgetter
sys.path.append(os.path.abspath('..'))
from MeanCovMatrix import MeanCovMatrix


class KMeansGaussian():

	k = 3
	max_iter = 20
	init = "random"
	MeanCovMatrix = None
	DivMatrix = np.ndarray(shape=(2,2))
	clusters = []


	def __init__(self, k, max_iter, init, precompute, MeanCovMatrix, DivMatrix):
		self.k = k
		self.max_iter = max_iter
		self.init = init
		self.precompute = precompute
		self.MeanCovMatrix = MeanCovMatrix
		self.DivMatrix = DivMatrix

		for x in xrange(k): self.clusters.append([])


	def start_centroids(self):
		badCentroids = 1
		while badCentroids == 1:	
			centroids_init = []
			x = 0
			badCentroids = 0
			if self.init == "random":
				while x < self.k:
					#print(x)									#[DEBUG]
					rand = (int)(random.randint(0, len(self.MeanCovMatrix.table[0]) - 1))
					if rand in centroids_init:
						pass
						#print("random value doubled.")			#[DEBUG]
					else:
						centroids_init.append(rand)
						x += 1
			#print(centroids_init)								#[DEBUG]

			#calculate average of all divmatrix values
			sum = 0
			for x in xrange(len(self.DivMatrix[0])):
				for y in xrange(len(self.DivMatrix[0])): sum += self.DivMatrix[x][y]
			avgDistance = sum / (self.DivMatrix.size)
			#print(avgDistance)									#[DEBUG]

			#ensure that kl-divergence distance between initial centroids is above an arbitrary threshold
			for x in xrange(0, len(centroids_init) - 1):
				for y in xrange(x + 1, len(centroids_init)):
					row = centroids_init[x]
					col = centroids_init[y]
					if self.DivMatrix[row][col] < avgDistance / 2:
						print("Centroids too close together. Restarting...")	#[DEBUG]
						badcentroids = 1

		return centroids_init


	def k_iter(self):	
		# Preprocess: copy current clusters to clusters_old
		clusters_old = list(self.clusters)
		#empty stack from current clusters
		for x in xrange(self.k): self.clusters[x] = []
		#print(clusters_old)												#[DEBUG]
		#print(self.clusters)												#[DEBUG]

		#systematically add each value to the three lists
		for x in xrange(len(self.MeanCovMatrix.table[0])):
			cdist = []
			for y in xrange(self.k):
				cdist.append(self.centroid_distance(clusters_old[y], x))
			#print(cdist)													#[DEBUG]
			#calculate minimum distance between separate bins
			minval = min(cdist)
			minimum = min(enumerate(cdist), key=itemgetter(1))[0]
			#print(minval)													#[DEBUG]
			#print(minimum)													#[DEBUg]
			#add to the list with the smallest distance from centroid
			self.clusters[minimum].append(x)


	def centroid_distance(self, list, point):
		total = 0
		count = 0
		for x in xrange(len(list)):
			total += self.DivMatrix[list[x]][point]
			count += 1
		return total / count


	def run(self):
		initial = self.start_centroids()
		#[DEBUG] check
		for x in xrange(0, len(initial) - 1):
			for y in xrange(x + 1, len(initial)):
				row = initial[x]
				col = initial[y]
				#print "distance from %d to %d: %d" % (row, col, self.DivMatrix[row][col]) #[DEBUG]
		#add initial centroids to each of the three lists
		for x in xrange(self.k): self.clusters[x].append(initial[x])
		
		#start kmeans iteration
		for x in range (0, self.max_iter):
			self.k_iter()
			print(self.clusters)
		return self.clusters


if __name__ == '__main__':
	m = MeanCovMatrix(13)
	d = DivMatrix(13)
	print(m.table[0])
	kmeans = KMeansGaussian(3, 4, "random", False, m, d)
	#kmeans.start_centroids()