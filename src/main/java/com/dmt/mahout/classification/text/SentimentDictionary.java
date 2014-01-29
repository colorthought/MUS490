package com.dmt.mahout.classification.text;

import java.util.List;

import org.apache.mahout.vectorizer.encoders.Dictionary;

public class SentimentDictionary extends Dictionary {
	
	static final String[] SENTIMENTS = { "positive", "mutual", "negative", };
	
	public SentimentDictionary()
	{
		//[DEBUG] -----------------------------------------------------------
		//for (int i = 0; i < SENTIMENTS.length; i++)
		//{
		//	this.intern(SENTIMENTS[i]);
		//}
	}
	
	public SentimentDictionary(String[] newSentiments)
	{
		for (int i = 0; i < newSentiments.length; i++)
		{
			this.intern(newSentiments[i]);
		}
	}
	
	public String listSentiments()
	{
		return this.toString();
	}
	

}
