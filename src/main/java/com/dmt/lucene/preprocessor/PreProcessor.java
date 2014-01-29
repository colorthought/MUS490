package com.dmt.lucene.preprocessor;

import java.io.IOException;
import java.io.Reader;

import org.apache.lucene.analysis.standard.ClassicTokenizer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.standard.StandardFilter;
import org.apache.lucene.analysis.Tokenizer;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.synonym.SynonymFilter;
import org.apache.lucene.analysis.synonym.SynonymMap;
import org.apache.lucene.analysis.synonym.WordnetSynonymParser;

import org.apache.lucene.util.CharsRef;
import org.apache.lucene.util.Version;


public class PreProcessor
{
	static final Version LUCENE_VERSION = Version.LUCENE_36; 
	
	static Analyzer analyzer()
	{	
		Analyzer analyzer = new StandardAnalyzer(LUCENE_VERSION);
		return analyzer;
	}
	
	
	public static void main(String[] args) throws IOException
	{
			    
	    TokenizerVectorizer maintv = new TokenizerVectorizer(analyzer());
	    maintv.printNGramTokenizer(TestStrings.testString1, 4);
	 
	}

}
