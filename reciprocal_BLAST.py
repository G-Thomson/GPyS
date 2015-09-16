#! /usr/bin/env python

### reciprocal_BLAST.py ################################################################
### By Geoffrey Thomson

### This script performs a nucleotide reciprocal BLAST on two fasta files input by the user.
### Draws heavily from the online tutorial (http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec11)
### and a script by Hong Qin (https://github.com/hongqin/Simple-reciprocal-best-blast-hit-pairs)

from Bio.Blast.Applications import NcbiblastnCommandline
from subprocess import call
import sys, re, os

if len(sys.argv) < 4:
    sys.exit('\n Usage: python %s <Input-FASTA-file-1> <Input-FASTA-file-2> <Output-file.txt>\n' % sys.argv[0])

fasta_file_1 = sys.argv[1]
fasta_file_2 = sys.argv[2]
output_file = sys.argv[3]

# Make databases to BLAST against
call(["makeblastdb", "-in", fasta_file_1, "-parse_seqids", "-dbtype", "nucl", "-out", "DB1.db"])
call(["makeblastdb", "-in", fasta_file_2, "-parse_seqids", "-dbtype", "nucl", "-out", "DB2.db"])

# Perform BLAST alignments
blastn_fasta_file_1_vs_DB_2 = NcbiblastnCommandline(query = fasta_file_1, db = "DB2.db", evalue = 0.001, outfmt = 7, out = "DB2.txt")
stdout, stderr = blastn_fasta_file_1_vs_DB_2()

blastn_fasta_file_2_vs_DB_1 = NcbiblastnCommandline(query = fasta_file_2, db = "DB1.db", evalue = 0.001, outfmt = 7, out = "DB1.txt")
stdout, stderr = blastn_fasta_file_2_vs_DB_1()

# Parse BLAST results, place matches into dictionaries
DB1_results = open("DB2.txt", 'r')
Dict_2 = {} 
for Line in DB1_results:
    if (Line[0] != '#'):
        Line.strip()
        Elements = re.split('\t', Line)
        queryId = Elements[0]
        subjectId = Elements[1]
        if (not( queryId in Dict_2.keys())):
            Dict_2[queryId] = subjectId  

DB1_results = open("DB1.txt", 'r')
Dict_1 = {} 
for Line in DB1_results:
    if (Line[0] != '#'):
        Line.strip()
        Elements = re.split('\t', Line)
        queryId = Elements[0]
        subjectId = Elements[1]
        if (not(queryId in Dict_1.keys())):
            Dict_1[queryId] = subjectId  

# Identify reciprocal best hits and put them in a new dictionary
RBH = {}
for id1 in Dict_1.keys():
    value1 = Dict_1[id1]
    #print(id1, value1)
    if (value1 in Dict_2.keys()):
        if (id1 == Dict_2[value1]) : 
            RBH[value1] = id1

# Write results to an output file 
output = open(output_file, 'w')

header = fasta_file_1 + "\t" +  fasta_file_2 + "\n"
output.write(header)

for pair in RBH.keys():
    line = pair + '\t' + RBH[pair] + '\n'
    output.write(line)


print("\n Identified %s reciprocal best BLAST hists between %s and %s \n" % (len(RBH), fasta_file_1, fasta_file_2))

output.close()

# Clean up created files
filelist = [ f for f in os.listdir(".") if f.startswith(("DB1", "DB2")) ]
for f in filelist:
    os.remove(f)