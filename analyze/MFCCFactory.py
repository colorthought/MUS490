"""
The MIT License

Copyright (c) 2014 Jacob Reske
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.
"""
import sys, os, glob, argparse, logging
import numpy as np
import stats
from MeanCovMatrix import MeanCovMatrix
from learning.KMeansGaussian import KMeansGaussian
from features import mfcc_1
syspath = os.path.dirname(os.path.realpath(__file__))
mp3path = os.path.abspath('../..') + '/mp3'
MFCCpath = os.path.abspath('..') + '/output'
sys.path.append(os.path.abspath('..'))

from analyze.Analyzer import Analyzer
from analyze.features import mfcc_1


class MFCCFactory:
	
	songpath = mp3path
	SAMPLERATE = 22050
	samplerate_alt = 44100
	featureList = mfcc_1.FEATURE

	def __init__(self, samplerate):
		self.SAMPLERATE = samplerate


	"""Simple factory for conversion of imput mp3 list to MFCC .csv files.
	"""
	def allmp3_to_MFCC(self):
		os.chdir(MFCCpath)
		MFCClist = glob.glob("*.csv")
		for f in MFCClist:
			os.remove(f)
		theanalyzer = Analyzer(self.SAMPLERATE, self.featureList, True)
		df = theanalyzer.dataFlowCreator()
		os.chdir(mp3path)
		Failedmp3 = []
		i = 0
		for mp3 in glob.glob("*.mp3"):
			if theanalyzer.process_mp3(mp3, df) == False:
				Failedmp3.append(mp3)
				i +=1

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
		Calls MeanCovMatrix and DivMatrix for output.
	"""
	def allMFCC_to_DivergenceMatrix(self, k):
		mp3count = 0
		os.chdir(MFCCpath)
		for file in glob.glob("*.mp3.mfcc.csv"):
			mp3count += 1
		logging.info('there are %d files to be processed.' % mp3count)
		meancovmatrix = MeanCovMatrix(mp3count)
		
		#adding mp3 names, mean, and cov matrices to table
		i = 0
		for file in glob.glob("*.mp3.mfcc.csv"):
			meancovmatrix.addmp3ToTable(i, file)
			mean, cov = stats.csvToMeanCovariance(meancovmatrix.table[0][i])
			meancovmatrix.addToTable(i, mean, cov)
			#logging.debug('%d' % mean)									#[DEBUG]
			#logging.debug('%d' % cov)									#[DEBUG]
			i +=1

		divMatrix = np.zeros(shape=(mp3count, mp3count))
		#[DEBUG]
		#for i in xrange(mp3count):
		#	(meancovmatrix.table[0][i])

		#populating divergence matrix
		for row in xrange(mp3count):
			for col in xrange(mp3count):
				mean1, cov1 = meancovmatrix.recallfromTable(row)
				mean2, cov2 = meancovmatrix.recallfromTable(col)

				divergence = stats.kl_DivergenceSymm(mean1, cov1, mean2, cov2)
				div_format = abs(int(divergence * 100))
				divMatrix[row][col] = div_format

		#[DEBUG] check for asymmetries in divergence Matrix
		#print(divMatrix)
		km = KMeansGaussian(k, 20, "random", False, meancovmatrix, divMatrix)
		clusters = km.run()
		for x in xrange(k):
			print
			logging.info('Cluster #%d:' % (x + 1))
			for y in xrange(len(clusters[x])):
				val = clusters[x][y]
				mp3result = meancovmatrix.table[0][val]
				logging.info('%s' % mp3result)
		print

if __name__ == '__main__':
	# test argument parser for debug flags
	parser = argparse.ArgumentParser()
	parser.add_argument('--log')
	args = parser.parse_args()
	if args.log:
		logging.basicConfig(format='%(message)s', level=logging.DEBUG)

	mfccfactory = MFCCFactory(44100)
	mfccfactory.allmp3_to_MFCC()
	#check if directory is empty-- should implement try/except later.
	if os.listdir(MFCCpath):
		mfccfactory.allMFCC_to_DivergenceMatrix(10)

