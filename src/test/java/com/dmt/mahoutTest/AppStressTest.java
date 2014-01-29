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
public class AppStressTest extends TestCase {
	
	
	private static final int N = 10;


	public static void main(String[] args) throws IOException
	{
		
		TestEveryModel();
	}
	
	
	public static void TestEveryModel() throws IOException
	{
		TestAllModels testmodels = new TestAllModels();
		
		for(int i = 0 ; i < N; i++)
		{
			testmodels.testTweetNBayes();
			testmodels.testSGDTrainer();
		}

	}
}
