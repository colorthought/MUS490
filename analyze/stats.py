"""
The MIT License

Copyright (c) 2014 Jacob Reske
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.
"""
import sys, os, csv, logging
import numpy as np
from numpy import linalg as LA
outputPath = os.path.abspath('../..') + '/output'


def csvToMatrix(filename):
	matrix = np.genfromtxt(outputPath + '/' + filename, dtype=float, delimiter=',', skiprows=5)
	return matrix


def matrixToMeanCovariance(matrix):
	#matrix = np.absolute(matrix)
	mean = np.mean(matrix, axis=0)
	covariance = np.cov(matrix, y=None, rowvar=0, bias=0, ddof=None)

	#check that all eigenvalues are positive? THIS IS A HACK. BE VERY ASHAMED.
	w, v = LA.eig(covariance)
	EPS = .000001
	error = 0
	for i in xrange(len(w)):
		if w[i] <= 0:
			error = 1
			w[i] = EPS
	diag = np.diag(w)
	if error == 1:
		newcov1 = np.multiply(v, diag)
		newcov = np.multiply(newcov1, np.transpose(v))
		covariance = newcov
	logging.debug(covariance)
	return (mean, covariance)


def csvToMeanCovariance(filename):
	matrix = csvToMatrix(filename)
	mean, covariance = matrixToMeanCovariance(matrix)
	return mean, covariance


def rmsError(mean1, cov1, mean2, cov2):
	return 1


def expectedLoglikelihood(mean1, cov1, mean2, cov2):
	return 1



"""Code inspired by Kulback-Liebler implementation in monomvm, a multivariate R package.
Translated with permission.
Copyright (C) 2007, University of Cambridge

:param mean1: mean vector of first Gaussian
:param cov1: covariance matrix of first Gaussian
:param mean2: mean vector of second Gaussian
:param cov2: covariance matrix of second Gaussian
"""
def kl_Divergence(mean1, cov1, mean2, cov2):
	N = mean1.size
	#check length of the mean vectors
	if N != mean2.size:
		raise Exception("Mean sizes do not match!")
	#check that cov matrices have the same length as the mean
	if cov1.shape[0] != N or cov1.shape[1] != N:
		raise Exception("cov1 sizes do not equal mean length!")
	if cov2.shape[0] != N or cov2.shape[1] != N:
		raise Exception("cov2 sizes do not equal mean length!")

	#return Cholesky decompositions for covariance matrices
	chol1 = np.linalg.cholesky(cov1)
	chol2 = np.linalg.cholesky(cov2)
	#begin distance calculation
	ld1 = 2 * np.sum(np.log10(np.diagonal(chol1)), axis=0)
	ld2 = 2 * np.sum(np.log10(np.diagonal(chol2)), axis=0)

	#calculate det
	ldet = ld2 - ld1
	#inverse from Cholesky decomposition
	S1i = np.dot((np.linalg.inv(np.transpose(chol1))), np.linalg.inv(chol1))
	tr = np.sum(np.diagonal(np.dot(S1i, cov2)), axis=0)
	m2mm1 = np.subtract(mean2, mean1)
	
	#asNumeric equivalent in python...
	qf = np.dot(np.transpose(m2mm1), np.dot(S1i, m2mm1))
	r = 0.5 * (ldet + tr + qf - N)
	return r


"""Sums Kulback-Liebler divergence values for both mean and covariance matrices,
to account for KL-divergence being asymmetric (KL(S1, S2) != KL(S2, S1))
Used to more accurately approximate distance of Gaussians.
"""
def kl_DivergenceSymm(mean1, cov1, mean2, cov2):
	return kl_Divergence(mean1, cov1, mean2, cov2) + kl_Divergence(mean2, cov2, mean1, cov1)


if __name__ == '__main__':
	mean1, cov1 = csvToMeanCovariance("TRAAAAV128F421A322.mp3.mfcc.csv")
	mean2, cov2 = csvToMeanCovariance("TRAAAIC128F14A5138.mp3.mfcc.csv")
	mean3, cov3 = csvToMeanCovariance("TRAAAOF128F429C156.mp3.mfcc.csv")
	result1 = kl_DivergenceSymm(mean1, cov1, mean2, cov2)
	result2 = kl_DivergenceSymm(mean2, cov2, mean3, cov3)
	result3 = kl_DivergenceSymm(mean1, cov1, mean3, cov3)
	result4 = kl_DivergenceSymm(mean1, cov1, mean1, cov1)

	print(result1)
	print(result2)
	print(result3)
	print(result4)