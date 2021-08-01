#!/usr/bin/env python

import os
import sys
#import re
#import csv
#import textwrap as tw
#import pysam
from  datetime import datetime
import argparse
#import yaml
#import json
from ncov.archive.virusseq import *


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', default='.',
                        help='path to search files')
    parser.add_argument('-q', '--qc', default=None, required=True,
                        help='path to the summary QC file from ncov-tools')
    parser.add_argument('-l', '--lab', default=None, required=True,
                        help='path to the lab metadata YAML file')
    parser.add_argument('-i', '--include', default=None,
                        help='path to file containing list of samples to include for processing')
    parser.add_argument('-e', '--exclude', default=None,
                        help='path to file containing list of samples to exclude from processing')
    return parser.parse_args()


def main():
    """
    Main program
    """
    submission_to = "virusseq"
    args = init_args()
    include_list = list()
    exclude_list = list()
    final_samples = list()
    multi_fasta_list = list()

    # create the list of dictionaries per sample
    consensus_genomes = get_consensus_fasta_files(path=args.path)

    # filter samples found in the include and exclude files
    if args.include:
        include_list = import_sample_list(file=args.include)
    if args.exclude:
        exclude_list = import_sample_list(file=args.exclude)
    final_samples = filter_samples(data=consensus_genomes,
                                   include=include_list,
                                   exclude=exclude_list)
    
    qc_data = import_summary_qc_data(file=args.qc)

    merged_samples = dict()
    for sample in final_samples:
        for samplename in sample:
            merged_samples.update(sample)
            merged_samples[samplename]['qc'] = next(item for item in qc_data if item['sample'] == samplename)

    lab_data = import_lab_metadata(file=args.lab)
    outfile_prefix = f'{datetime.now().strftime("%Y%m%d")}_{lab_data["sample_collected_by_short"]}_{submission_to}'
    
    metadata_list = list()

    meta_ofh = open(f'{outfile_prefix}.tsv', 'w')
    meta_ofh.write('\t'.join(get_metadata_header()))
    meta_ofh.write('\n')
    for samplename in merged_samples:
        meta_ofh.write(create_metadata_string(metadata=create_metadata(row=merged_samples[samplename], sample=samplename, lab=lab_data)))
        meta_ofh.write("\n")
        multi_fasta_list.extend(create_fasta_record(fasta=merged_samples[samplename]['consensus'],
                                                    header=merged_samples[samplename]['fasta_header']))
    meta_ofh.close()

    with open(f'{outfile_prefix}.fasta', 'w') as fasta_ofh:
        for line in multi_fasta_list:
            fasta_ofh.write(line)
            fasta_ofh.write("\n")
    fasta_ofh.close()



if __name__ == '__main__':
    main()


#__END__
