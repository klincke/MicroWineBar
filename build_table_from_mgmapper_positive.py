#!/usr/bin/env python3.6

#python build_table_from_mgmapper_positive.py bobal2012_0  --suffix .tab

import sys
import os
import glob
import pandas as pd
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('sample', action='store', help='name of the MGmapper directory')
parser.add_argument('--MGmapper_dir', action='store', default='./', help='directory where the MGmapper output directory is placed for')
parser.add_argument('--suffix', action='store', default='_microwine.tsv', help='suffix for the output file, the default is "_microwine.tsv"')
args = parser.parse_args()


sample= args.sample
path=args.MGmapper_dir
suffix=args.suffix

num_of_positive_files = 0
columns_to_use = ['R_Abundance (%)', 'Reads','superfamily', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'speciesTax']
sample_df = pd.DataFrame()
print(path)
print(sample)
for filename in glob.glob(os.path.join(path, sample + '*', 'stat/positive.species.*')):
    df = pd.read_table(filename, header=0, index_col=None, usecols=columns_to_use, dtype={'R_Abundance (%)':np.float64, 'Reads':np.int64})
    df.set_index(df.columns[-1], drop=False, inplace=True)
    df = pd.concat([sample_df,df], sort=True).reset_index(drop=True)
    df = df.groupby(['speciesTax', 'species','genus','family','order','class','phylum','superfamily']).sum()
    sample_df = pd.DataFrame(df.to_records())
    sample_df.set_index(['speciesTax'], drop=False, inplace=True)
    myindex = list(sample_df.index)
    newindex = sorted(set([i for i in myindex if myindex.count(i)>1]))
    for idx in newindex:
        newabundance = sum(list(sample_df.loc[idx,'R_Abundance (%)']))
        newrow = sample_df.loc[idx]
        newrow = newrow.iloc[0]
        newrow['R_Abundance (%)'] = newabundance
        sample_df.drop([idx, idx], inplace=True)
        sample_df = sample_df.append(newrow)
        num_of_positive_files += 1
try:
    sample_df = sample_df[columns_to_use[:-1]]
    sample_df = sample_df[sample_df['R_Abundance (%)'] >= 0.001]
    sample_df.to_csv(sample + suffix, sep='\t', header=True, index=False)
except KeyError:
    pass

try:
    if num_of_positive_files == 0:
        raise IOError('no files found')
except IOError as exp:
    print("Error", exp)