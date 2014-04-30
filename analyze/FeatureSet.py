"""
The MIT License

Copyright (c) 2014 Jacob Reske.
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.
"""
import sys, os, glob, logging, copy, csv
import numpy as np
from numpy import linalg as LA
from MeanCovMatrix import MeanCovMatrix
import stats
from features import features
syspath = os.path.dirname(os.path.realpath(__file__))
outputpath = syspath + '/../..' + '/output'
featurepath = os.path.abspath(outputpath) + '/features'

class FeatureSet(list):

	manifest = []
	filecount = 0
	featureList = None
	num_features = 0
	weightvector = []
	#DefaultMeanCovMatrix = None
	DefaultDivMatrix = None

	def __init__(self, featureList, fromFile):
		#append list for every feature in featureList and populates with featurenames
		self.featureList = featureList
		self.num_features = len(featureList)
		#print "NumFeatures: %d" % self.num_features
		for x in xrange(self.num_features):
			self.append([])
			self[x] = []
			featurename = features.getExtension(self.featureList, x)
			self[x].append(featurename)
			self[x].append(1)
			#self[x].append(copy.deepcopy(self.DefaultMeanCovMatrix))
			self[x].append(copy.deepcopy(self.DefaultDivMatrix))

			if fromFile == True:
				os.chdir(featurepath)
				with open(featurename + '.csv') as f:
					div = np.genfromtxt(f, delimiter=',')
					self[x][2] = div
					print(self[x][2])
		if fromFile == True:
			self.manifestFromFile()
		else:
			self.addAllDivCov()
			self.writeToFile()

		#populates weight vector with 1/num_features by default
		if not self.weightvector:
			for x in xrange(self.num_features):
				self.weightvector.append(float(1) / float(self.num_features))
			self.updateWeights(self.weightvector)


	"""Changes weight vectors and adds them to FeatureSet accordingly.
		If any (formerly) zero vectors are changed to nonzero, issues warning and updates FeatureSet.
	"""
	def updateWeights(self, vector):
		#copies old weightvector into storage for later compare
		wv_old = self.weightvector
		if len(vector) != len(self.featureList):
			print("Error: Weight vector not the same length as featureList!")
			return 0
		
		#adds weights to FeatureList proper
		self.weightvector = vector
		for x in xrange(len(vector)):
			self[x][1] = self.weightvector[x]
			if wv_old[x] == 0 and self.weightvector[x] != 0:
				print("Updated weights requires new div/cov calculation. Working...")
				if self.addDivCov(x) == 1:
					print("Successfully added new weights.")
				else: print("FLAG: UNSUCCESSFUL.")
		return 1


	"""Brief check on DivMatrix dimensions and manifest size.
	"""
	def isValid(self):
		#print(self)
		try:
			size_old = self[0][2].size
		except: return False
		for x in xrange(self.num_features):
			size_new = self[x][2].size
			if size_old != size_new: return False
			size_old = size_new 
		return True


	"""Adds all Mean, Covariance, and Divergence matrixes to the FetureSet object.
	"""
	def addAllDivCov(self):
		for x in xrange(len(self)):
			logging.info("Now Processing feature: %s"%(self[x][0]))
			if self.addDivCov(x) == 0: print("Weight of 0 detected; skipping DivCov creation")
		return 1


	"""adds Mean, Covariance, and Divergence matrices of index to the FeatureSet object.
		skips any features with weights of zero.
	"""
	def addDivCov(self, index):
		if self[index][1] == 0:
			return 0
		cov, div = self.CreateMeanCovDiv(index)
		#self[index][2] = cov
		self[index][2] = div
		return 1


	"""Factory function for obtaining mean, covariance, and divergence matrices from a 
		generic feature in a featurelist.
		Replaces cluster_100 as of 4-23-14
	"""
	def CreateMeanCovDiv(self, featureIndex):
		featurename = self[featureIndex][0]
		#counts number of feature files for c
		featurecount = self.countfeatureFiles(featurename)
		
		meancovmatrix = MeanCovMatrix(featurecount)
		#for each datafile, opens and creates mean and cov matrices, adds mp3 names to table.	
		i = 0
		for file in glob.glob("*.mp3." + featurename + ".csv"):
			f = file.split('.mp3')
			filename = f[0]
			self.manifest[i] = filename
			print(filename)
			meancovmatrix.addmp3ToTable(i, filename)
			mean, cov = stats.csvToMeanCovariance(file)
			meancovmatrix.addToTable(i, mean, cov)
			#logging.debug('%d' % mean)									#[DEBUG]
			#logging.debug('%d' % cov)									#[DEBUG]
			i += 1
		#creates empty Divergence Matrix and populates it with kl-divergence tests
		divMatrix = np.zeros(shape=(featurecount, featurecount))

		#populating divergence matrix
		for row in xrange(featurecount):
			for col in xrange(featurecount):
				mean1, cov1 = meancovmatrix.recallfromTable(row)
				mean2, cov2 = meancovmatrix.recallfromTable(col)
				divergence = stats.kl_DivergenceSymm(mean1, cov1, mean2, cov2)
				divMatrix[row][col] = divergence
		norm = LA.norm(divMatrix, 2)
		divMatrix = divMatrix * float(1/ float(norm))

		#int(divergence * 100)

		logging.debug(divMatrix)
		return meancovmatrix, divMatrix
	

	"""Counts number of datafiles for current feature. Used mostly for debugging.
	Also resets manifest. 
	"""
	def countfeatureFiles(self, featurename):
		filecount = 0
		os.chdir(outputpath)
		for file in glob.glob("*.mp3." + featurename + ".csv"):
			filecount += 1
		logging.info('there are %d files to be processed.' % filecount)
		self.filecount = filecount
		self.manifest = ["Null"] * filecount
		return filecount


	"""Defines manifest[] and filecount from file
	"""
	def manifestFromFile(self):
		#clears active manifest and filecount
		self.manifest = []
		self.filecount = 0
		os.chdir(featurepath)
		with open("manifest") as m:
			self.manifest = m.read().splitlines()
			self.filecount = len(self.manifest)


	"""Averages the values of all rows and columns of the DivMatrix.
	Used in KMeansHeuristic and KMeansGaussian to select random points with a minumum distance heuristic.
	"""
	def divMatrixAvg(self, featureIndex):
		#calculate average of all divmatrix values
		div = self[featureIndex][2]
		sum = 0
		for x in xrange(len(div[0])):
			for y in xrange(len(div[0])): sum += div[x][y]
		avgDistance = sum / (div.size)
		#print(avgDistance)									#[DEBUG]
		return avgDistance


	"""Implements writing FeatureSet to files.
	 Useful for running clustering on file-feature combos that have been attempted before.
	 """
	def writeToFile(self):
		#removes all prior features in featurepath
		try:
			os.chdir(featurepath)
			fileList = glob.glob("*.csv")
			for f in fileList:
				os.remove(f)
			#for each feature, write a different file
			for feature in xrange(self.num_features):
				featurename = self[feature][0]
				div = self[feature][2]
				np.savetxt(featurename + '.csv', div, delimiter=',')
			#writes file manifest as manifest.csv
			with open('manifest', 'w') as f:
				for item in self.manifest:
					f.write("%s\n" % item)
			return True
		except:
			print("ERROR: IO issue [DEBUG]")


if __name__ == '__main__':
	f = FeatureSet(features.FEATURE, True)
	w = [.2, .3, .5]
	f.updateWeights(w)
	print(f.isValid())

"""
	COL
ROW	feature 	Weight		DivMatrix             (#MeanCovMatrix no longer stored)
"""