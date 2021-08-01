#!/usr/bin/env python

import os
import sys
import re
import csv
import textwrap as tw
import pysam
from  datetime import datetime
import argparse
import yaml
import json


def get_sample_name_from_fasta(file,
                               pattern=['\.consensus.fasta',
                                        '\.consensus.fa',
                                        '\.primertrimmed.consensus.fa',
                                        '\.primertrimmed.consensus.fasta']):
    '''
    Extracts the sample name based on the removal of the pattern.
    Arguments:
        * file:     FASTA filename
        * pattern:  a list of search strings to remove from file (default:
                    .consensus.fasta, .consensus.fa)
    Return Value:
        Returns the sample name extracted from the FASTA filename.
    '''
    _search = '(?:% s)' % '|'.join(pattern)
    return re.sub(_search, '', os.path.basename(file))


def create_fasta_header(virus, sample_id, country, year):
    """
    Replace a FASTA header with a VirusSeq compatible version:
        ">hCoV-19/Canada/ON-samplename/2021"
    """
    fasta_id = '/'.join([virus, country, sample_id, str(year)])
    fasta_header = ''.join(['>', fasta_id])
    return fasta_header


def create_fasta_record(fasta, header):
    """
    Create a FASTA record
    """
    fasta_record = list()
    fasta_record.append(header)
    fasta = pysam.FastxFile(fasta)
    for record in fasta:
        fasta_record.extend(tw.wrap(str(record.sequence), width=60))
    return fasta_record


def get_consensus_fasta_files(path=os.getcwd(),
                              year=datetime.now().year):
    """
    Get a list of FASTA files from the provided path

    Arguments:
        * path: full path to the directory containing FASTA files

    Return Value:
        Returns an array of dictionaries where the key is the
        sample name and the value is the full path to the FASTA
        file.
    """
    consensus_files = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if is_fasta(file):
                sample_name = get_sample_name_from_fasta(file=file)
                consensus_files.append({sample_name :
                    {'consensus' : '/'.join([root, file]),
                     'fasta_header' : create_fasta_header(virus='hCoV-19',
                                                          sample_id='-'.join(['ON', sample_name]),
                                                          country='Canada',
                                                          year=year)
                     }})
            else:
                continue
    return consensus_files


def is_fasta(file, pattern=['\.consensus.fasta',
                            '\.consensus.fa',
                            '\.primertrimmed.consensus.fa',
                            '\.primertrimmed.consensus.fasta']):
    """
    Determine whether a file is FASTA formatted.

    Arguments:
        * file:     filename to search FASTA pattern
        * pattern:  a list of search strings

    Return Values:
        Returns a boolean
    """
    _search = '(?:% s)' % '|'.join(pattern)
    return re.search(_search, file)


def create_metadata(row, sample, lab):
    """
    Construct the metadata row 
    """
    data = dict()
    data = {"study_id": lab["study_id"],
            "specimen collector sample ID": sample,
            "sample collected by": lab["sample_collected_by"],
            "sequence submitted by": lab["submitted_by"],
            "sample collection date": row["qc"]["collection_date"],
            "sample collection date null reason": "Not Provided",
            "geo_loc_name (country)": lab["country"],
            "geo_loc_name (state/province/territory)": lab["province"],
            "organism": "Not Provided",
            "isolate": re.sub('^>', '', row["fasta_header"]),
            "fasta header name": re.sub('^>', '', row["fasta_header"]),
            "purpose of sampling": "Not Provided",
            "purpose of sampling details": "Not Provided",
            "anatomical material": "Not Provided",
            "anatomical part": "Not Provided",
            "body product": "Not Provided",
            "environmental material": "Not Provided",
            "environmental site": "Not Provided",
            "collection device": "Not Provided",
            "collection method": "Not Provided",
            "host (scientific name)": lab["host"],
            "host disease": "Not Provided",
            "host age": "Not Provided",
            "host age null reason": "Not Provided",
            "host age unit": "Not Provided",
            "host age bin": "Not Applicable",
            "host gender": "Not Provided",
            "purpose of sequencing": "Not Provided",
            "purpose of sequencing details": "Not Provided",
            "sequencing instrument": lab["sequencing_instrument"],
            "sequencing protocol": "",
            "raw sequence data processing method": "",
            "dehosting method": "",
            "consensus sequence software name": lab["consensus_sequencing_software_name"],
            "consensus sequence software version": lab["consensus_sequencing_software_version"],
            "breadth of coverage value": "",
            "depth of coverage value": row["qc"]["mean_sequencing_depth"],
            "reference genome accession": "",
            "bioinformatics protocol": "",
            "gene name": "",
            "diagnostic pcr Ct value": row["qc"]["qpcr_ct"]}
    return data


