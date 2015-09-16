#! /usr/bin/env python

### summary_of_fasta_seqs.py ################################################################
### By Geoffrey Thomson

### This script I modified from the online tutorial  
### (http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec11). 
### It takes a FASTA file as input and produces a list of FASTA seq IDs 
### and their lengths. Also gives you a total number of sequences.  

from Bio import SeqIO
import sys, re

if len(sys.argv) < 2:
    sys.exit('\n Usage: python %s <FASTA-file>\n' % sys.argv[0])

input_file = sys.argv[1]

# Places sequemce objects into a list
records = list(SeqIO.parse(input_file , "fasta"))

# Print header
print
print("ID\tLength (bases)\t%A\t%C\t%G\t%T")

# This function will work out the percentage of a base
def seq_perc(x):
	res = round(x/length, 4) * 100
	return res

# Loop throug the records list and print out summary statistics
for s in records:
	sequence = s.seq.upper()
	length = float(len(s.seq))
	print s.id, "\t",  int(length), "\t", seq_perc(sequence.count('A')), "\t", seq_perc(sequence.count('C')), "\t", seq_perc(sequence.count('G')), "\t", seq_perc(sequence.count('T'))

print 
print("Found %i records" % len(records))
print