# MUS490 Project
Jacob Reske, YC '14 
In partial fulfillment of the Music (INT) Major requirement

##Description:

MUS490 is a toolkit for realtime musical feature extraction and clustering.
It combines integration with the Yaafe audio feature extraction toolbox with a set of variants on a weighted K-means clustering algorithm. Options are available for adding different distance metrics, auto-K, auto-weighting, and drilldowns on clusters after the clustering is run.

MUS490 is designed to be general and extensible, able to find similarities amidst virtually any musical styles you give it. We implement auto-weighing and auto-k on the principle that musical styles/genres often prioritize a small subset of musical features distinct to that genre. 

Planned features in the next iteration include model saving/loading and a second, more advanced auto-weight heuristic.

Sources are 

#Demo:
MUS490 includes a demo script to run and test any .mp3 dataset you like. In the tests folder, run ./testAll.sh to select options. Before doing so, place the .mp3 datasets you would like to use in a folder called "mp3," located in MUS490's parent folder. A folder in that location, marked "output," will also be created.


##Dependencies:

MUS490 requires a few dependencies to run correctly.
**NumPy** http://www.numpy.org
**Yaafe** http://yaafe.sourceforge.net