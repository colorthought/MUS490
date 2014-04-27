"""
The MIT License

Copyright (c) 2014 Jacob Reske
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.
"""
import sys, os, glob, logging, copy
sys.path.append(os.path.abspath('..'))
from FeatureSet import FeatureSet
from operator import itemgetter
from KMeansGaussian import KMeansGaussian, KMeansHeuristic
from features import features


class ClusterFactory:

	current_cluster = []
	featureSet = None
	k = 0
	auto_k = False
	weight = []
	auto_weights = False
	euclidean = False

	def __init__(self, featureSet, k, weight, euclidean):
		self.featureSet = featureSet
		self.k = k
		if k == 'auto':
			self.auto_k = True
		self.weight = weight
		if weight == 'auto':
			self.auto_weights = True
		self.euclidean = euclidean


	#create cluster with parameters defined in ClusterFactory's init
	def create_defaultCluster(self):
		f2 = copy.deepcopy(self.featureSet)
		if self.auto_weights == True:
			return KMeansHeuristic(self.weight, self.k, 20, "random", False, f2, self.euclidean)
		else:
			return KMeansGaussian(self.k, 20, "random", False, f2, self.euclidean)


	#create cluster with defined parameters; returns cluster object
	def create_customCluster(self, k, weight, auto, euclidean):
		f2 = copy.deepcopy(self.featureSet)
		if auto_weights == True:
			return KMeansHeuristic(weight, k, 20, "random", False, f2, euclidean)
		else: return KMeansGaussian(k, 20, "random", False, f2, euclidean)


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
	def iterate_cluster(self, times):
		clusterlist = []
		clustercount = []
		for cl in range(0, times):
			km = self.create_defaultCluster()
			print("Iteration #%d" %(cl + 1))
			cluster = self.run_cluster(km)
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
	def print_cluster(self):
		print
		for x in xrange(self.k):
			print
			print 'Cluster #%d:' % (x + 1)
			for y in xrange(len(self.current_cluster[x])):
				val = self.current_cluster[x][y]				
				mp3result = self.featureSet.manifest[val]
				print '%s' % mp3result


	#returns the distortion value of a given cluster
	def find_distortion(self):
		return 1		

	def auto_k(self):
		return 1


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


