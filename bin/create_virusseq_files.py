#!/usr/bin/env python

"""
Generate metadata and FASTA files for upload to the VirusSeq data portal.
"""

from ncov.archive.virusseq import *
import os
import sys
import argparse
import yaml
from ncov.archive.common import *
from ncov.archive import *


def init_args():
    description = ''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-c', '--config', required=True,
                        help='config file in YAML format')
    parser.add_argument('-d', '--directory', required=True,
                        help='')
    return parser.parse_args()


def get_config(config):
    """ Import a YAML config file """
    with open(config, 'r') as fh:
        return yaml.load(fh, Loader=yaml.FullLoader)


def main():
    """
    create_virusseq_files.py --directory /.mounts/labs/simpsonlab/projects/ncov/qc/PHO/PHO/illumina/Plate0196_210505 --config config.yaml

    """
    args = init_args()
    config = get_config(config=args.config)
    print(config)


if __name__ == '__main__':
    main()
