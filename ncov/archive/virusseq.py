"""
Python module for handling VirusSeq data.
"""

from dataclasses import dataclass, field
from pprint import pprint

def get_virusseq_header():
    header = ["specimen collector sample ID",
              "sample collected by",
              "sequence submitted by",
              "sample collection date",
              "sample collection date precision",
              "geo_loc_name (country)",
              "geo_loc_name (state/province/territory)",
              "geo_loc_name (city)",
              "organism",
              "isolate", # same as the FASTA header for the sample
              "purpose of sampling",
              "purpose of sampling details",
              "NML submitted specimen type",
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
              "host age unit",
              "host age bin",
              "host gender",
              "purpose of sequencing",
              "purpose of sequencing details",
              "sequencing date",
              "library ID",
              "sequencing instrument",
              "sequencing protocol name",
              "raw sequence data processing method",
              "dehosting method",
              "consensus sequence software name",
              "consensus sequence software version",
              "breadth of coverage value",
              "depth of coverage value",
              "consensus genome length",
              "Ns per 100 kbp",
              "reference genome accession",
              "bioinformatics protocol",
              "lineage/clade name",
              "lineage/clade analysis software name",
              "lineage/clade analysis software version",
              "variant designation",
              "variant evidence",
              "variant evidence details",
              "study_id"]
    return '\t'.join(header)


@dataclass
class Virusseq():

    @property
    def specimen_collector_sample_id(self):
        pass

    @property
    def sample_collected_by(self):
        pass

    @property
    def sequence_submitted_by(self):
        pass

    @property
    def sample_collection_date(self):
        pass

    @property
    def sample_collection_date_precision(self):
        pass

    @property
    def geo_loc_name_country(self):
        pass

    @property
    def geo_loc_name_state_province_territory(self):
        pass

    @property
    def geo_loc_name_city(self):
        pass

    @property
    def organism(self):
        pass

    @property
    def isolate(self):
        pass

    @property
    def purpose_of_sampling(self):
        pass

    @property
    def purpose_of_sampling_details(self):
        pass

    @property
    def nml_submitted_specimen_type(self):
        pass

    @property
    def anatomical_material(self):
        pass

    @property
    def anatomical_part(self):
        pass

    @property
    def body_product(self):
        pass

    @property
    def environmental_material(self):
        pass

    @property
    def environment_site(self):
        pass

    @property
    def collection_device(self):
        pass

    @property
    def collection_method(self):
        pass

    @property
    def host_scientific_name(self):
        pass

    @property
    def host_disease(self):
        pass

    @property
    def host_age(self):
        pass

    @property
    def host_age_unit(self):
        pass

    @property
    def host_gender(self):
        pass

    @property
    def purpose_of_sequencing(self):
        pass

    @property
    def purpose_of_sequencing_details(self):
        pass

    @property
    def sequencing_date(self):
        pass

    @property
    def library_id(self):
        pass

    @property
    def sequencing_instrument(self):
        pass

    @property
    def sequencing_protocol_name(self):
        pass

    @property
    def raw_sequence_data_processing_method(self):
        pass

    @property
    def dehosting_method(self):
        pass

    @property
    def consensus_sequence_software_name(self):
        pass

    @property
    def consensus_sequencing_software_version(self):
        pass

    @property
    def breadth_of_coverage_value(self):
        pass

    @property
    def depth_of_coverage_value(self):
        pass

    @property
    def consensus_genome_length(self):
        pass

    @property
    def ns_per_10kbp(self):
        pass

    @property
    def reference_genome_accession(self):
        pass

    @property
    def lineage_clade_name(self):
        pass

    @property
    def lineage_clade_analysis_software_name(self):
        pass

    @property
    def lineage_clade_analysis_software_version(self):
        pass

    @property
    def variant_designation(self):
        pass

    @property
    def variant_evidence(self):
        pass

    @property
    def variant_evidence_details(self):
        pass

    @property
    def study_id(self):
        return 'UHTC-ON'
