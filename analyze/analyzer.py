"""
    A map-reduce that calculates the density for each
    of a set of tracks.  The track density is the average
    number of segments per segment for a track.
"""

from yaafelib import *

import sys, os, inspect
from features import mfcc_1


class analyzer:

    SAMPLERATE = 22050
    mp3 = None
    featureList = mfcc_1.FEATURE
    dataflow_file = None
    toCSV = False

    
    #init for loading from a featureList array
    def __init__(self, mp3, featureList, toCSV):
        self.mp3 = mp3
        self.featureList = featureList
        self.toCSV = toCSV

    
    #init for loading from an existing datafile
    def __init__(self, mp3, dataflow_file, toCSV):
        self.mp3 = mp3
        self.dataflow_file = dataflow_file
        self.toCSV = toCSV 

    
    #parses dataflow from featureList array given at __init__
    def dataFlowCreator(self): 
        fp = FeaturePlan(sample_rate=self.SAMPLERATE)
        for i in range(len(self.featureList)):
            fp.addFeature(self.featureList[i])

        df = fp.getDataFlow()
        return df

    
    #loads an existing dataflow from file
    def dataFlowLoader(self):
        if self.dataflow_file != None:
            df = DataFlow()
            df.load(self.dataflow_file)
            return df

    
    #processes audio given specified dataflow
    def Processor(self, dataflow):
        engine = Engine()
        engine.load(dataflow)
        afp = AudioFileProcessor()
        
        afp.processFile(engine, mp3)
        feats = engine.readAllOutputs()
        if self.toCSV:
            afp.setOutputFormat('csv', '../output', {'Precision': '8'})
            afp.processFile(engine,mp3)
        #[DEBUG]
        #print(feats)


if __name__ == '__main__':
    mp3 = sys.argv[1]
    featureList = mfcc_1.FEATURE
    print(featureList)          #[DEBUG]
    analyzer = analyzer(mp3, featureList, True)
    df = analyzer.dataFlowCreator()
    analyzer.Processor(df)

