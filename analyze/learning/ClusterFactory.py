"""
The MIT License

Copyright (c) 2014 Jacob Reske
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.
"""
import sys, os, glob, logging, copy, math
sys.path.append(os.path.abspath('..'))
from FeatureSet import FeatureSet
from operator import itemgetter
from KMeans import KMeansGaussian, KMeansHeuristic
from features import features


class ClusterFactory:

	current_cluster = []
	featureSet = None
	times = 1
	k = None
	isAutoK = False
	weight = []
	auto_weights = False
	euclidean = False

	def __init__(self, times, featureSet, k, weight, euclidean):
		self.featureSet = featureSet
		self.times = times
		if k == 'auto':
			self.k = 1
			self.isAutoK = True
		else: self.k = k
		self.weight = weight
		if weight == 'auto':
			self.weight = [1] * featureSet.num_features
			self.auto_weights = True
		self.euclidean = euclidean


	#create cluster with parameters defined in ClusterFactory's init
	def create_defaultCluster(self):
		f2 = copy.deepcopy(self.featureSet)
		if self.auto_weights == True:
			return KMeansHeuristic(self.weight, self.k, 20, "random", False, f2, self.euclidean)
		else:
			return KMeansGaussian(self.weight, self.k, 20, "random", False, f2, self.euclidean)


	#create cluster with defined parameters; returns cluster object
	def create_customCluster(self, k, iterations, weight, auto, euclidean):
		f2 = copy.deepcopy(self.featureSet)
		if self.auto_weights == True:
			return KMeansHeuristic(weight, k, iterations, "random", False, f2, euclidean)
		else: return KMeansGaussian(weight, k, iterations, "random", False, f2, euclidean)


	#run cluster; returns cluster[] list
	def run_cluster(self, km):
		print
		print("-------------------------------")
		print
		print("Starting kMeans clustering...")
		self.current_cluster = km.run()
		return self.current_cluster


	#run cluster a number of times; use heuristic to determine "best" cluster result
	#returns cluster[] list
	def iterate_cluster(self, times, km):
		clusterlist = []
		clustercount = []
		for cl in range(0, times):
			print("Iteration #%d" %(cl + 1))
			cluster = self.run_cluster(km)
			cluster = sorted(cluster, key = lambda x: len(x))
			print cluster
			if cluster not in clusterlist:
				clusterlist.append(cluster)
				clustercount.append(1)
			else:
				ind = clusterlist.index(cluster)
				clustercount[ind] += 1
		clustermax = max(enumerate(clustercount), key=itemgetter(1))[0]
		finalcluster = clusterlist[clustermax]
		logging.info(clustercount)
		return finalcluster


	#prints output of given cluster
	def print_cluster(self, cluster):
		print
		for x in xrange(len(cluster)):
			print
			print 'Cluster #%d:' % (x + 1)
			for y in xrange(len(cluster[x])):
				val = cluster[x][y]				
				mp3result = self.featureSet.manifest[val]
				print '%s' % mp3result


	"""Computes the Squared Error Distoriton for a given (finished) KMeans object.
	Squared Error Distortion is defined as follows:
	Let V = {v1, v2,..., vn} be the set of n data points and X be the set of centroids.
	d(vi, X) = min(d(vi, xi)) for xi in X
	the Squared Error Distortion d(V,X) = SUM(d(vi, X)^2) / n for 1 <= i <= n
	"""
	def find_sqe_distortion(self, km):
		n = self.featureSet.filecount
		total = 0
		for cluster_i in xrange(len(km.clusters)):
			for point in km.clusters[cluster_i]:
				distance = km.centroid_distance(km.clusters[cluster_i], point, self.featureSet.weightvector)
				total += math.pow(distance, 2)
				return float(total) / float(n)


	def auto_k(self):
		p = 3
		Y = -float((float(p) / 2))
		D = []
		D.append(0)
		for k in range(1, self.featureSet.filecount / 10):
			print "Iteration: %s" %(k)
			km = self.create_customCluster(k, 5, self.weight, self.auto_k, self.euclidean)
			self.run_cluster(km)
			d = self.find_sqe_distortion(km)
			print "distortion = %f" %(d)
			D.append(float(math.pow(d, Y)))
			print(D)
		J = []
		J.append(0)
		for i in range(1, len(D)):
			J.append(D[i] - D[i - 1])
		maxval = max(J)
		best_k = max(enumerate(J), key=itemgetter(1))[0]
		print(J)
		print "best k = %d" %(best_k)

		bkm = self.create_customCluster(best_k, 20, self.weight, self.auto_k, self.euclidean)
		cluster = self.iterate_cluster(30, bkm)
		return cluster


	"""General runner with init settings.
	"""
	def run_with_settings(self):
		c = self.create_defaultCluster()
		if self.isAutoK == False:
			cluster = self.iterate_cluster(self.times, c)
		else: cluster = self.auto_k()
		self.print_cluster(cluster)



if __name__ == '__main__':
	w = [1, 0, 0]
	k = 10
	fe = features.FEATURE
	times = 100
	mp3dirs = ["5Albums"]

	featureFactory = FeatureFactory(44100, fe, mp3dirs, k, times, False)
	clusterFactory = ClusterFactory(featureFactory.f, k, w)
	c = clusterFactory.create_defaultCluster()
	cluster = clusterFactory.run_cluster(c)
	clusterFactory(print_cluster)


