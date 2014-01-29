package com.dmt.mahout.classification.text;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.SequenceFile;
import org.apache.hadoop.io.SequenceFile.Writer;
import org.apache.hadoop.io.Text;
import org.apache.mahout.utils.vectors.io.SequenceFileVectorWriter;
import org.apache.mahout.utils.vectors.io.VectorWriter;

/**
 * @class TSVToTrainingSetSeq
 * @author RESKJ001
 * 
 * Class for converting TSV files to Mahout sequence files. Splits data into 80/20 split
 * of training/test data.
 * 
 */
public class TSVToSeq {
	
	private static String inputFileName;
	private static String outputDirName;
	
	public TSVToSeq(String[] args)
	{
		if (args.length != 2) {
			System.err.println("Arguments: [input tsv file] [output sequence file]");
			return;
		}
		inputFileName = args[0];
		outputDirName = args[1];
		System.out.println("writing " + inputFileName + " to " + outputDirName);
		
	}
	
	public void CreateSequence() throws Exception {
		Configuration configuration = new Configuration();
		FileSystem fs = FileSystem.get(configuration);
		
		Writer writer = new SequenceFile.Writer(fs, configuration, new Path(outputDirName + "/chunk-0"),
				Text.class, Text.class);
		
		int count = 0;
		BufferedReader reader = new BufferedReader(new FileReader(inputFileName));
		Text key = new Text();
		Text value = new Text();
		while(true) {
			String line = reader.readLine();
			if (line == null) {
				break;
			}
			String[] tokens = line.split("\t", 3);
			if (tokens.length != 3) {
				System.out.println("Skip line: " + line);
				continue;
			}
			String category = tokens[0];
			String id = tokens[1];
			String message = tokens[2];
			key.set("/" + category + "/" + id);
			value.set(message);
			writer.append(key, value);
			count++;
		}
		writer.close();
		System.out.println("Wrote " + count + " entries.");
		
	}
}
