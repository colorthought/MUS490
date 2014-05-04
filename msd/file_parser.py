"""
    Loads track from the flat-file database of the Million Song Dataset (MSD).
"""

import sys
import track


def listMSDValues(filepath, value):
    """
        URL getter of a given track for use in the
    """
    f = open(filepath)

    valuestr = str(value)
    for which, line in enumerate(f):
        t = track.load_track(line)
        print t['title']
        print t[valuestr]


def filelength(file):
    with open(file) as f:
        for i, l in enumerate(f):
            pass
        return i + 1

if __name__ == '__main__':
    filepath = sys.argv[1]
    value = str(sys.argv[2])
    listMSDValues(filepath, value)


'''
values that the parser needs:
    1) filepath to dataset
    2) MSD value
'''
