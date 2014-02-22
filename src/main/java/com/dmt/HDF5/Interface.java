package com.dmt.HDF5;
import ncsa.hdf.hdf5lib.*;
import ncsa.hdf.hdf5lib.exceptions.HDF5LibraryException;

import java.io.*;

public class Interface {

	public static void main(String[] args)
	{
		try
		{
			int flags = 0;
			int access = 0;
			int file = H5.H5Fopen("myFile.hdf", flags, access );
			} catch (HDF5LibraryException e) {
				
			} 
	} 
}

