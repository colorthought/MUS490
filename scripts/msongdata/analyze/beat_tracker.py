#!/usr/bin/env python
'''
CREATED:2013-02-11 18:37:30 by Brian McFee <brm2132@columbia.edu>

Track beat events in an audio file

Usage:   ./beat_tracker.py [-h] input_file.mp3    output_beats.csv
'''

import sys, librosa, argparse

# 1. load the wav file and resample to 22.050 KHz
def beat_track(input_file, output_csv):
    '''Beat tracking function
    
    :parameters:
      - input_file : str
          Path to input audio file (wav, mp3, m4a, flac, etc.)

      - output_file : str
          Path to save beat event timestamps as a CSV file
    '''

    print 'Loading ', input_file
    y, sr         = librosa.load(input_file, sr=22050)

    # Use a default hop size of 64 frames @ 22KHz ~= 11.6ms
    HOP_LENGTH  = 64

    # This is the window length used by default in stft
    N_FFT       = 2048

    print 'Tracking beats'
    tempo, beats    = librosa.beat.beat_track(y=y, sr=sr, hop_length=HOP_LENGTH)

    print 'Estimated tempo: %0.2f beats per minute' % tempo

    # 3. save output
    # 'beats' will contain the frame numbers of beat events.

    beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=HOP_LENGTH, n_fft=N_FFT)

    print 'Saving output to ', output_csv
    librosa.output.times_csv(output_csv, beat_times)
    print 'done!'


def process_arguments():
    '''Argparse function to get the program parameters'''

    parser = argparse.ArgumentParser(description='librosa beat-tracking example')

    parser.add_argument(    'input_file',
                            action      =   'store',
                            help        =   'path to the input file (wav, mp3, etc)')

    parser.add_argument(    'output_file',
                            action      =   'store',
                            help        =   'path to the output file (csv of beat times)')

    return vars(parser.parse_args(sys.argv[1:]))


if __name__ == '__main__':
    # Get the parameters
    parameters = process_arguments()

    # Run the beat tracker
    beat_track(parameters['input_file'], parameters['output_file'])