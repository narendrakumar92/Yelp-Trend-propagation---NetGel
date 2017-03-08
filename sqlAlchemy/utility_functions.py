#!/usr/bin/python

import csv
from numpy import genfromtxt

def get_csv_data_numpy(file_name):
	data = genfromtxt(file_name, delimiter=',', skip_header=1, converters={0: lambda s: str(s)})
	return data.tolist()
	
def get_csv_data(filepath):
	with open(filepath, 'r') as csvfile:
#		sample = csvfile.read(1024)
#		dialect = csv.Sniffer().sniff(sample, [';',',','|'])
		csvfile.seek(0)
#		reader = csv.reader(csvfile,dialect=dialect)
		reader = csv.reader(csvfile)
		header = next(reader)
		lines = []
		for line in reader:
			lines.append(line)
		return lines
