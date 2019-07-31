# MicroWineBar

version 1.1

Available from: https://github.com/klincke/MicroWineBar

Author: Franziska Klincke

Mail: franziska.klincke@bio.ku.dk

MicroWineBar is a graphical tool for analysing metagenomic sequencing samples.

Copyright (c) 2019 Franziska Klincke


## Installation

MicroWineBar only works on **MacOS** and **Linux**. It uses the Python package scikit-bio which is currently not supported for Windows.

#### Python

prerequisites:	Python >=3.6

recommended is anaconda:     
    download [anaconda](https://www.anaconda.com/distribution/#download-section) and install as described there   
or miniconda:   
	download [miniconda](https://docs.conda.io/en/latest/miniconda.html) and install as described there  
but one can also use another Python installation

##### Python virtual environment
It is also recommended to set up a Python environment. I experienced problems with matplotlib version 3.1.x.   
If you are using anaconda, virtualenv is already installed, otherwise you need to run `pip install virtualenv` to install it. To set up a Python environment open a terminal and type `virtualenv NAMEOFYOURTESTENV` and change NAMEOFYOURTESTENV to your preferred name of the environment.   
To activate your python environment type `source NAMEOFYOURTESTENV/bin/activate`.   
Inside you environment you can install and run MicroWineBar. Afterwards deactivate the environment by typing `deactivate`.

#### Install MicroWineBar
Note: Remember to activate you Python environment if you use one.
Open a terminal and simply type
	`pip install microwinebar`

This will install all required python packages automatically. However, if this is not the case one can also manually install them:
additinal Python packages:
* Pmw: open a terminal and type `pip install Pmw`
* wikipedia: open a terminal and type `pip install wikipedia`
* scikit-bio: open a terminal and type `pip install scikit-bio`
* scikit-learn: open a terminal and type `pip install scikit-learn`
* numpy: open a terminal and type `pip install numpy`
* pandas: open a terminal and type `pip install pandas`

Note: Remember to deactivate you Python environment if you use one.

## Usage
Note: Remember to activate you Python environment if you use one.
Open a terminal and type `microwinebar` to start MicroWineBar.  
Note: Remember to deactivate you Python environment if you use one.

## Input formats

[](Tab delimited files from programs that estimate abundances of microbial organisms from metagenomics samples such as MGmapper, Kraken or MetaPhlAn. These files contain absolute (and relative) [](abundances with taxonomic annotations.)
MicroWineBar was designed for species abundance tables from shotgun metagenomics data but it can also be used for other types of hierarchical data. The tab-delimietd files contain absolute (and relative) abundances with taxonomic annotations.

[//]: test

[^Comment]:  Text

<!-- MGmapper, Kraken or MetaPhlAn -->


#### Prepare Input
Scripts for preparing input are provided:
* build_table_from_bracken.py   
  Takes [Bracken](https://ccb.jhu.edu/software/bracken/index.shtml) output and adds NCBI taxonomy for all levels. To run it one also needs to install the Environment for Tree Exploration by typing `pip install ete3`
* build_table_from_mgmapper_positive.py   
  Takes [MGmapper](https://bitbucket.org/genomicepidemiology/mgmapper/src/master/) output and combines the output from several databases into one table


## Example

In the directory ExampleData one can find the first samples of the wine dataset from fermentations of Bobal grapes. These files were created with MGmapper and the running the script build_table_from_mgmapper_positive.py.
To analyse these files one has to start MicroWineBar and in the **file**-menu choose **MGmapper files** which opens a file dialog to open the files.
Then one should filter the non-microorganisms by clicking on the **overview**-menu and then choose **filter**. This opens a table with all species present in the samples. To sort the rows (species) by one column one has to click on the header, e.g. click in Phylum to sort by phylum name. To hide all species belonging to the phylum Streptophyta one has to right click in the column Phylum in a row where hide is False. Then a popup menu will appear where one has to click on **hide/show**. If  in the row hide is False all Streptohyta will be displayed, if one right clicks on Streptophyta and in the popup menu chooses **hide/show**.

To compare two groups of samples choose **compare two groups of samples** in the **overview**-menu choose.

Select the samples belonging to the first group in the left listbox, e.g. all samples from 2012 and change the name of the group from 'group1' to '2012'. Do the same for the second group of samples.
To run the differential abundance analysis one has to click on **ANCOM**. Then a file dialog will open in case one wants to save the results as a .csv file. The results are also displayed in MicroWineBar.
To get a PCA plot one has to click on **PCA**.
To obtain a boxplot of the species richness and Shannon diversity one has to click in **richness** and **Shannon diversity** respectively. There is also the option to get these plots for all samples instead of the two groups. For this one has to click in the **overview**-menu on **richness** or **Shannon diversity** respectively.
