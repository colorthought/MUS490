"""
    Loads track from the flat-file database of the Million Song Dataset (MSD).
"""

import sys
import os
import track
import get_preview_url
import urllib2

syspath = os.path.dirname(os.path.realpath(__file__))

def makefolder(name):
    path = (syspath + '/' + name)
    if not os.path.exists(path):
        os.makedirs(path)
    print path
    return path


def downloadtrack(track, line, downloadpath):
    t = track.load_track(line)
    print t['preview']
    try:
        mp3 = urllib2.urlopen(t['preview'])
        with open(downloadpath + '/' + t['track_id'] + ".mp3", "wb") as code:
            code.write(mp3.read())
    except urllib2.HTTPError:
        print "this works."


def downloadAllTracks(filepath):
    """
        URL getter of a given track for use in the """
    f = open(filepath)

    mp3path = makefolder('mp3')
    for which, line in enumerate(f):   
        downloadtrack(track, line, mp3path)

        #Seventrack = get_preview_url.get_trackid_from_text_search(t['title'], t['artist_name'])
        #p = get_preview_url.get_preview_from_trackid(Seventrack[1])
        #print p


def trainTestSplitter(filepath):
    """
        Loads .dat file and splits into training and test set for processing.
    """
    datapath = makefolder('data')

    f = open(filepath)
    train = open(os.path.join(datapath, 'train.dat'), 'wb')
    test = open(os.path.join(datapath, 'test.dat'), 'wb')
    
    #80/20 split
    length = filelength(filepath)
    tr_length = int(filelength(filepath) * .8)
    te_length = int(length - tr_length)

    #write split to training/test files
    for i in range(0, tr_length):
        train.write(f.readline() + '\n')
    for i in range(0, te_length):
        test.write(f.readline() + '\n')
    print('wrote ' + str(tr_length) + ' entries to training set' +
         ' and ' + str(te_length) + ' entries to test set.')


def filelength(file):
    with open(file) as f:
        for i, l in enumerate(f):
            pass
        return i + 1

if __name__ == '__main__':
    filepath = sys.argv[1]
    downloadAllTracks(filepath)
    trainTestSplitter(filepath)