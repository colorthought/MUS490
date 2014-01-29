package com.dmt.mahout.classification.text;

import java.util.ArrayList;
import java.util.List;

import com.google.common.base.Splitter;
import com.google.common.collect.ConcurrentHashMultiset;
import com.google.common.collect.Lists;
import com.google.common.collect.Multiset;

public class Line {
	private static final String SEPARATOR = "\t";
	private static final String TEXTSEPARATOR = ", ";
	private static final Splitter onTabs = Splitter.on(SEPARATOR);
	private static final Splitter onComma = Splitter.on(TEXTSEPARATOR);
	public List<String> data;
	private Object[] dataArray;
	public int lineLength;
	private Multiset<String> words = ConcurrentHashMultiset.create();


	public Line(String line)
	{
		data = Lists.newArrayList(onTabs.split(line));
		dataArray = data.toArray();
		lineLength = line.length();

	}
	
	public Line(List<String> ar)
	{
		ArrayList<String> constructorArray = new ArrayList<String>(ar);
		data = constructorArray;
		dataArray = data.toArray();
		lineLength = ar.toString().length();
	}

	public double getDouble(int field)
	{
		return Double.parseDouble(data.get(field));
	}
	
	public double getInt(int field)
	{
		return Integer.parseInt(data.get(field));
	}
		
	public String getSentiment()
	{
		return dataArray[0].toString();
	}
	
	public String getText()
	{
		return data.get(1);
	}
	
}