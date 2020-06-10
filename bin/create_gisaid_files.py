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
parser.add_argument('-m', '--meta', help='meta file')
parser.add_argument('-q', '--qc', help='the summary QC file')
parser.add_argument('-i', '--include', help='a list of samples to be included',
                    default=None)
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

include_list = []
if args.include:
    include_list = gisaid.import_sample_include_list(file=args.include)
qc_dict =  {}
qc_dict = gisaid.get_coverage_dictionary(file=args.qc)
metadata = gisaid.import_uhtc_metadata(file=args.meta)

# create the metadata file which will be imported into Excel for
# GISAID upload
file_o = open(args.output, 'w')
file_o.write(gisaid.get_column_header())
file_o.write("\n")
file_o.write(gisaid.get_column_header_name())
file_o.write("\n")
gisaid_samples = gisaid.get_consensus_fasta_files(path=os.getcwd())
for gisaid_sample in gisaid_samples:
    for samplename in gisaid_sample:
        if samplename in metadata:
            date = metadata[samplename]['collection_date']
        else:
            date = 'unknown'
        # if the include list is not empty, filter those samples in the include
        # list
        _sample_dict = gisaid.create_metadata_dictionary(consensus=gisaid_sample[samplename]['consensus'],
                                                         sample_name=samplename,
                                                         fasta_header=gisaid_sample[samplename]['fasta_header'],
                                                         date=date)
        if include_list:
            if samplename in include_list:
                file_o.write(gisaid.create_metadata_string(_sample_dict))
                file_o.write("\n")
            else:
                print(' '.join(['Excluding sample: ', samplename]))
                continue
        else:
            file_o.write(gisaid.create_metadata_string(_sample_dict))
            file_o.write("\n")