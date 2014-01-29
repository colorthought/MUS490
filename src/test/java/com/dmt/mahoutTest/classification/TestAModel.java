package com.dmt.mahoutTest.classification;

import java.io.*;

import com.dmt.mahout.classification.sgd.SGDTrainer;
import com.dmt.mahout.classification.text.*;

import com.dmt.mahout.classification.NaiveBayes.NBayesFactoryParams;
import com.dmt.mahout.classification.NaiveBayes.NaiveBayesFactory;

import junit.framework.TestCase;

public class TestAModel extends TestCase {

	static String trainingOUT = "data/training-seq";
	static String imdbTESTOUT = "data/imdb-seq";
	static int ngramsize = 3;
	
	
	public TestAModel(String dataset, String model, int ngramsize) throws IOException
	{
		TestAModel.ngramsize = ngramsize; 
		if(dataset == "data/imdb-seq")
		{
			model = "nbayes";
			testNBayes(imdbTESTOUT, false);
		}
		else if(dataset == "data/tweets-train.tsv")
		{
			ToSeq(dataset, true);
			modelPicker(dataset, model);
		}
		else
		{
			ToSeq(dataset, false);
			modelPicker(dataset, model);
		}
		
	}
	
	public static void modelPicker(String dataset, String model) throws IOException
	{
		if(model == "nbayes")
		{
			testNBayes(trainingOUT, false);
		}
		else if(model == "cnbayes")
		{
			testNBayes(trainingOUT, true);
		}
		else
		{
			testSGDTrainer(dataset);
		}

	}
	
	public static void testNBayes(String training, boolean isComplementary) throws IOException
	{
				
		NBayesFactoryParams factoryparams1 = new NBayesFactoryParams(training, "sampleclass");
		factoryparams1.setParams("for-testing", training, "sampleclass", 20, isComplementary, true, ngramsize, "tfidf");
		NaiveBayesFactory factory = new NaiveBayesFactory(factoryparams1);
		try {
			factory.startFactory();
		} catch (Exception e) {
			System.out.println("Failed to start factory");
			e.printStackTrace();
		}
	}
	
	
	public static void ToSeq(String trainingIN, boolean hasID)
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
	
	
	public static void testSGDTrainer(String dataset) throws IOException
	{
		SGDTrainer sgdtrainer = new SGDTrainer(dataset, true);
		sgdtrainer.TrainSGD(ngramsize);
	}
	
}

