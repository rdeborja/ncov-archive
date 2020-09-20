# ncov-archive

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

As part of our efforts with nCoV data analysis, uploading data to public
repositories is key.  This package provides Python modules for archiving
and uploading data public data repositories.  Currently GISAID is the only
supported repository platform.


## Installation
```
git clone git@github.com:rdeborja/ncov-archive.git
cd ncov-archive
pip install .
```


## Usage
### Configuration files
`ncov-archive` requires a configuration file containing institute level
information.  The configuration file, in YAML format, would include the
following:
```
---
submitter: "<username of registered GISAID submitter>"
type: "betacoronavirus"
location: "North America / Canada / Ontario"
host: "Human"
platform: "<sequencing platform used>"
assembly_method: "<assembly method used to construct consensus FASTA files>"
originating_lab: "<name of institute where samples originated from>"
originating_lab_address: "<full address for original lab>"
submitting_lab: "<name of insititute submitting data>"
submitting_lab_address: "<full address of institute submitting data>"
authors: "<comma seperated list of authors>"
```

### Top Level Scripts
A top level script exists that will parse output files from the provided path
and aggregate metadata and contruct bulk upload files required according to
GISAIDs guidelines: `create_gisaid_files.py`

The usage is as follows:
```
usage: create_gisaid_files.py [-h] [-o OUTPUT] [-p PATH] [-m META] [-q QC]
                              [-f FASTA] [-i INCLUDE] [-c CONFIG]

Create required GISAID files

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        filename to write metadata to
  -p PATH, --path PATH  path to search
  -m META, --meta META  meta file
  -q QC, --qc QC        the summary QC file
  -f FASTA, --fasta FASTA
                        filename of output fasta
  -i INCLUDE, --include INCLUDE
                        a list of samples to be included
  -c CONFIG, --config CONFIG
                        YAML file containing GISAID run config
```
Note that the `--meta` argument requires the same metadata file format generated
for `ncov-tools` and the `--qc` argument is generated from the output of
`ncov-tools` using the `get_qc.py` script or the `all_qc_reports` rule from the
snakemake file.  The `--include` argument requires a file containing a list with
each row consisting of sample names.  This is an optional argument and if not
included returns all samples with a FASTA file and corresponding entry in the
metadata.


## Credit and Acknowledgement
This package was developed in conjunction with `ncov-tools` and utilizes both
output files and configuration files from this package.


## License
MIT

