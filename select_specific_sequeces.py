#!/usr/bin/python

### select_specific_sequences.py ################################################################
### By Geoffrey Thomson

### This script I modified from the online tutorial  
### (http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec11). 
### It takes a fasta file and txt file of fasta IDs as input and extracts the  
### sequences which match the fasta IDs and places them in a new file.  

from Bio import SeqIO
import sys

if len(sys.argv) < 4:
    sys.exit('\n Usage: python %s <FASTA-file> <ID-file> <Output-file>\n\n NOTE: there should be no ">" symbols in front of the IDs' % sys.argv[0])

# Input and output files
input_file = sys.argv[1]
id_file = sys.argv[2]
output_file = sys.argv[3]

# Places desired sequences into a set (unordered) of unique IDs
wanted = set(line.rstrip("\n").split(None,1)[0] for line in open(id_file))
print("Found %i unique identifiers in %s" % (len(wanted), id_file))

# Picks out desired fasta sequences if the IDs match those in the "wanted" set 
records = (r for r in SeqIO.parse(input_file, "fasta") if r.id in wanted)
count = SeqIO.write(records, output_file, "fasta")

print("Saved %i records from %s to %s" % (count, input_file, output_file))
if count < len(wanted):
    print("Warning %i IDs not found in %s" % (len(wanted)-count, input_file))