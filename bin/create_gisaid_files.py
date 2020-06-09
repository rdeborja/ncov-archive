#!/usr/bin/env python
'''
Create the required files for GISAID uploads.
'''

import os
import sys
import argparse
import ncov.archive.gisaid as gisaid

parser = argparse.ArgumentParser(description='Create required GISAID files')
parser.add_argument('-o', '--output', help='filename to write metadata to')
parser.add_argument('-p', '--path', default=os.getcwd(), help='path to search')
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

file_o = open(args.output, 'w')
file_o.write(gisaid.get_column_header())
file_o.write("\n")
file_o.write(gisaid.get_column_header_name())
file_o.write("\n")
gisaid_samples = gisaid.get_consensus_fasta_files(path=os.getcwd())
for gisaid_sample in gisaid_samples:
    for samplename in gisaid_sample:
        _sample_dict = gisaid.create_metadata_dictionary(consensus=gisaid_sample[samplename]['consensus'],
                                                         sample_name=samplename,
                                                         fasta_header=gisaid_sample[samplename]['fasta_header'])
        file_o.write(gisaid.create_metadata_string(_sample_dict))
        file_o.write("\n")
