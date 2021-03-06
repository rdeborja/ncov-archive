'''
A Python module for handling files for uploading to GISAID.
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
        


def get_consensus_fasta_files(path=os.getcwd(), year='2020'):
    '''
    Create an array of dictionaries containing the sample and FASTA consensus file.

    Arguments:
        * path: full path to the directory containing FASTA files

    Return Value:
        The function returns an array of dictionaries where the key is the
        sample name and the value is the full path to the FASTA file
    '''
    consensus_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if is_file_fasta(file):
                sample_name = get_sample_name_from_fasta(file=file)
                consensus_files.append({sample_name :
                    {'consensus' : '/'.join([root, file]),
                     'fasta_header' : create_fasta_header(virus='hCoV-19',
                         sample_id='-'.join(['ON', sample_name]),
                     country='Canada', year=year)
                    }})
    return consensus_files


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


def init_metadata_dictionary():
    '''

    '''
    metadata_record = {}


def create_metadata_dictionary(config, consensus, sample_name, fasta_header,
                               coverage, fasta_file, date='unknown'):
    '''
    Create a dictionary containing metadata fields used in the GISAID template.
    '''
    metadata_record = {}
    metadata_record['Submitter'] = config['submitter']
    metadata_record['FASTA_filename'] = os.path.basename(fasta_file)
    metadata_record['Virus_name'] = re.sub('^>', '', fasta_header)
    metadata_record['Type'] = config['type']
    metadata_record['Passage_details_history'] = 'Original'
    metadata_record['Collection_date'] = date
    metadata_record['Location'] = config['location']
    metadata_record['Additional_location_information'] = ''
    metadata_record['Host'] = config['host']
    metadata_record['Additional_host_information'] = ''
    metadata_record['Gender'] = 'unknown'
    metadata_record['Patient_age'] = 'unknown'
    metadata_record['Patient_status'] = 'unknown'
    metadata_record['Specimen_source'] = ''
    metadata_record['Outbreak'] = ''
    metadata_record['Last_vaccinated'] = ''
    metadata_record['Treatment'] = ''
    metadata_record['Sequencing_technology'] = config['platform']
    metadata_record['Assembly_method'] = config['assembly_method']
    metadata_record['Coverage'] = coverage
    metadata_record['Originating_lab'] = config['originating_lab']
    metadata_record['Originating_lab_Address'] = f'\"{config["originating_lab_address"]}\"'
    metadata_record['Sample_ID_given_by_the_sample_provider'] = sample_name
    metadata_record['Submitting_lab'] = config['submitting_lab']
    metadata_record['Submitting_lab_Address'] = f'\"{config["submitting_lab_address"]}\"'
    metadata_record['Sample_ID_given_by_submitting_laboratory'] = sample_name
    metadata_record['Authors'] = f'\"{config["authors"]}\"'
    return metadata_record


def create_metadata_string(metadata, delimiter=','):
    '''

    '''
    return delimiter.join([
        metadata['Submitter'],
        metadata['FASTA_filename'],
        metadata['Virus_name'],
        metadata['Type'],
        metadata['Passage_details_history'],
        metadata['Collection_date'],
        metadata['Location'],
        metadata['Additional_location_information'],
        metadata['Host'],
        metadata['Additional_host_information'],
        metadata['Gender'],
        metadata['Patient_age'],
        metadata['Patient_status'],
        metadata['Specimen_source'],
        metadata['Outbreak'],
        metadata['Last_vaccinated'],
        metadata['Treatment'],
        metadata['Sequencing_technology'],
        metadata['Assembly_method'],
        metadata['Coverage'],
        metadata['Originating_lab'],
        metadata['Originating_lab_Address'],
        metadata['Sample_ID_given_by_the_sample_provider'],
        metadata['Submitting_lab'],
        metadata['Submitting_lab_Address'],
        metadata['Sample_ID_given_by_submitting_laboratory'],
        metadata['Authors']])

def get_column_header(delimiter=','):
    '''
    Get the column headers.
    '''
    return delimiter.join([
        'submitter',
        'fn',
        'covv_virus_name',
        'covv_type',
        'covv_passage',
        'covv_collection_date',
        'covv_location',
        'covv_add_location',
        'covv_host',
        'covv_add_host_info',
        'covv_gender',
        'covv_patient_age',
        'covv_patient_status',
        'covv_specimen',
        'covv_outbreak',
        'covv_last_vaccinated',
        'covv_treatment',
        'covv_seq_technology',
        'covv_assembly_method',
        'covv_coverage',
        'covv_orig_lab',
        'covv_orig_lab_addr',
        'covv_provider_sample_id',
        'covv_subm_lab',
        'covv_subm_lab_addr',
        'covv_subm_sample_id',
        'covv_authors'])


def get_column_header_name(delimiter=','):
    '''
    Get the column header names.
    '''
    return delimiter.join([
        'Submitter',
        'FASTA filename',
        'Virus name',
        'Type',
        'Passage details/history',
        'Collection date',
        'Location',
        'Additional location information',
        'Host',
        'Additional host information',
        'Gender',
        'Patient age',
        'Patient status',
        'Specimen source',
        'Outbreak',
        'Last vaccinated',
        'Treatment',
        'Sequencing technology',
        'Assembly method',
        'Coverage',
        'Originating lab',
        'Address',
        'Sample ID given by the sample provider',
        'Submitting lab',
        'Address', 
        'Sample ID given by the submitting laboratory',
        'Authors'
    ])


def write_metadata_to_file(metadata, file='out.csv'):
    '''

    '''
    gisaid_fasta_files = get_consensus_fasta_files()
    with open(file, 'w') as outfile:
        outfile.write(get_column_header() + "\n")
        for file in gisaid_fasta_files:
            for sample in file:
                metadata_string = ','.join()
                outfile.write(create_metadata_dictionary(sample_name=sample, consensus=file[sample]['consensus']) + "\n")


def import_uhtc_metadata(file):
    '''
    A function for reading in a tab seperated text file from
    UHTC and import the data as a dictionary.
    The header for the file is listed as: sample, external_name, date, ct

    Arguments:
        * file: a tab seperated file containing sample name, external name,
                collection date and cycle threshold

    Return Value:
        Returns a dictionary containing samples as the key and the
        collection date as the value.
    '''
    data = {}
    with open(file, 'r') as file_i:
        ct_reader = csv.DictReader(file_i, delimiter='\t')
        for line in ct_reader:
            data[line['sample']] = {'collection_date' : line['date'], 'ct' : line['ct']}
    return data


def import_sample_include_list(file):
    '''
    Read a list of samples and import them into an array for use.
    '''
    sample_include = []
    with open(file, 'r') as file_i:
        for line in file_i:
            sample_include.append(line.rstrip())
    return sample_include


def import_sample_exclude_list(file):
    '''
    Read a list of samples and import them as a sample removal step.
    '''
    sample_exclude = []
    with open(file, 'r') as file_i:
        for line in file_i:
            sample_exclude.append(line.rstrip())
    return sample_exclude


def get_coverage_dictionary(file):
    '''
    Get the coverage dictionary.
    '''
    qc_data = {}
    with open(file, 'r') as file_i:
        qc_reader = csv.DictReader(file_i, delimiter='\t')
        for line in qc_reader:
            qc_data[line['sample']] = {'mean_depth' : line['mean_sequencing_depth']}
    return qc_data
