package com.dmt.mahout.classification.text;

import java.io.IOException;
import java.io.Reader;
import java.util.Collection;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;

public class WordCounter {

	public WordCounter()
	{
		
	}
	
	/**
	 * 
	 * Counts words
	 * 
	 * @param analyzer
	 * @param words
	 * @param in
	 * @throws IOException
	 */
	
	public static void countWords(Analyzer analyzer, Collection<String> words,
			Reader in) throws IOException {

		//System.out.println( "> ----- countWords ------" );

		TokenStream ts = analyzer.tokenStream("text", in);
		ts.addAttribute(CharTermAttribute.class);
		ts.reset();
		while (ts.incrementToken()) {
			String s = ts.getAttribute(CharTermAttribute.class).toString();
			// System.out.print( " " + s );
			words.add(s);
		}

		// System.out.println( "\n<" );

		/* overallCounts.addAll(words); */
	}

}
