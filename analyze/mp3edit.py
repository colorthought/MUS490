"""
The MIT License

Copyright (c) 2014 Jacob Reske
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.
"""
import os, glob
from mutagen.id3 import ID3, TRCK, TIT2, TPE1, TALB, TDRC, TCON, COMM

syspath = os.path.abspath(os.curdir)
os.chdir(syspath + "/../.." + "/mp3")


def get_mp3_title(mp3):
	return 1


def get_mp3_artist(mp3):
	audio = ID3(mp3)
	genre = audio.getall('TIT2:Artist')
	print(genre)

def get_mp3_genre(mp3):
	return 1

if __name__ == '__main__':
	for file in glob.glob("*.mp3"):
		get_mp3_artist(file)
		#REMIXanalyzer.playMP3(file)

		

