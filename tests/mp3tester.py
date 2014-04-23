import sys, os, glob
syspath = os.path.dirname(os.path.realpath(__file__))
mp3path = os.path.abspath('../..') + '/mp3'
sys.path.append(os.path.abspath('..'))

from analyze.Analyzer import Analyzer
from analyze.features import mfcc_1

def test_all_mp3():
	featureList = mfcc_1.FEATURE
	theanalyzer = Analyzer(22050, featureList, True)
	df = theanalyzer.dataFlowCreator()
	os.chdir(mp3path)
	Failedmp3 = []
	for mp3 in glob.glob("*.mp3"):
		if theanalyzer.process_mp3(mp3, df) == False:
			Failedmp3.append(mp3)

	try:
		for mp3 in Failedmp3:
			theanalyzer = Analyzer(44100, featureList, True)
			df = theanalyzer.dataFlowCreator()
			theanalyzer.process_mp3(mp3, df)
	except IOError:
		print("that didn't work either...")


if __name__ == '__main__':
	test_all_mp3()