"""
Helper class for UHTC
"""

import os
import sys
import pandas as pd


def import_metadata(file, sheet_name, usecols=cols, skiprows=0):
    df = pd.read_excel(file, sheet_name=sheet_name, usecols=cols, skiprows=skiprows)
    return df


class Uhtc():
    def __init__(self, dir):
        self.dir = dir

