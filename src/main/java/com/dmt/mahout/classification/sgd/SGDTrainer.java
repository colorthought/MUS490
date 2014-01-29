package com.dmt.mahout.classification.sgd;


import java.io.IOException;

import org.apache.mahout.classifier.sgd.L1;
import org.apache.mahout.classifier.sgd.OnlineLogisticRegression;
import org.apache.mahout.math.DenseVector;
import org.apache.mahout.math.Vector;

import com.google.common.collect.HashMultiset;
import com.google.common.collect.Multiset;

import com.dmt.mahout.classification.text.CSVEncoderLine;
import com.dmt.mahout.classification.text.SentimentDictionary;

/**
 * Adapted from:
 * 
 * https://github.com/tdunning/MiA/blob/master/src/main/java/mia/classifier/ch14
 * /TrainNewsGroups.java
 * 
 * @author: JER
 * 
 */
public class SGDTrainer {

	String filename;
	boolean isTSV;
	
	static int numCategories;
	static int FEATURES = 10000;
	static int alphaval = 1;
	static int stepOffsetval = 1000;
	static double decayExponentval = 0.9;
	static double lambdaval = 3.0e-5;
	static int learningRateval = 20;
	
	@SuppressWarnings("unused")
	private static Multiset<String> overallCounts;
	private static String[] currentSentiments = { "positive", "negative", "mutual" };
	private static SentimentDictionary sentimentdict = new SentimentDictionary(currentSentiments);
	OnlineLogisticRegression learningAlgorithm = new OnlineLogisticRegression(
			20, FEATURES, new L1()).alpha(1).stepOffset(1000)
			.decayExponent(0.9).lambda(3.0e-5).learningRate(20);

	static long t0;
	static double step;
	static int k;
	static double averageLL;
	static int[] bumps;
	static double averageCorrect;
	static double averageLineCount;
	static double lineCount;

	public SGDTrainer(String filename, boolean isTSV)
	{
		this.filename = filename;
		this.isTSV = isTSV;
	}
	
	
	public void setSentiments(String[] currentSentiments)
	{
		this.currentSentiments = currentSentiments;
		SentimentDictionary sentimentdict = new SentimentDictionary(currentSentiments);
		
	}
	
	/**
	 * Runs model on example Training set
	 * 
	 * 
	 * @param baseTrainingDataDir
	 * @throws IOException
	 */
	public void TrainSGD(int GramNum) throws IOException
	{
		overallCounts = HashMultiset.create();
	    int leakType = 0;
	    
		CSVEncoderLine csvencoder = new CSVEncoderLine(filename, GramNum);
		initStats();
		String line = csvencoder.readCSVFirstLine();
		while (line != null)
		{
			csvencoder.MakeLine(line);
			int actual = sentimentdict.intern(csvencoder.getCurrentSentiment(line));
			Vector v = csvencoder.encodeFeatureVector(line);
			
			learningAlgorithm.train(actual, v);
			
			k++;
			
			
			double mu = Math.min(k + 1, 200);
			double ll = learningAlgorithm.logLikelihood(actual, v);
			averageLL = averageLL + (ll - averageLL) / mu;

			Vector p = new DenseVector(20);
			learningAlgorithm.classifyFull(p, v);
			int estimated = p.maxValueIndex();
			int correct = (estimated == actual ? 1 : 0);
			averageCorrect = averageCorrect + (correct - averageCorrect) / mu;


			int bump = bumps[(int) Math.floor(step) % bumps.length];
			int scale = (int) Math.pow(10, Math.floor(step / bumps.length));

			if (k % (bump * scale) == 0)
			{
				step += 0.25;
				System.out.printf("%10d %10.3f %10.3f %10.2f %s %s %s\n", k, ll,
						averageLL, averageCorrect * 100, csvencoder.getCurrentSentiment(line), sentimentdict
								.values().get(estimated), csvencoder.getCurrentText(line));
			}

			learningAlgorithm.close();
			
			line = csvencoder.readCSVNewLines();
		}
		
		System.out.printf("\nElapsed time = %.3f s\n",
				(System.currentTimeMillis() - t0) / 1000.0);

	}	

	public void initStats()
	{
		t0 = System.currentTimeMillis();
		step = 0.0;
		k = 0;
		averageLL = 0.0;
		bumps = new int[] { 1, 2, 5 };
		averageCorrect = 0.0;
		averageLineCount = 0.0;
		lineCount = 0;
	}
	      
	
	public void setRegressionAlgorithm()
	{
		@SuppressWarnings("resource")
		OnlineLogisticRegression learningAlgorithm = new OnlineLogisticRegression(
				20, FEATURES, new L1()).alpha(1).stepOffset(1000)
				.decayExponent(0.9).lambda(3.0e-5).learningRate(20);

	}	

}
