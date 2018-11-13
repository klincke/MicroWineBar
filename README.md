# MicroWineBar

version 1.1

Available from: https://github.com/klincke/MicroWineBar

Author: Franziska Klincke

Mail: klincke@bioinformatics.dtu.dk

MicroWineBar is a graphical tool for analysing metagenomic sequencing samples. 
MicorWineBar has to be installed locally.

Copyright (c) 2018 Franziska Klincke


## Installation

prerequisites:	Python 3.6

recommended is anaconda    
    download from https://www.continuum.io/downloads and install as described there

additinal Python packages:
* Pmw     
	open a terminal and type
    	`pip install Pmw`
* wikipedia   
    open a terminal and type
        `pip install wikipedia`
* scikit-bio
    open a terminal and type
        `pip install scikit-bio`
* rpy2
    open a terminal and type
    	`pip install rpy2`


## Usage

open terminal and move into the MicroWineBar directory and type `python microwinebar.py` or `./microwinebar.py`
, in case of several python versions one can also try `python3 microwinebar.py`


## Input formats

Tab delimited files from programs that estimate abundances of microbial organisms from metagenomics samples such as MGmapper, Kraken or MetaPhlAn. These files contain absolute (and relative) abundances with taxonomic annotations. 


## Using other Python versions than anaconda

It is possible to use other Python versions but then one needs to install additional packages:
* openpyxl
* numpy
* pandas
* scipy
* scikit-learn


## Example

