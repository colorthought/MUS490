package com.dmt.mahout.classification.RandomForest;


import org.apache.mahout.classifier.df.mapreduce.BuildForest;
import org.apache.mahout.classifier.naivebayes.test.TestNaiveBayesDriver;
import org.apache.mahout.classifier.naivebayes.training.TrainNaiveBayesJob;
import org.apache.mahout.utils.SplitInput;
import org.apache.mahout.vectorizer.SparseVectorsFromSequenceFiles;


public class RandomForestFactory {

	static String workingDIR;
	RandomForestFactoryParams factoryparams;
	
	
	public RandomForestFactory(RandomForestFactoryParams factoryparams)
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
		
		BuildForest buildforest = new BuildForest();
		String[] arguments = { };
		buildforest.main(arguments);
		
		
		
		
	}
}
