"""
The MIT License

Copyright (c) 2014 Jacob Reske
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.

Description: wget and splitter from the flat-file database of the Million Song Dataset (MSD).
"""

import sys
import os
import track
import get_preview_url
import urllib2
syspath = os.path.dirname(os.path.realpath(__file__))

class TrackGetter:

    filepath = None

    def __init__(self, filepath):
        self.filepath = filepath


    def makefolder(self, name):
        path = (syspath + '/' + name)
        if not os.path.exists(path):
            os.makedirs(path)
        print path
        return path


    def downloadtrack(self, track, line, downloadpath):
        t = track.load_track(line)
        print(t['preview'])
        #print t['preview']
        try:
            mp3 = urllib2.urlopen(t['preview'])
            mp3name =  downloadpath + '/' + t['track_id'] + ".mp3"
            with open(mp3name, "wb") as code:
                code.write(mp3.read())
                print(mp3name)              #[DEBUG]
        except urllib2.HTTPError:
            mp3 = get_preview_url.get_preview_from_trackid(t['track_id'])
            print(mp3)
            print "dammit."                 #[DEBUG]


    def downloadAllTracks(self):
        """
            URL getter of a given track for use in the """
        f = open(self.filepath)

        for which, line in enumerate(f):   
            self.downloadtrack(track, line, mp3path)

            #Seventrack = get_preview_url.get_trackid_from_text_search(t['title'], t['artist_name'])
            #p = get_preview_url.get_preview_from_trackid(Seventrack[1])
            #print p


    def splitTrainTest(self):
        """
            Loads .dat file and splits into training and test set for processing.
        """
        datapath = self.makefolder('data')

        f = open(self.filepath)
        train = open(os.path.join(datapath, 'train.dat'), 'wb')
        test = open(os.path.join(datapath, 'test.dat'), 'wb')
        
        #80/20 split
        length = self.filelength(self.filepath)
        tr_length = int(self.filelength(self.filepath) * .8)
        te_length = int(length - tr_length)

        #write split to training/test files
        for i in range(0, tr_length):
            train.write(f.readline() + '\n')
        for i in range(0, te_length):
            test.write(f.readline() + '\n')
        print('wrote ' + str(tr_length) + ' entries to training set' +
             ' and ' + str(te_length) + ' entries to test set.')


    def filelength(self, file):
        with open(file) as f:
            for i, l in enumerate(f):
                pass
            return i + 1


if __name__ == '__main__':
    filepath = sys.argv[1]
    TrackGetter = TrackGetter(filepath)
    TrackGetter.downloadAllTracks()
    TrackGetter.splitTrainTest()
