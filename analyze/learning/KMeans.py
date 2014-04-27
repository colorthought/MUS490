"""
The MIT License

Copyright (c) 2014 Jacob Reske
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.
"""
import sys, os, random, logging, copy, math
from operator import mul
from fractions import Fraction
import numpy as np
from operator import itemgetter
sys.path.append(os.path.abspath('..'))
from FeatureSet import FeatureSet


class KMeansGaussian():

	k = 3
	max_iter = 20
	init = "random"
	clusters = []
	precompute = False
	featureSet = None
	euclidean = False

	def __init__(self, k, max_iter, init, precompute, featureSet, euclidean):
		self.k = k
		self.max_iter = max_iter
		self.init = init
		self.precompute = precompute
		self.featureSet = featureSet
		self.clusters = []
		self.euclidean = euclidean

		for x in xrange(k): self.clusters.append([])


	"""Initializes centroids to a random set of k vectors in R[n].
	init = "random" picks random centroids and checks their distance against a threshold. (Default: average value of all dimensions)
	init = "weighted" to be built soon.
	"""
	def start_centroids(self):
		if (self.k > self.featureSet.filecount - 1):
			print("Error: More centroids than files!")
			sys.exit(0)
		badCentroids = 1
		while badCentroids == 1:	
			centroids_init = []
			x = 0
			badCentroids = 0
			if self.init == "random":
				#choose a set of k random values
				while x < self.k:
					#print(x)									#[DEBUG]
					rand = (int)(random.randint(0, self.featureSet.filecount - 1))
					if rand in centroids_init:
						pass
						#print("random value doubled.")			#[DEBUG]
					else:
						centroids_init.append(rand)
						x += 1
			#print(centroids_init)								#[DEBUG]

			#ensure that kl-divergence distance between initial centroids is above avg distance for each feature
			for feature in xrange(self.featureSet.num_features):
				avgDistance = self.featureSet.divMatrixAvg(feature)

				for x in xrange(0, len(centroids_init) - 1):
					for y in xrange(x + 1, len(centroids_init)):
						row = centroids_init[x]
						col = centroids_init[y]
						if self.featureSet[feature][2][row][col] < avgDistance / 2:
							#print("Centroids too close together. Restarting...")	#[DEBUG]
							badcentroids = 1
				if badCentroids == 1: break
		return centroids_init


	"""Main iteration function for KMeans algorithm.
	"""
	def k_iter(self):	
		# Preprocess: copy current clusters to clusters_old
		clusters_old = list(self.clusters)

		#empty stack from current clusters
		for x in xrange(self.k): self.clusters[x] = []

		#systematically add each value to the three lists
		for x in xrange(self.featureSet.filecount):
			cdist = []
			for y in xrange(self.k):
				cdist.append(self.centroid_distance(clusters_old[y], x, self.featureSet.weightvector))								#WARNING REFERENCES WEIGHTVECTOR!
			logging.debug(cdist)													#[DEBUG]

			#calculate minimum distance between separate bins
			minval = min(cdist)
			minimum = min(enumerate(cdist), key=itemgetter(1))[0]

			#add to the list with the smallest distance from centroid
			self.clusters[minimum].append(x)


	"""Calculates centroid distance for a given dimension.
	Since each DivMatrix point is a gaussian distance, the centroid itself is implicit. The formula for distance to an implicit centroid is:
	For cluster X (x1, x2,...,xn), Centroid C, and point Y,
		Distance (Y, C) = [SUM (Distance (Y, xi))] / n for all xi in X 
	The distance between two points (the weighted average of all DivMatrix distances) is calculated in distance() below.
	"""
	def centroid_distance(self, cluster, point, weight):
		total = 0
		clusterCount = 0
		for x in xrange(len(cluster)):
			if self.euclidean == True: total += self.euclideanAvgDistance(point, cluster[x], weight)
			else: total += self.avgDistance(point, cluster[x], weight)
			clusterCount += 1
		return total / clusterCount


	"""Calculates the "distance" between two given points using the FeatureSet object.
	The distance between points x1 and x2 is defined as the weighted average of each feature's DivMatrix(x1, x2) compare.
	"""
	def avgDistance(self, x1, x2, weights):
		dist = 0
		for i in xrange(self.featureSet.num_features):
			div = self.featureSet[i][2]
			dist += float(div[x1][x2]) * weights[i]
		return dist


	"""Euclidean version of avgDistance function above.
	"""
	def euclideanAvgDistance(self, x1, x2, weights):
		dist = 0
		for i in xrange(self.featureSet.num_features):
			div = self.featureSet[i][2]
			dist += math.pow(float(div[x1][x2] * float(weights[i])), 2)
		return math.sqrt(dist)


	"""Run function for simple version of KMeansGaussian algorithm
	"""
	def run(self):
		self.clusters = []
		for x in xrange(self.k): self.clusters.append([])

		initial = self.start_centroids()
		#add initial centroids to each of the three lists
		for x in xrange(self.k): self.clusters[x].append(initial[x])

		#start kmeans iteration
		for x in range (0, self.max_iter):
			self.k_iter()
			for cluster_i in self.clusters:
				#accounts for empty clusters by reconfiguring
				if not cluster_i:
					unique = 0
					while (unique == 0):
						rand = (int)(random.randint(0, len(self.clusters) - 1))
						takecluster = self.clusters[rand]
						if takecluster != cluster_i and takecluster:
							unique = 1
							cluster_i.append(takecluster[0])
							self.clusters[rand].remove
			logging.info(self.clusters)
		return self.clusters


