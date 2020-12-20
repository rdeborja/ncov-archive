"""
Test suite for the gisaid module
"""

import ncov.archive.gisaid as gs

def test_create_fasta_header():
    """
    Determine whether the FASTA header matches expected. 
    """
    expected_header = '>testvirus/Canada/sample/2020'
    _header = gs.create_fasta_header(virus='testvirus',
                                     sample_id='sample',
                                     country='Canada',
                                     year='2020')
    assert _header == expected_header


def test_create_fasta_record():
    """
    Test the create_fasta_record method
    """
    _exp_fasta = list()
    _exp_fasta.append('>testvirus/Canada/sample/2020')
    _exp_fasta.append('ACCTGAGATGACCAGAGTGACGAGATAAGACCCTGACGA')
    _fasta_file = 'data/sample.fa'
    _header = gs.create_fasta_header(virus='testvirus',
                                     sample_id='sample',
                                     country='Canada',
                                     year='2020')
    _fasta_record = gs.create_fasta_record(fasta=_fasta_file, header=_header)
    assert _exp_fasta == _fasta_record


def test_get_consensus_fasta_files():
    """
    Test whether the get_consensus_fasta_files method collects the correct FASTA
    files.
    """
    _exp_sampleA = {'consensus' : 'data/sampleA.consensus.fasta',
                    'fasta_header' : '>hCoV-19/Canada/ON-sampleA/2020'}
    _fasta_dict = gs.get_consensus_fasta_files(path='data')
    assert _fasta_dict[0]['sampleA'] == _exp_sampleA


def test_get_sample_name_from_fasta():
    """
    Test the extraction of the sample name from the FASTA file.
    """
    _exp_sample_name = 'sampleA'
    _fasta_file = 'data/sample.fa'
    assert gs.get_sample_name_from_fasta(file='sample.fa', pattern=['.fa'])
