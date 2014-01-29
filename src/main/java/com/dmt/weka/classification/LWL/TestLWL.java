package com.dmt.weka.classification.LWL;


import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Random;

import weka.classifiers.Classifier;
import weka.classifiers.lazy.LWL;
import weka.classifiers.rules.ZeroR;
import weka.core.Instance;
import weka.core.Instances;

public class TestLWL {

	
	static File file = new File("data/numeric/housing.arff");
	static int numKNN = 50;
	
	public static void main(String[] args) throws IOException
	{
		FileReader reader = new FileReader(file);
		Instances instances = new Instances(reader);
		int ATTRIBUTE_INDEX = (instances.numAttributes() - 2);
		instances.setClassIndex(ATTRIBUTE_INDEX);
		
		//Splits .arff instances into training and test instances
		int trainSize = (int) Math.round(instances.numInstances() * 0.8);
		int testSize = instances.numInstances() - trainSize;
		Instances train = new Instances(instances, 0, trainSize);
		Instances test = new Instances(instances, trainSize, testSize);
			
		//Selects random instance from the test set, just as an example
		Random randomtestindex = new Random();
		int randomIndex = randomtestindex.nextInt(test.numInstances());
		Instance testRandom = new Instance(test.instance(randomIndex));
		testRandom.setDataset(instances);
				
		//[DEBUG] -----------------------------------------------------
		//System.out.println(instances.toSummaryString());
		
		//Creates new LWL classifier
		Classifier m_Classifier = new ZeroR();
		LWL localWeightedLinear = new LWL();
		localWeightedLinear.setDebug(false);
		localWeightedLinear.setKNN(numKNN);
		localWeightedLinear.setClassifier(m_Classifier);
		localWeightedLinear.setDebug(true);
		
		
		try {
			localWeightedLinear.buildClassifier(train);
		} catch (Exception e) {
			System.out.println("Error: Can't build classifier.");
			e.printStackTrace();
		}
		
		double[] trainingActuals = new double[test.numInstances()];
		double[] trainingResults = new double[test.numInstances()];
		
		//Classifies 20% of unclassed instances, keeps around the actual unclass.
		try {
			
			
			for (int instance = 0; instance < test.numInstances(); instance++)
			{
				double actual = test.instance(instance).value(ATTRIBUTE_INDEX);
				double result = localWeightedLinear.classifyInstance(test.instance(instance));
				
				trainingActuals[instance] = actual;
				trainingResults[instance] = result;
			}	
		} catch (Exception e) {
			System.out.println("Error: Can't classify that instance.");
			e.printStackTrace();
		}
		
		double percentTotal = 0;
		int totals = 0;
		//Compares results
		for (int instance = 0; instance < trainingActuals.length; instance++)
		{
			double percentDiff = calcPercentDiff(trainingResults[instance], trainingActuals[instance]);
			percentTotal+= percentDiff;
			totals++;
		}
		
		double percent = ((percentTotal)/((double)totals)) * 100;
		System.out.printf("We're looking at a %1.2f percent error.", percent);
		System.out.println("This is while predicting value: " + instances.attribute(instances.classIndex()));
		System.out.println("\n Okay, now let's try a random class example from the test set. \n");
		
		try {
			double actual = testRandom.value(ATTRIBUTE_INDEX);
			double result = localWeightedLinear.classifyInstance(testRandom);
			double percentDiff = calcPercentDiff(actual, result) * 100;
			System.out.printf("For a random instance, value " + actual + " was estimated as %1.2f \n", result);
			System.out.printf("We're also looking at a %1.2f percent difference here.", percentDiff);

		} catch (Exception e) {
			System.out.println("Can't classify random instance, for some reason.");
			e.printStackTrace();
		}
		
						
	}
	
	static double calcPercentDiff(double result, double actual)
	{
		double absDiff = Math.abs((actual - result));
		double percentDiff = Math.abs(( absDiff / actual));
		return percentDiff;
	}
}
