"""
The MIT License

Copyright (c) 2014 Jacob Reske
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.
"""
import echonest.remix.audio as audio
import os

syspath = os.path.abspath(os.curdir)
os.chdir("..")
mp3path = os.path.abspath(os.curdir) + + '/../' + '/mp3'

def playMP3(songID):
	mp3 = mp3path + "/" + songID
	
	audio_file = audio.LocalAudioFile(mp3)
	beats = audio_file.analysis.beats
	beats.reverse()
	audio.getpieces(audio_file, beats).encode(mp3path + "/backwards/_backwards" + songID)


if __name__ == '__main__':
	#songID = sys.argv[1]
	#debug
	songID = 'TRAAAAW128F429D538.mp3'
	playMP3(songID)

