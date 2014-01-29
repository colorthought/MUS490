/*
 * Standard Tokenizer/ReutersToSparseVectors. Adapted from 14.1
 * 
 */
package com.dmt.lucene.preprocessor;

import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import java.util.*;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.Token;
import org.apache.lucene.analysis.TokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.StopAnalyzer;
import org.apache.lucene.analysis.StopFilter;
import org.apache.lucene.analysis.ngram.EdgeNGramTokenFilter;
import org.apache.lucene.analysis.ngram.EdgeNGramTokenFilter.Side;
import org.apache.lucene.analysis.ngram.NGramTokenizer;
import org.apache.lucene.analysis.shingle.ShingleAnalyzerWrapper;
import org.apache.lucene.analysis.shingle.ShingleFilter;
import org.apache.lucene.analysis.snowball.SnowballFilter;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.tokenattributes.*;
import org.apache.lucene.analysis.CharArraySet;
import org.apache.lucene.util.Version;
import org.apache.mahout.common.nlp.NGrams;
import org.apache.mahout.math.RandomAccessSparseVector;
import org.apache.mahout.math.SequentialAccessSparseVector;
import org.apache.mahout.math.Vector;
import org.apache.mahout.utils.io.WrappedWriter;
import org.apache.mahout.vectorizer.encoders.FeatureVectorEncoder;
import org.apache.mahout.vectorizer.encoders.StaticWordValueEncoder;
import org.apache.mahout.vectorizer.encoders.TextValueEncoder;
import org.hsqldb.Tokenizer;

/**
 * @author RESKJ001
 * @param sr
 */
public class TokenizerVectorizer {

	protected static String field;
	protected static String valueType;
	static final Version LUCENE_VERSION = Version.LUCENE_36; 
	protected static Analyzer analyzer = new StandardAnalyzer(LUCENE_VERSION);	
	public static final Set<?> STOP_WORDS_SET =	StopAnalyzer.ENGLISH_STOP_WORDS_SET;
	
	/**
	* The default TokenizerVectorizer constructor. Uses the Standard Analyzer.
	*/	
	public TokenizerVectorizer()
	{
		
		TokenizerVectorizer.field = "body";
		TokenizerVectorizer.analyzer = new StandardAnalyzer(Version.LUCENE_36);
	}
	
	
	/**
	* A TokenizerVectorizer that uses a custom Analyzer.
	*/
	public TokenizerVectorizer(Analyzer givenAnalyzer)
	{
		TokenizerVectorizer.field = "body";
		TokenizerVectorizer.analyzer = givenAnalyzer;
	}

	
	/**
	* Tokenizes the given String. Returns as List<String>.
	*/	
	public List<String> Tokenize(String sampleString)
	{
		FeatureVectorEncoder encoder = new StaticWordValueEncoder(valueType);
		StringReader reader = new StringReader(sampleString);
		
	    List<String> result = new ArrayList<String>();
	    	    
	    try 
	    {
	    	TokenStream stream  = analyzer.tokenStream(field, reader);
	    	
	    	stream.reset();
	    	while (stream.incrementToken())
	    	{
	    		result.add(stream.getAttribute(CharTermAttribute.class).toString());
	        }
	    }	catch (IOException e)
	    	{
	    		System.out.println("Failed to add tokens to stream.");
	    		throw new RuntimeException(e);
	    	}
	    
	    return result;
	}
	

	/**
	* Tokenizes the given String as an N-gram. Returns as List<String>.
	* @param gramnum: the number of string grams.
	*/	
	public List<String> TokenizeAsNGrams(String sampleString, int gramnum) throws IOException
	{		
		FeatureVectorEncoder encoder = new StaticWordValueEncoder(valueType);
		StringReader reader = new StringReader(sampleString);
		
	    List<String> result = new ArrayList<String>();
	    	    
	    try 
	    {	 
	    	
	    	TokenStream stream  = analyzer.tokenStream(field, reader);
	    	StopFilter stopFilter = new StopFilter(LUCENE_VERSION, stream, STOP_WORDS_SET);
	    	stopFilter.setEnablePositionIncrements(true);
	    	ShingleFilter shinglefilter = new ShingleFilter(stopFilter, gramnum);
	    	
	    	CharTermAttribute cattr = shinglefilter.addAttribute(CharTermAttribute.class);
	    	shinglefilter.reset();
	    	while (shinglefilter.incrementToken())
	    	{	
	    		String currentToken = cattr.toString();
	    		String currentTokenMod = currentToken.replace("_", "");
	    		//[DEBUG] ------------------------------------------------------------------
	    		//System.out.println(currentTokenMod);
	    		result.add(currentTokenMod);
	    	}
	    }	catch (IOException e)
	    	{
	    		System.out.println("Failed to add tokens to stream.");
	    		throw new RuntimeException(e);
	    	}
	    
	    return result;
	}

	
	/**
	* Tokenizes the given String. Prints resulting String.
	*/		
	public void printTokenizer(String sampleString)
	{
		System.out.println(Tokenize(sampleString));
	}

	/**
	* Tokenizes the given String. Prints resulting String.
	 * @throws IOException 
	*/		
	public void printNGramTokenizer(String sampleString, int gramnum) throws IOException
	{
		System.out.println(TokenizeAsNGrams(sampleString, gramnum));
	}


	public Vector Vectorizer(List<String> Tokenizer, TextValueEncoder encoder, Reader sr) throws IOException
	{
		TokenStream ts = analyzer.tokenStream(field, sr);
		OffsetAttribute osa = ts.addAttribute(OffsetAttribute.class);
		CharTermAttribute cta = ts.addAttribute(CharTermAttribute.class);

		Vector v1 = new RandomAccessSparseVector(100); 
		ts.reset();
		while (ts.incrementToken()) {
		  int startOffset = osa.startOffset();
		  int endOffset = osa.endOffset();
		  String term = cta.toString();
			char[] termBuffer = cta.buffer();
		  int termLen = cta.length();
		  String w = new String(termBuffer, 0, termLen);                 
		  encoder.addToVector(w, 1, v1);                                 
		}
		String result = "%s\n";
		String formatted = String.format((new SequentialAccessSparseVector(v1)).toString());

		return v1;
	}
}
/*		
*/