def get_metadata_header():
    """
    Return a tab separated string representing the metadata header
    """
    header = ["study_id",
              "specimen collector sample ID",
              "sample collected by",
              "sequence submitted by",
              "sample collection date",
              "sample collection date null reason",
              "geo_loc_name (country)",
              "geo_loc_name (state/province/territory)",
              "organism",
              "isolate",
              "fasta header name",
              "purpose of sampling",
              "purpose of sampling details",
              "anatomical material",
              "anatomical part",
              "body product",
              "environmental material",
              "environmental site",
              "collection device",
              "collection method",
              "host (scientific name)",
              "host disease",
              "host age",
              "host age null reason",
              "host age unit",
              "host age bin",
              "host gender",
              "purpose of sequencing",
              "purpose of sequencing details",
              "sequencing instrument",
              "sequencing protocol",
              "raw sequence data processing method",
              "dehosting method",
              "consensus sequence software name",
              "consensus sequence software version",
              "breadth of coverage value",
              "depth of coverage value",
              "reference genome accession",
              "bioinformatics protocol",
              "gene name",
              "diagnostic pcr Ct value"]
    return header


def create_metadata_string(metadata, delimiter='\t'):
    """
    Return a string containing the VirusSeq metadata

    Arguments:
        * metadata: the metadata as a dictionary

    Return Value:
        * returns a string with tab separated values for VirusSeq metadata
    """
    return delimiter.join([metadata["study_id"],
        metadata["specimen collector sample ID"],
        metadata["sample collected by"],
        metadata["sequence submitted by"],
        metadata["sample collection date"],
        metadata["sample collection date null reason"],
        metadata["geo_loc_name (country)"],
        metadata["geo_loc_name (state/province/territory)"],
        metadata["organism"],
        metadata["isolate"],
        metadata["fasta header name"],
        metadata["purpose of sampling"],
        metadata["purpose of sampling details"],
        metadata["anatomical material"],
        metadata["anatomical part"],
        metadata["body product"],
        metadata["environmental material"],
        metadata["environmental site"],
        metadata["collection device"],
        metadata["collection method"],
        metadata["host (scientific name)"],
        metadata["host disease"],
        metadata["host age"],
        metadata["host age null reason"],
        metadata["host age unit"],
        metadata["host age bin"],
        metadata["host gender"],
        metadata["purpose of sequencing"],
        metadata["purpose of sequencing details"],
        metadata["sequencing instrument"],
        metadata["sequencing protocol"],
        metadata["raw sequence data processing method"],
        metadata["dehosting method"],
        metadata["consensus sequence software name"],
        metadata["consensus sequence software version"],
        metadata["breadth of coverage value"],
        metadata["depth of coverage value"],
        metadata["reference genome accession"],
        metadata["bioinformatics protocol"],
        metadata["gene name"],
        metadata["diagnostic pcr Ct value"]])


def import_sample_list(file):
    """
    Read a list of samples from a file and import them into a
    list for processing.

    Arguments:
        * file: full path to the file containing sample names to process

    Returns:
        A list of samples
    """
    sample_list = list()
    with open(file, 'r') as ifh:
        for line in ifh:
            sample_list.append(line.rstrip())
    return sample_list


def filter_samples(data, include=[], exclude=[]):
    """
    Filter the data based on a list of sample names
    in an include and exclude list of samples.

    Arguments:
        * data: list of sample dictionaries
        * include: list of names to include
        * exclude: list of names to exclude

    Return Values:
        Returns a list of dictionaries containing
        filtered samples.
    """
    final_samples = list()
    for sample in data:
        for samplename in sample:
            if exclude:
                if samplename in exclude:
                    print(f"Sample found in exclude list: {samplename} skipping...")
                    continue
            if include:
                if samplename in include:
                    print(f"Including sample: {samplename}")
                    final_samples.append(sample)
                else:
                    print(f"Sample not in include list: {samplename}")
            else:
                final_samples.append(sample)
    return final_samples


def import_summary_qc_data(file, delimiter='\t'):
    """
    Import the summary QC data from the ncov-tools pipeline.

    Arguments:
        * file: path to file containing the summary_qc.tsv data
    
    Return Values:
        Returns a list containing samples and the associated
        summary QC data.
    """
    data = list()
    with open(file, 'r') as fh:
        ct_reader = csv.DictReader(fh, delimiter=delimiter)
        for line in ct_reader:
            data.append(line)
    return data


def import_lab_metadata(file):
    """
    Import the lab metadata in YAML format

    Arguments:
        * file: full path to the a config file in YAML format

    Return Value:
        Returns a dictionary containing the lab metadata
    """
    metadata = dict()
    with open(file, 'r') as yp:
        metadata = yaml.full_load(yp)
    return metadata