"""
Experimental Heuristic for low-dim clustering:
In each round of clustering [!],
	For each Cluster that exists,
		Pick from a list of flows between weights of distance 1/num_features.
		For each weight value,
			Run the algorithm and see which points you would win.
			That weight's score is the avg distance of points won LESS than the avg distances 
			of those points to all other clusters with the same weights.
		Pick the weight with the greatest score for that cluster
	Run the clustering algorithm where the weight vector is different for every existing cluster
"""
class KMeansHeuristic(KMeansGaussian):

	defaultWeight = None

	def __init__(self, weightvec, k, max_iter, init, precompute, featureSet, euclidean):
		KMeansGaussian.__init__(self, k, max_iter, init, precompute, featureSet, euclidean)
		weight = Weight(weightvec)
		weight.gen_subsets()
		weight.clear_weightscore()
		self.defaultWeight = copy.deepcopy(weight)


	"""Main iteration function for KMeans heuristic.
	Overrides super(KMeansHeuristic, self).k_iter()
	"""
	def k_iter(self):	
		# Preprocess: copy current clusters to clusters_old
		clusters_old = list(self.clusters)
		#empty stack from current clusters
		for x in xrange(self.k): self.clusters[x] = []
		#create list for finalWeights and initialize
		logging.debug("defaultWeight:")
		logging.debug(self.defaultWeight)
		finalw = [0] * self.defaultWeight.weightlength
		finalweights = [copy.deepcopy(finalw)] * self.k
		#for each cluster that exists,
		for cluster_i in xrange(self.k):
			weights = copy.deepcopy(self.defaultWeight)
			#for each weight in the list of subsets:
			logging.debug("Number of subsets: %d" %(weights.get_num_subets()))
			for weight_i in xrange(weights.get_num_subets()):
				#print "Weight #%d" %(cluster_i)
				score = 0
				#create copies of self.clusters and clusters_old
				c_new = copy.deepcopy(self.clusters)
				c_old = copy.deepcopy(clusters_old)
				#systematically add each value to the three lists
				for x in xrange(self.featureSet.filecount):
					cdist = []
					for y in xrange(self.k):
						cdist.append(self.centroid_distance(c_old[y], x, weights.get_subset(weight_i)))
					#logging.debug(cdist)													#[DEBUG]
					#calculate minimum distance between separate bins
					minval = min(cdist)
					minimum = min(enumerate(cdist), key=itemgetter(1))[0]
					#add to the list with the smallest distance from centroid
					c_new[minimum].append(x)
					#update score if we added to our current cluster.
					if minimum == cluster_i: score += 1
				#update weightscore
				weights.update_weightscore(weight_i, score)
			logging.debug("Weightscore:")
			logging.debug(weights.get_all_weightscore())
			minindex = max(enumerate(weights.get_all_weightscore()), key=itemgetter(1))[0]
			finalweights[cluster_i] = weights.get_subset(minindex)
		logging.debug("Final weights:")
		logging.debug(finalweights)
		#now run the main k_iter algorithm with the filled-out finalweights
		for x in xrange(self.featureSet.filecount):
			cdist = []
			for cluster_i in xrange(self.k):
				cdist.append(self.centroid_distance(clusters_old[cluster_i], x, finalweights[cluster_i]))
			#logging.debug(cdist)													#[DEBUG]
			#calculate minimum distance between separate bins
			minval = min(cdist)
			minimum = min(enumerate(cdist), key=itemgetter(1))[0]
			#add to the list with the smallest distance from centroid
			self.clusters[minimum].append(x)


