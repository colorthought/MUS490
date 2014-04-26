"""
The MIT License

Copyright (c) 2014 Jacob Reske
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.
"""
import sys, os, glob, copy, argparse, logging
from operator import itemgetter
import numpy as np
from FeatureSet import FeatureSet
from learning.KMeansGaussian import KMeansGaussian, KMeansHeuristic
syspath = os.path.dirname(os.path.realpath(__file__))
mp3path = os.path.abspath('../..') + '/mp3'
outputpath = os.path.abspath('..') + '/output'
sys.path.append(os.path.abspath('..'))

from analyze.Analyzer import Analyzer
from analyze.features import features


class FeatureFactory:
	
	songpath = mp3path
	SAMPLERATE = 22050
	samplerate_alt = 44100
	featureList = features.FEATURE
	num_features = len(featureList)

	def __init__(self, samplerate, featureList):
		self.SAMPLERATE = samplerate
		self.featureList = featureList
		self.num_features = len(featureList)


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
		os.chdir(mp3path)

		#dynamic list of mp3s that generate exceptions with current featureList
		Failedmp3 = []
		i = 0
		for mp3 in glob.glob("*.mp3"):
			if theanalyzer.process_mp3(mp3, df) == False:
				Failedmp3.append(mp3)
				i +=1

		#second attempt with a separate sample rate (soon deprecated)
		try:
			for mp3 in Failedmp3:
				theanalyzer = Analyzer(self.samplerate_alt, self.featureList, True)
				df = theanalyzer.dataFlowCreator()
				theanalyzer.process_mp3(mp3, df)
				i += 1
		except IOError:
			print("that didn't work either...")
		os.chdir(syspath)
		print "wrote %d files." % i


	"""Factory for implementing MFCC-to-divergence-matrix path.
		Deprecated by CreateMeanCovDiv as of 4-23-14
	"""
	def Cluster_100(self, feature, k, weights, times):
		f = FeatureSet(feature)
		f.addAllDivCov()
		w = weights

		clusterlist = []
		clustercount = []		
		for cl in range(0, times):
			w2 = copy.deepcopy(w)
			f2 = copy.deepcopy(f)
			km = KMeansHeuristic(w2, k, 20, "random", False, f2)
			print
			print("-------------------------------")
			print
			print("Starting kMeans clustering...")
			print("iteration #%d" %(cl))
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
		for x in xrange(k):
			print
			print 'Cluster #%d:' % (x + 1)
			for y in xrange(len(finalcluster[x])):
				val = finalcluster[x][y]				
				mp3result = f.manifest[val]
				print '%s' % mp3result
		return finalcluster


if __name__ == '__main__':
	w = [1, 0, 0]
	k = 10
	fe = features.FEATURE

	# test argument parser for debug flags
	parser = argparse.ArgumentParser()
	parser.add_argument('--log')
	args = parser.parse_args()
	if args.log == 'INFO':
		logging.basicConfig(format='%(message)s', level=logging.INFO)
	elif args.log == 'DEBUG':
		logging.basicConfig(format='%(message)s', level=logging.DEBUG)
	FeatureFactory = FeatureFactory(44100, fe)
	FeatureFactory.mp3_to_feature_vectors()
	#check if directory is empty-- should implement try/except later.
	if os.listdir(outputpath):
		finalcluster = FeatureFactory.Cluster_100(fe, k, w)



