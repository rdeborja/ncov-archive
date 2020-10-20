#!/usr/bin/env python
'''
Create the required files for GISAID uploads.
'''

import os
import sys
import argparse
import yaml
import datetime
import ncov.archive.gisaid as gisaid

parser = argparse.ArgumentParser(description='Create required GISAID files')
parser.add_argument('-o', '--output', help='filename to write metadata to')
parser.add_argument('-p', '--path', default=os.getcwd(), help='path to search')
parser.add_argument('-m', '--meta', help='meta file')
parser.add_argument('-q', '--qc', help='the summary QC file')
parser.add_argument('-f', '--fasta', help='filename of output fasta')
parser.add_argument('-i', '--include', help='a list of samples to be included',
                    default=None)
parser.add_argument('-e', '--exclude', help='a list of samples to remove',
                    default=None)
parser.add_argument('-c', '--config', help='YAML file containing GISAID run config')
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

year = datetime.date.today().year
config = dict()
with open(args.config, 'r') as yaml_p:
    config = yaml.full_load(yaml_p)

include_list = []
if args.include:
    include_list = gisaid.import_sample_include_list(file=args.include)
exclude_list = []
if args.exclude:
    exclude_list = gisaid.import_sample_exclude_list(file=args.exclude)

qc_dict =  {}
qc_dict = gisaid.get_coverage_dictionary(file=args.qc)
metadata = gisaid.import_uhtc_metadata(file=args.meta)
multi_fasta_list = []

# create the metadata file which will be imported into Excel for
# GISAID upload
file_o = open(args.output, 'w')
file_o.write(gisaid.get_column_header())
file_o.write("\n")
file_o.write(gisaid.get_column_header_name())
file_o.write("\n")
gisaid_samples = gisaid.get_consensus_fasta_files(path=args.path, year=year)

for gisaid_sample in gisaid_samples:
    for samplename in gisaid_sample:
        if exclude_list:
            if samplename in exclude_list:
                print(' '.join(['Sample found in exclude list: ', samplename]))
                continue
        if samplename in metadata:
            date = metadata[samplename]['collection_date']
        else:
            date = 'unknown'
        # if the include list is not empty, filter those samples in the include
        # list
        _sample_dict = gisaid.create_metadata_dictionary(consensus=gisaid_sample[samplename]['consensus'],
                                                         sample_name=samplename,
                                                         fasta_header=gisaid_sample[samplename]['fasta_header'],
                                                         coverage=qc_dict[samplename]['mean_depth'],
                                                         fasta_file=args.fasta,
                                                         date=date,
                                                         config=config)
        if include_list:
            if samplename in include_list:
                multi_fasta_list.extend(gisaid.create_fasta_record(fasta=gisaid_sample[samplename]['consensus'],
                                                                   header=gisaid_sample[samplename]['fasta_header']))
                file_o.write(gisaid.create_metadata_string(_sample_dict))
                file_o.write("\n")
            else:
                print(' '.join(['Excluding sample: ', samplename]))
                continue
        else:
            multi_fasta_list.extend(gisaid.create_fasta_record(fasta=gisaid_sample[samplename]['consensus'],
                                                                header=gisaid_sample[samplename]['fasta_header']))
            file_o.write(gisaid.create_metadata_string(_sample_dict))
            file_o.write("\n")
# write the multi-sample FASTA list to a file
with open(args.fasta, 'w') as fasta_out:
    for line in multi_fasta_list:
        fasta_out.write(line)
        fasta_out.write("\n")
