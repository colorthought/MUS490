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
from learning.KMeans import KMeansGaussian, KMeansHeuristic
from learning.ClusterFactory import ClusterFactory
syspath = os.path.dirname(os.path.realpath(__file__))
outputpath = syspath + '/../..' + '/output'
sys.path.append(os.path.abspath('..'))

from Analyzer import Analyzer
from features import features


class FeatureFactory:
	
	cluster = []
	SAMPLERATE = 22050
	samplerate_alt = 44100
	mp3dirs = []
	featureList = None
	num_features = 0
	k = None
	times = 1
	f = None
	euclidean = False

	def __init__(self, samplerate, featureList, mp3dirs, k, times, run_before, euclidean):
		self.cluster = []
		self.SAMPLERATE = samplerate
		self.featureList = featureList
		self.num_features = len(featureList)
		self.mp3dirs = mp3dirs
		self.k = k
		self.times = times
		self.euclidean = euclidean

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
					i += 1
		os.chdir(syspath)
		print "wrote %d files." % i


	"""Factory function for implementing MFCC-to-divergence-matrix path.
		Deprecated by CreateMeanCovDiv as of 4-23-14
	"""
	def cluster_100(self, weights, auto):
		clusterFactory = ClusterFactory(self.times, self.f, self.k, weights, self.euclidean)
		clusterFactory.run_with_settings()


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
