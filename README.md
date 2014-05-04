# MUS490
Jacob Reske, YC '14 
(In partial fulfillment of the requirements for the degree of Bachelor of Arts, Music [INT])

##Description:

MUS490 is a toolkit for realtime musical feature extraction and clustering.
It combines integration with the Yaafe audio feature extraction toolbox with a set of variants on a weighted K-means clustering algorithm. Options are available for adding different distance metrics, auto-K, auto-weighting, and drilldowns on clusters after the clustering is run.

MUS490 is designed to be general and extensible, able to find similarities amidst virtually any musical styles you give it. We implement auto-weighing and auto-k on the principle that musical styles/genres often prioritize a small subset of musical features distinct to that genre. 

Planned features in the next iteration include model saving/loading and a second, more advanced auto-weight heuristic.

Sources for each algorithm are available in the /thesis folder.

#Demo:
MUS490 includes a demo script to run and test any .mp3 dataset you like. In the tests folder, run ./testAll.sh to select options. Before doing so, place the .mp3 datasets you would like to use in a folder called "mp3," located in MUS490's parent folder. A folder in that location, marked "output," will also be created.


##Dependencies:
MUS490 requires a few dependencies to run correctly.

**NumPy:**
http://www.numpy.org

**Yaafe:**
http://yaafe.sourceforge.net

##Papers:

**Unsupervised, Auto K-Means Audio Clustering using Dynamic Weight Selection**

Abstract: *Fully unsupervised, automatic clustering by musical features (e.g. timbre, pitch, and rhythm) presents a number of problems. Selecting essential criteria for musical feature extraction, preprocessing the data, and finding similarities in the results introduces typical machine learning problems of overfitting and high dimensionality. The benefits of creating a fully unsupervised clustering algorithm, however, are clear. Fully unsupervised clustering could find unlikely matches in disparate musical styles, as well as a method to process large (or very new) datasets from streaming sources. Music researchers could use this tool to observe similarities in new, uncategorized, or recently digitized music (i.e. without ID3 tags). In this paper, we propose a toolkit that combines a robust musical feature selector and an auto-k, auto-weighted k-means clustering algorithm.*

**Information Theory and a Musical AI**

Abstract: *In this paper, we apply the basic principles of Information theory to the field of artificial music cognition— its problems, some solutions, and the role of computers as the final stage of a fully informed information system. Some of the earliest writings on Information Theory and aesthetics— specifically, Claude E. Shannon’s A Mathematical Theory for Communication, as well as Abraham Moles’ Information Theory and Aesthetic Perception— are just as relevant for computer cognition today as they were when they were published. As the focus of music cognition shifts from the role of the transmitter to that of the receptor (the computer), both Shannon and Moles’ original texts can provide valuable insight for solving the biggest issues of creating a generalized music AI today. Three basic problems of making a musical AI will be explored— the need for a representation system that can handle the system’s entropy, the necessity of reassembling a transmission contextually, and the role of an aesthetic arbiter outside the system— problems which correlate strongly with those of communication systems decades before. The goal of viewing these problems in this way is to use Information Theory principles to unite various disciplines in music AI under a larger task: creating a machine that can receive sound just as an individual would and, ultimately, extend further the basic human process of distinguishing signal from noise.*