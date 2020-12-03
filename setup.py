'''
Setup.py file for the ncov-archive package.
'''
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ncov-archive",
    version="0.3.1",
    author="Richard J. de Borja",
    author_email="richard.deborja@oicr.on.ca",
    description="A nCoV package for archiving files to publice repos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rdeborja/ncov-archive",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=['bin/create_gisaid_files.py']
)
