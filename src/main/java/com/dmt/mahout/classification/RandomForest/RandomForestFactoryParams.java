/**
 * @author Jacob E. Reske
 * @description Class for instantiating preferences specific to the custom factory, NBayesFactory. 
 */

package com.dmt.mahout.classification.RandomForest;

import java.util.ArrayList;
import java.util.Arrays;

public class RandomForestFactoryParams {
	
	static String workingDIR;
	static String trainingseqfile;
	static String shortLabel;
	static String workingFULL;
	static String modelDIR;

	static int randomselectionPct;
	static boolean trainComplementary;
	static boolean logNormalize;
	static int nGramsize;
	static String weight;
	
	/**
	 * 
	 * @param trainingseqfile Sequence file, put in HDFS, used for vectorization.
	 * @param shortLabel Short name describing Naive Bayes case.
	 */
	public RandomForestFactoryParams(String trainingseqfile, String shortLabel)
	{
		workingDIR = "for-testing";
		RandomForestFactoryParams.trainingseqfile = trainingseqfile;
		RandomForestFactoryParams.shortLabel = shortLabel;
		RandomForestFactoryParams.workingFULL = workingDIR + "/" + shortLabel;
		modelDIR = workingDIR + "/model" + "-" + shortLabel;
		
		randomselectionPct = 40;
		trainComplementary = false;
		logNormalize = false;
		nGramsize = 1;
		weight = "tfidf";
	}
	
	/**
	 * 
	 * @param workingDIR The working directory for the NBayes classifier.
	 * @param trainingseqfile Sequence file, put in HDFS, used for vectorization.
	 * @param shortLabel Short name describing Naive Bayes case.
	 * @param randomSelectionpct Percentage of full set that is split off as a test set.
	 * @param trainComplementary Option for Complementary Naive Bayes. Defaults to false.
	 * @param logNormalize Set to false by default. Option for normalizing tokens on a log scale.
	 * @param nGramsize Size of NGrams. Defaults to 1.
	 * @param weight Option for tfidf or tf weights. Defaults to tfidf.
	 */
	public void setParams(String workingDIR, String trainingseqfile, String shortLabel, int randomSelectionpct, 
			boolean trainComplementary, boolean logNormalize, int nGramsize, String weight)
	{
		RandomForestFactoryParams.workingDIR = workingDIR;
		RandomForestFactoryParams.trainingseqfile = trainingseqfile;
		RandomForestFactoryParams.shortLabel = shortLabel;
		RandomForestFactoryParams.workingFULL = workingDIR + "/" + shortLabel;
		RandomForestFactoryParams.modelDIR = workingDIR + "/model" + "-" + shortLabel;

		RandomForestFactoryParams.randomselectionPct = randomSelectionpct;
		RandomForestFactoryParams.trainComplementary = trainComplementary;
		RandomForestFactoryParams.logNormalize = logNormalize;
		RandomForestFactoryParams.nGramsize = nGramsize;
		RandomForestFactoryParams.weight = weight;
	}
	
	
	public String[] sparseVectorArgs()
	{
		String[] sparsevectorargs = { "-i", trainingseqfile, 
				"-o", workingFULL + "/nbayes-vectors", 
				"-lnorm", "-ng", Integer.toString(nGramsize), "-wt", weight};
		
		String[] trainargsmod = addtoSeq2Sparse(new ArrayList<String>(Arrays.asList(sparsevectorargs)));
		return trainargsmod;
	}
			
	public String[] splitArgs()
	{
		String[] splitargs = { "-i", workingFULL + "/nbayes-vectors/tfidf-vectors", 
				"--trainingOutput", workingFULL + "/train-vectors", 
			"--testOutput", workingFULL + "/test-vectors", 
			"--randomSelectionPct", Integer.toString(randomselectionPct), 
			"--overwrite", 
			"--sequenceFiles", "-xm", "sequential" };
		return splitargs;
	}
		
	
	public String[] trainArgs()
	{
		String[] trainargs = { "-i", workingFULL + "/train-vectors", 
				"-el", "-li", workingFULL + "/labelindex", "-o", 
				modelDIR, "-ow" };
		String[] trainargsmod = addComplementary(new ArrayList<String>(Arrays.asList(trainargs)));
		
		return trainargsmod;
	}
	
	
	public String[] testontrainingArgs()
	{
		String[] testontrainingargs = { "-i", workingFULL + "/train-vectors", 
				"-m", modelDIR, "-l", workingFULL + "/labelindex", "-ow", 
				"-o", workingFULL + "/nbayes-testing" };
		
		String[] testontrainingargsmod = addComplementary(new ArrayList<String>(Arrays.asList(testontrainingargs)));

		return testontrainingargsmod;
	}
	
	
	public String[] testontestArgs()
	{
		String[] testontestargs = { "-i", workingFULL + "/test-vectors", 
				"-m", modelDIR, "-l", workingFULL + "/labelindex", 
				"-ow", "-o", workingFULL + "/nbayes-testing" };
		
		String[] testontestargsmod = addComplementary(new ArrayList<String>(Arrays.asList(testontestargs)));
		
		return testontestargsmod;
	}

	
	public String[] addtoSeq2Sparse(ArrayList<String> arg)
	{
		if(logNormalize)
		{
			arg.add("-lnorm");
		}
		String[] result = new String[arg.size()];
		result = arg.toArray(result);
		return result;
	}
	
	
	public String[] addComplementary(ArrayList<String> arg)
	{
		if(trainComplementary)
		{
			arg.add("-c");
		}
		String[] result = new String[arg.size()];
		result = arg.toArray(result);
		return result;
	}
		
}
