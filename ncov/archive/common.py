'''
Common functions for ncov.archive
'''

import os
import re
import csv
import textwrap as tw
import pysam

def create_fasta_header(virus, sample_id, country, year):
    '''
    Replace a FASTA header with a GISAID compatible version:
        ">hCoV-19/Canada/ON-samplename/2020"
    '''
    fasta_id = '/'.join([virus, country, sample_id, str(year)])
    fasta_header = ''.join(['>', fasta_id])
    return fasta_header


def create_fasta_record(fasta, header):
    '''
    Create a FASTA record
    '''
    fasta_record = list()
    fasta_record.append(header)
    fasta = pysam.FastxFile(fasta)
    for record in fasta:
        fasta_record.extend(tw.wrap(str(record.sequence), width=60))
    return fasta_record


def is_file_fasta(file, pattern=['\.consensus.fasta',
                                 '\.consensus.fa',
                                 '\.primertrimmed.consensus.fa']):
    '''
    Returns a boolean after determining whether the file is a consensus FASTA file.

    Arguments:
        * file:     filename to search FASTA pattern for
        * pattern:  a list of search strings (default: .consensus.fasta, .consensus.fa)

    Return Values:
        Returns a boolean
    '''
    _search = '(?:% s)' % '|'.join(pattern)
    return re.search(_search, file)


def get_sample_name_from_fasta(file,
                               pattern=['\.consensus.fasta',
                                        '\.consensus.fa',
                                        '\.primertrimmed.consensus.fa']):
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

