import os
import beat_tracker
import librosa

syspath = os.path.abspath(os.curdir)
os.chdir("..")
mp3path = os.path.abspath(os.curdir) + '/mp3'

def tempoEstimate(songID):
	audio_path = mp3path + '/' + songID

	beat_tracker.beat_track(audio_path, 'output.csv')

if __name__ == '__main__':
	songID = 'TRAAAAW128F429D538.mp3'
	tempoEstimate(songID)