"""Weight object.
	Given a weight set of lenght n, can generate a list of SUM(n:k)(k=1, n) subsets, all of length 1
	Needs: list of length weightlength
"""
class Weight:

	weight = []
	weightlength = 0
	weightscore = []
	subsets = []
	subsetlength = 0

	def __init__(self, weight):
		self.weight = weight
		self.weightlength = len(weight)
		self.subsets = []
		self.subsetlength = 0
		self.weightscore = []
		self.clear_weightscore()


	"""Checks that all weight vectors sum to 1 for weight and all subsets.
	"""
	def check(self):
		if not self.weight or sum(self.weight) != 1:
			return False
		for x in self.subsets:
			s = sum(x)
			if round(s, 2) != round(1, 2): 
				return False
		return True


	"""Populates list of random weight subsets for given weight.
		Experimental; Monte Carlo Method for finding weight subsets.
	""" 
	def gen_subsets(self):
		slength = 0
		length = self.weightlength
		#placing x weights down per cycle 
		for x in range(1, length + 1):
			wvalue = float(1) / float(x)
			w = [0] * length
			#initialize default subset 
			for i in xrange(x):
				w[i] = wvalue
			#shuffle n choose k times * 2; Monte Carlo
			for i in xrange(3 * self.n_choose_k(length, x)):
				w_new = copy.deepcopy(w)
				random.shuffle(w_new)
				if w_new not in self.subsets:
					self.subsets.append(w_new)
					slength += 1
		self.subsetlength = slength


	"""Returns the length of subsets[].
	"""
	def get_num_subets(self):
		return self.subsetlength


	"""Returns the subset of index in Weight object.
	"""
	def get_subset(self, index):
		return self.subsets[index]


	"""Returns List object that contains all subsets generated so far.
	"""
	def get_allsubsets(self):
		return self.subsets


	"""Resets weightscore (necessary if kmeans does multiple iterations).
	"""
	def clear_weightscore(self):
		self.weightscore = [0] * self.get_num_subets()


	"""Takes List object of length = weightlength and replaces weightscore.
	"""
	def update_all_weightscore(self, weightscore_new):
		if len(weightscore_new) != len(self.weightscore):
			print("ERROR: new weightscore's length does not equal new!")
			return False
		self.weightscore = weightscore_new
		return True


	"""Updates weightscore with a given value.
	"""
	def update_weightscore(self, index, value):
		self.weightscore[index] = value


	"""Returns weightscore at a given index.
	"""
	def get_weightscore(self, index):
		return self.weightscore[index]


	"""Returns list of all given weightscores.
	"""
	def get_all_weightscore(self):
		return self.weightscore


	"""Quick formula to calculate binomial coefficients (N, k)
	"""
	def n_choose_k(self, N, k): 
  		return int( reduce(mul, (Fraction(N-i, i+1) for i in range(k)), 1) )

