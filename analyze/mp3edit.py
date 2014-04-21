import os
import glob
import REMIXanalyzer

syspath = os.path.abspath(os.curdir)
os.chdir(syspath + "/mp3")
mp3path = os.path.abspath(os.curdir)

if __name__ == '__main__':
	for file in glob.glob("*.mp3"):
		REMIXanalyzer.playMP3(file)

		

