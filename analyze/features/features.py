"""
The MIT License

Copyright (c) 2014 Jacob Reske
For use in MUS491 Senior Project, in partial fulfillment of the Yale College Music Major (INT).
Code may be reused and distributed without permission.
"""

FEATURE = ['mfcc: MFCC blockSize=512 stepSize=256',
'mfcc_d1: MFCC blockSize=512 stepSize=256 > Derivate DOrder=1',
'mfcc_d2: MFCC blockSize=512 stepSize=256 > Derivate DOrder=2'
]

FEATURE2 = ['mfcc: MFCC blockSize=512 stepSize=256',
'obsi: OBSI blockSize=512 stepsize=256', 
'am: AmplitudeModulation blockSize=32768 stepSize=16384']

FEATURE3 = ['mfcc: MFCC blockSize=512 stepSize=256',
'mfcc_d1: MFCC blockSize=512 stepSize=256 > Derivate DOrder=1',
'mfcc_d2: MFCC blockSize=512 stepSize=256 > Derivate DOrder=2',
'obsi: OBSI blockSize=512 stepsize=256',
'am: AmplitudeModulation blockSize=32768 stepSize=16384']

STRESSTEST = ['mfcc: MFCC blockSize=512 stepSize=256',
'mfcc_d1: MFCC blockSize=512 stepSize=256 > Derivate DOrder=1',
'mfcc_d2: MFCC blockSize=512 stepSize=256 > Derivate DOrder=2',
'obsi: OBSI blockSize=512 stepSize=256',
'am: AmplitudeModulation blockSize=32768 stepSize=16384',
'autocorr: AutoCorrelation blockSize=512 stepSize=256',
'onsdet: ComplexDomainOnsetDetection blockSize=512 stepSize=256',
'lpc: LPC blockSize=512 stepSize=256',
'secvar: SpectralVariation blockSize=512 stepSize=256']


def getExtension(featureList, index):
	feature = featureList[index]
	x = feature.split(':')
	extension = x[0]
	#print(extension)					#[DEBUG]
	return extension

if __name__ == '__main__':
	getExtension(FEATURE, 1)


'''
'sf: SpectralFlatness blockSize=1024 stepSize=256',
'sf: SpectralRolloff blockSize=1024 stepSize=256
'''