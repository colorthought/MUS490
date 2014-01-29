package com.dmt.mahoutTest.classification;

import java.io.*;

import com.dmt.mahout.classification.sgd.SGDTrainer;
import com.dmt.mahout.classification.text.*;

import com.dmt.mahout.classification.NaiveBayes.NBayesFactoryParams;
import com.dmt.mahout.classification.NaiveBayes.NaiveBayesFactory;

import junit.framework.TestCase;

public class TestAllModels extends TestCase {

	static String hobbitfilename = "data/thehobbit-train.tsv";
	static String newimdbfilename = "data/imdbtrainingData.tsv";
	static String tweetfilename = "data/tweets-train.tsv";
	static String imdbfilename = "data/imdbtrainingData.tsv";
	static String trainingOUT = "data/training-seq";
	static String imdbTESTOUT = "data/imdb-seq";
	
	
	public void testTweetNBayes() throws IOException
	{
		
		
		ToSeq(hobbitfilename, false);
		
		NBayesFactoryParams factoryparams1 = new NBayesFactoryParams(trainingOUT, "thehobbit3class");
		factoryparams1.setParams("for-testing", trainingOUT, "thehobbit3class", 40, false, true, 3, "tfidf");
		NaiveBayesFactory factory = new NaiveBayesFactory(factoryparams1);
		try {
			factory.startFactory();
		} catch (Exception e) {
			System.out.println("Failed to start factory");
			e.printStackTrace();
		}
	
		ToSeq(tweetfilename, true);		
		
		NBayesFactoryParams factoryparams2 = new NBayesFactoryParams(trainingOUT, "tweetclass");
		factoryparams2.setParams("for-testing", trainingOUT, "tweetclass", 40, false, true, 1, "tfidf");		
		NaiveBayesFactory factory2 = new NaiveBayesFactory(factoryparams2);
		try {
			factory2.startFactory();
		} catch (Exception e) {
			System.out.println("Failed to start factory");
			e.printStackTrace();
		}
		
		NBayesFactoryParams factoryparams3 = new NBayesFactoryParams(imdbTESTOUT, "imdb2class");
		factoryparams3.setParams("for-testing", imdbTESTOUT, "imdb2class", 40, false, true, 3, "tfidf");
		NaiveBayesFactory factory3 = new NaiveBayesFactory(factoryparams3);
		try {
			factory3.startFactory();
		} catch (Exception e) {
			System.out.println("Failed to start factory");
			e.printStackTrace();
		}
		
	}
	
	
	public void ToSeq(String trainingIN, boolean hasID)
	{
		
		String[] seqArguments = {trainingIN, trainingOUT};		

		if(hasID)
		{
			TSVToSeq tsv2seq = new TSVToSeq(seqArguments);
			try {
				tsv2seq.CreateSequence();
			} catch (Exception e) {
				System.out.println("Error: Can't create sequence file");
				e.printStackTrace();
			}
		}
		else
		{
			TSVUnhashedToSeq tsvnohash2seq = new TSVUnhashedToSeq(seqArguments);
			try {
				tsvnohash2seq.CreateSequence();
			} catch (Exception e) {
				System.out.println("Error: Can't create sequence file");
				e.printStackTrace();
			}
		}
		
	}
	
	
	public void testSGDTrainer() throws IOException
	{
		SGDTrainer sgdtrainer = new SGDTrainer(hobbitfilename, true);
		sgdtrainer.TrainSGD(3);
	}
}

