package com.dmt.mahout.classification.text;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;


import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.util.Version;
import org.apache.mahout.classifier.naivebayes.NaiveBayesModel;
import org.apache.mahout.classifier.sgd.L1;
import org.apache.mahout.classifier.sgd.OnlineLogisticRegression;
import org.apache.mahout.math.DenseVector;
import org.apache.mahout.math.RandomAccessSparseVector;
import org.apache.mahout.math.Vector;
import org.apache.mahout.vectorizer.encoders.ConstantValueEncoder;
import org.apache.mahout.vectorizer.encoders.FeatureVectorEncoder;
import org.apache.mahout.vectorizer.encoders.StaticWordValueEncoder;
import org.apache.mahout.vectorizer.encoders.TextValueEncoder;

import com.dmt.lucene.preprocessor.TokenizerVectorizer;
import com.google.common.collect.ConcurrentHashMultiset;
import com.google.common.collect.HashMultiset;
import com.google.common.collect.Multiset;

public class CSVEncoderLine {

	private static final int FIELDS = 10;
	private static final int FEATURES = 10000;
	private static Multiset<String> overallCounts;
	private static int WordGrams = 2;
	
	private FileReader filereader;
	private BufferedReader in;
	private Map<String, Set<Integer>> traceDictionary = new TreeMap<String, Set<Integer>>();
	private static Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_36);
	private static final TextValueEncoder encoder = new TextValueEncoder("text");
	private static final FeatureVectorEncoder bias = new ConstantValueEncoder("Intercept");

	static String currentClass;
	static String currentText;
	

	public CSVEncoderLine(String filename)
	{
		encoder.setProbes(10);
		try {
			this.filereader = new FileReader(filename);
		} catch (FileNotFoundException e) {
			System.out.println("Datafile not found. Please construct with a useable file type.");
			e.printStackTrace();
		}
		in = new BufferedReader(filereader);
	}
	
	/**
	 * Constructs a CSVEncoderLine with a filename and specified number of WordGrams.
	 * @param filename
	 * @param WordGrams
	 */
	public CSVEncoderLine(String filename, int WordGrams)
	{
		this.WordGrams = WordGrams;
		try {
			filereader = new FileReader(filename);
		} catch (FileNotFoundException e) {
			System.out.println("Datafile not found. Please construct with a useable file type.");
			e.printStackTrace();
		}
		in = new BufferedReader(filereader);
	}


	public Vector ToDoubleVector() throws IOException {
		FeatureVectorEncoder[] encoder = new FeatureVectorEncoder[FIELDS];
		for (int i = 0; i < FIELDS; i++) {
			encoder[i] = new ConstantValueEncoder("v" + i);
		}
		long t0 = System.currentTimeMillis();
		Vector v = new DenseVector(1000);
		BufferedReader in = new BufferedReader(filereader);
		String line = in.readLine();
		while (line != null) {
			v.assign(0);
			Line x = new Line(line);		
			//[DEBUG]
			//System.out.println(x.getSentiment());
			//System.out.println(x.getText());
	
			for (int i = 0; i < FIELDS; i++)
			{
				encoder[i].addToVector(x.getSentiment(), 1.0, v);
				encoder[i].addToVector(x.getText(), 1.0, v);
			}
			line = in.readLine();
		}
		System.out.printf("\nElapsed time = %.3f s\n",
				(System.currentTimeMillis() - t0) / 1000.0);
		
		return v;
	}

	
	public String readCSVFirstLine() throws IOException
	{
		List<String> trainingSet = new ArrayList<String>();
		encoder.setTraceDictionary(traceDictionary);
		bias.setTraceDictionary(traceDictionary);
		String line = in.readLine();
		return line;
	}
	
	public String readCSVNewLines() throws IOException
	{
		String line = in.readLine();
		return line;
	}
	
	public void MakeLine(String line)
	{
		Line x = new Line(line);	
		currentClass = x.getSentiment();
		currentText = x.getText();
	}
	
	public String getCurrentSentiment(String line)
	{
		return currentClass;
	}
	
	public String getCurrentText(String line)
	{
		return currentText;
	}

	public Vector encodeFeatureVector(String line) throws IOException
	{	
		Line x = new Line(line);	
		String currentText = x.getText();
		//[DEBUG] ------------------------------------------------------
		//System.out.println(currentText.toLowerCase());
		TokenizerVectorizer tokenvector = new TokenizerVectorizer();
		List<String> NGrams = tokenvector.TokenizeAsNGrams(currentText.toLowerCase(), WordGrams);
		String NGramsAsString = (NGrams.toString()).toLowerCase();
		//[DEBUG] ------------------------------------------------------
		//System.out.println(NGramsAsString);
		encoder.addText(NGramsAsString);
		
		Vector v = new RandomAccessSparseVector(FEATURES);
		bias.addToVector((byte[]) null, 1, v);
		encoder.flush(1, v);
		return v;
		
	}

}
