package com.dmt.mahoutTest;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Scanner;

import com.dmt.mahoutTest.classification.TestAModel;
import com.dmt.mahoutTest.classification.TestAllModels;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

/**
 * Unit test for simple App.
 */
public class AppTest extends TestCase {
	
	static final String WELCOME_TEXT = "Welcome, ADVENTURER, to the magical land of MAHOUT. \n" +
			"Please select one of these groovy options.";
	static final String WELCOME2_TEXT = "Select your dataet -- if you DARE.";
	static final String WELCOME3_TEXT = "Good choice. Waaaay better than those other, inferior datasets. \n" +
			"Select your model -- if you DARE.";
	static final String WELCOME4_TEXT = "Nice one. \n" +
			"Generating model...........";
	static final String INVALID_TEXT = "That is not a valid option, adventurer. \n" + 
			"Pick a valid option -- if you DARE.";
	
	static final String FIRSTOPTION_TEXT = "[1]. Run Test 1 (IMDB, Naive Bayes, 3 classes. \n" +
			"[2]. Run Test 2 (Twitter, Naive Bayes, 10 classes. \n" +
			"[3]. Run Test 3 (IMDB, Naive Bayes, 2 classes. \n" +
			"[4]. Run Test 4 (IMB, Stochastic Gradient Descent (SGD). \n" + 
			"[5]. Run Test 5 (The Hobbit, Stochastic Gradient Descent (SGD). \n" +
			"[6]. Run a custom test. \n" +
			"[7]. Run all tests.";
	
	static final String DATASET_TEXT = "[1]. Twitter - Deal Classification dataset \n" +
			"[2]. IMDB - 10,000 movie reviews dataset (sorted by star rating) \n" +
			"[3]. IMDB - 30,000 movie reviews dataset (sorted by sentiment) \n" +
			"[4]. The Hobbit - 1,000 movie reviews (sorted by sentiment";
	
	static String MODELTYPE_TEXT = "[1]. Naive Bayes \n" +
			"[2]. Complementary Naive Bayes \n" +
			"[3]. Stochastic Gradient Descent (SGD)";
	
	static String dataset;
	static String model;	
	
	public static void main(String[] args) throws IOException
	{
		BufferedReader in = new BufferedReader(new FileReader("data/intro.txt"));
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		
		String introline;
		while((introline = in.readLine()) != null)
		{
		    System.out.println(introline);
		}
		System.out.println();
		
		System.out.println(WELCOME_TEXT);
		System.out.println(FIRSTOPTION_TEXT);
		
		int mainoption;
		boolean isInvalid = false;
		
		do
		{
		mainoption = br.read();
		switch(mainoption)
		{
			case '1': {TestAModel testamodel = new TestAModel("data/imdb-seq", "nbayes", 2); 
				isInvalid = false; break;}
			case '2': {TestAModel testamodel = new TestAModel("data/tweets-train.tsv", "cnbayes", 1);
				isInvalid = false; break;}
			case '3': {TestAModel testamodel = new TestAModel("data/imdbtrainingData.tsv", "nbayes", 2);
				isInvalid = false; break;}
			case '4': {TestAModel testamodel = new TestAModel("data/imdbtrainingData.tsv", "sgd", 3);
				isInvalid = false; break;}
			case '5': {TestAModel testamodel = new TestAModel("data/thehobbit-train.tsv", "sgd", 3);
				isInvalid = false; break;}
			case '6': {TestCustom();
				isInvalid = false; break;}
			case '7': {TestEveryModel();
				isInvalid = false; break;}
			default: { isInvalid = true;
				System.out.println(INVALID_TEXT);
			}
		}
		} while (isInvalid == true);
	}
	
	
	public static void TestEveryModel() throws IOException
	{
		TestAllModels testmodels = new TestAllModels();
		testmodels.testTweetNBayes();
		testmodels.testSGDTrainer();

	}
	
	
	public static void TestCustom() throws IOException
	{
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		
		System.out.print(WELCOME2_TEXT + "\n");
		System.out.println(DATASET_TEXT + "\n");
		
		int datasetoption;
		boolean dataInvalid = false;
		
		do
		{
		datasetoption = br.read();
		switch(datasetoption)
		{
			case '1': {dataset = "data/tweets-train.tsv"; break;}
			case '2': {dataset = "data/imdb-seq"; 
				dataInvalid = false; break;}
			case '3': {dataset = "data/imdbtrainingData.tsv"; 
				dataInvalid = false; break;}
			case '4': {dataset = "data/thehobbit-train.tsv";
				dataInvalid = false; break;}
			default: { dataInvalid = true;
				System.out.println(INVALID_TEXT);
			}
		}
		} while (dataInvalid == true);
		
		System.out.println(WELCOME3_TEXT + "\n");
		System.out.println(MODELTYPE_TEXT + "\n");
		
		int modeloption;
		boolean modelInvalid = false;
		
		do
		{
		modeloption = br.read();
		switch(modeloption)
		{
			case '1': {model = "nbayes"; 
				modelInvalid = false; break;}
			case '2': {model = "cnbayes"; 
				modelInvalid = false; break;}
			case '3': {model = "sgd";
				modelInvalid = false; break;}
			default: { modelInvalid = true;
				System.out.println(INVALID_TEXT);
			}
		}
		} while (modelInvalid == true);
		
		Scanner intIn = new Scanner(System.in);
		System.out.println("NGramsize?");
		int ngramsize = intIn.nextInt();
		
		System.out.println(WELCOME4_TEXT);
		System.out.println("Dataset: " + dataset);
		System.out.println("Model: " + model);
		System.out.println("Ngram size: " + ngramsize);
		TestAModel testamodel = new TestAModel(dataset, model, ngramsize);
		
	}
}
