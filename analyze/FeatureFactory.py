"""
The MIT License

Copyright (c) 2014 Jacob Reske
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.
Module: FeatureFactory.py
"""
import sys, os, glob, copy, argparse, logging
import os.path
from operator import itemgetter
import numpy as np
from FeatureSet import FeatureSet
from learning.KMeansGaussian import KMeansGaussian, KMeansHeuristic
syspath = os.path.dirname(os.path.realpath(__file__))
outputpath = os.path.abspath('../..') + '/output'
sys.path.append(os.path.abspath('..'))

from analyze.Analyzer import Analyzer
from analyze.features import features


class FeatureFactory:
	
	cluster = []
	SAMPLERATE = 22050
	samplerate_alt = 44100
	mp3dirs = []
	featureList = None
	num_features = 0
	k = 0
	times = 0
	f = None

	def __init__(self, samplerate, featureList, mp3dirs, k, times, run_before):
		self.cluster = []
		self.SAMPLERATE = samplerate
		self.featureList = featureList
		self.num_features = len(featureList)
		self.mp3dirs = mp3dirs
		self.k = k
		self.times = times

		#do mp3_to_feature_vectors and brand new FeatureSet object if this is a new dataset/feature combo
		if run_before == False:
			self.mp3_to_feature_vectors()
			self.f = FeatureSet(self.featureList, False)
		#else skip conversion, load from file
		else:
			self.f = FeatureSet(self.featureList, True)


	"""Generic factory function for generating feature datafiles (.csv) using Analyzer.py.
	featureList and SAMPLERATE required.
	"""
	def mp3_to_feature_vectors(self):
		#checks for and removes existing feature vector files
		os.chdir(outputpath)
		fileList = glob.glob("*.csv")
		for f in fileList:
			os.remove(f)
		#new generic Analyzer and dataflow
		theanalyzer = Analyzer(self.SAMPLERATE, self.featureList, True)
		df = theanalyzer.dataFlowCreator()
		
		failed_mp3 = []
		failed_dir = []
		i = 0
		for path in self.mp3dirs:
			logging.info("Changed path: %s"%(path))
			for dirpath, dirnames, filenames in os.walk(path):
				for filename in [f for f in filenames if f.endswith(".mp3")]:
					os.chdir(dirpath)
					if theanalyzer.process_mp3(filename, df) == False:
						failed_mp3.append(filename)
					i +=1
		#second attempt with a separate sample rate (soon deprecated)
		"""
		try:
			for filename in xrange(len(failed_mp3)):
				os.chdir(failed_dir[filename])
				theanalyzer = Analyzer(self.samplerate_alt, self.featureList, True)
				df = theanalyzer.dataFlowCreator()
				theanalyzer.process_mp3(failed_mp3[filename], df)
				i += 1
		except IOError:
			print("that didn't work either...")
		"""
		os.chdir(syspath)
		print "wrote %d files." % i


	"""Factory function for implementing MFCC-to-divergence-matrix path.
		Deprecated by CreateMeanCovDiv as of 4-23-14
	"""
	def cluster_100(self, weights, auto):
		w = weights
		self.f.updateWeights(w)

		clusterlist = []
		clustercount = []
		for cl in range(0, self.times):
			w2 = copy.deepcopy(w)
			f2 = copy.deepcopy(self.f)
			km = KMeansGaussian(self.k, 20, "random", False, f2)
			if auto == True:
				km = KMeansHeuristic(w2, self.k, 20, "random", False, f2)
			print
			print("-------------------------------")
			print
			print("Starting kMeans clustering...")
			print("Iteration #%d" %(cl + 1))
			clusters = km.run()
			if clusters not in clusterlist:
				clusterlist.append(clusters)
				clustercount.append(1)
			else:
				ind = clusterlist.index(clusters)
				clustercount[ind] += 1
		clustermax = max(enumerate(clustercount), key=itemgetter(1))[0]
		finalcluster = clusterlist[clustermax]
		logging.info(clustercount)

		print
		for x in xrange(self.k):
			print
			print 'Cluster #%d:' % (x + 1)
			for y in xrange(len(finalcluster[x])):
				val = finalcluster[x][y]				
				mp3result = self.f.manifest[val]
				print '%s' % mp3result
		this.cluster = finalcluster
		return finalcluster


if __name__ == '__main__':
	w = [1, 0, 0]
	k = 10
	fe = features.FEATURE
	times = 100
	mp3dirs = ["5Albums"]

	# test argument parser for debug flags
	parser = argparse.ArgumentParser()
	parser.add_argument('--log')
	args = parser.parse_args()
	if args.log == 'INFO':
		logging.basicConfig(format='%(message)s', level=logging.INFO)
	elif args.log == 'DEBUG':
		logging.basicConfig(format='%(message)s', level=logging.DEBUG)
	FeatureFactory = FeatureFactory(44100, fe, mp3dirs, k, times, False)
	
	#check if directory is empty-- should implement try/except later.
	if os.listdir(outputpath):
		finalcluster = FeatureFactory.cluster_100(w, False)
