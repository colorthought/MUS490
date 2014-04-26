"""
The MIT License

Copyright (c) 2014 Jacob Reske
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.
Module: clusterTest.py
"""
import sys, os, glob, argparse, logging
syspath = os.path.dirname(os.path.realpath(__file__))
mp3path = os.path.abspath('../..') + '/mp3'
outputpath = os.path.abspath('..') + '/output'
sys.path.append(os.path.abspath('../analyze'))

from Analyzer import Analyzer
from FeatureFactory import FeatureFactory
from features import features


def test_cluster(w, k, fe, t, auto):
	#check if directory is empty-- should implement try/except later.
	if os.listdir(outputpath):
		finalcluster = FeatureFactory.Cluster_100(fe, k, w, t, auto)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--log')
	args = parser.parse_args()
	if args.log == 'INFO':
		logging.basicConfig(format='%(message)s', level=logging.INFO)
	elif args.log == 'DEBUG':
		logging.basicConfig(format='%(message)s', level=logging.DEBUG)

	#begin basic testing interface and options selector.
	#dataset directory selector and basic directory checker
	dirs_exist = 0
	while (dirs_exist) == 0:
		dirs_exist = 1
		mp3string = raw_input('Enter the filepaths for the mp3 datasets you wish to use.\n'
						'Common dataset names are also acceptable, such as "Jazz" or "5Albums.\n'
						'For multiple datasets, delimit dataset names by spaces: ') or 'Jazz'
		mp3list = mp3string.split(" ")
		print(mp3list)
		for mp3 in xrange(len(mp3list)):
			if mp3list[mp3] == "Jazz" or mp3list[mp3] == "jazz":
				mp3list[mp3] = "Jazz1959"
			if mp3list[mp3] == "5":
				mp3list[mp3] = "5Albums"
			if mp3list[mp3] == "Piano" or mp3list[mp3] == "piano":
				mp3list[mp3] = "ClassicalPiano"
			fullpath = mp3path + '/' + mp3list[mp3]
			if not os.path.exists(fullpath):
				print("ERORR: one of your directory names does not exist!")
				dirs_exist = 0
				mp3list = []
				break
			mp3list[mp3] = fullpath

	#options for FeatureSet
	k = int(raw_input('Number of clusters (k): ') or 10)
	t = int(raw_input('Number of iterations: ') or 1)
	fe = None
	feature = raw_input('FeatureSet?: ') or '1'
	auto = False
	autoselect = raw_input('Auto select weights? [Y/N]: ') or 'N'
	if autoselect == 'Y': auto = True
	if feature == '1':	
		fe = features.FEATURE
	elif feature == '2':
		fe = features.FEATURE2	
	w = [1, 0, 0]
	run_before = raw_input('Ran these features last time? [Y/N]: ') or 'N'
	
	FeatureFactory = FeatureFactory(44100, fe, mp3list)

	if run_before == 'Y':
		test_cluster(w, k, fe, t, auto)
	else:
		FeatureFactory.mp3_to_feature_vectors()
		test_cluster(w, k, fe, t, auto)
