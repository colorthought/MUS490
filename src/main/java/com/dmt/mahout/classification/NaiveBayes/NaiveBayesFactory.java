package com.dmt.mahout.classification.NaiveBayes;


import org.apache.mahout.classifier.naivebayes.test.TestNaiveBayesDriver;
import org.apache.mahout.classifier.naivebayes.training.TrainNaiveBayesJob;
import org.apache.mahout.utils.SplitInput;
import org.apache.mahout.vectorizer.SparseVectorsFromSequenceFiles;


public class NaiveBayesFactory {

	static String workingDIR;
	NBayesFactoryParams factoryparams;
	
	
	public NaiveBayesFactory(NBayesFactoryParams factoryparams)
	{
		this.factoryparams = factoryparams;
	}
		
	
	@SuppressWarnings("static-access")
	public void startFactory() throws Exception
	{
		
		SparseVectorsFromSequenceFiles sparsevectors = new SparseVectorsFromSequenceFiles();
		sparsevectors.main(factoryparams.sparseVectorArgs());

		SplitInput inputsplitter = new SplitInput();
		inputsplitter.main(factoryparams.splitArgs());
		
		//[DEBUG] -----------------------------------------------------------------------------------
		System.out.println("We got this far...");
		
		TrainNaiveBayesJob trainnbayes = new TrainNaiveBayesJob();
		trainnbayes.main(factoryparams.trainArgs());
		
		TestNaiveBayesDriver testnbayes = new TestNaiveBayesDriver();
		testnbayes.main(factoryparams.testontrainingArgs());
		
		TestNaiveBayesDriver testtestnbayes = new TestNaiveBayesDriver();
		testtestnbayes.main(factoryparams.testontestArgs());
	}
}
