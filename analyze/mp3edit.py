"""
The MIT License

Copyright (c) 2014 Jacob Reske
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.
"""
import os
import glob
import REMIXanalyzer

syspath = os.path.abspath(os.curdir)
os.chdir(syspath + "../.." + "/mp3")
mp3path = os.path.abspath(os.curdir)

if __name__ == '__main__':
	for file in glob.glob("*.mp3"):
		REMIXanalyzer.playMP3(file)

		

