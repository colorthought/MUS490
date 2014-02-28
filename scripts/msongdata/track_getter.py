"""
    Loads track from the flat-file database of the Million Song Dataset (MSD).
"""

import sys
import track
import get_preview_url


def getURL(filepath):
    """ The mapper loads a track and yields its density """
    f = open(filepath)
    for which, line in enumerate(f):
        t = track.load_track(line)
        #debug
        print t['tempo']
        Seventrack = get_preview_url.get_trackid_from_text_search(t['title'], t['artist_name'])
        p = get_preview_url.get_preview_from_trackid(Seventrack[1])
        print p

if __name__ == '__main__':
    filepath = sys.argv[1]
    getURL(filepath)