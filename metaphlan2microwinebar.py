#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#converts MetaPhlAn output into format which can be read by microwinebar
#Franziska Klincke


import os, sys
import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description="helper script to prepare MetaPhlAn output for MicroWineBar,\neither INPUT_FILE or INPUT_LIST needs to be specified")
parser.add_argument('--input_file', action='store', type=str, nargs='?', help='name of MetaPhlAn output file')
parser.add_argument('--input_list', action='store', type=str, nargs='?', help='name of file containing a list of MetaPhlAn output files')
parser.add_argument('--suffix', action='store', type=str, default='_microwine.tsv', help='suffix for the output file, default: "_microwine.tsv"')

args = parser.parse_args()

if len(sys.argv)==1:    # display help message when no args are passed.
    parser.print_help()
    sys.exit(1)

def convert_file_format(filename, header_dict, taxlevels):
    in_df = pd.read_csv(filename, header=None, sep='\t', names=['taxonomy','rel_abundance'], skiprows=1)
    in2_df = in_df[in_df['taxonomy'].str.contains("s__")]
    in3_df = in2_df[in2_df['taxonomy'].str.contains("t__") == False]
    df = pd.DataFrame(columns=['rel_abundance'] + taxlevels)
    for idx in in3_df.index:
        series = pd.Series(np.array([in3_df.loc[idx,'rel_abundance']]+['-']*len(taxlevels)), index=['rel_abundance']+taxlevels)
        for pair in in_df.loc[idx,'taxonomy'].split('|'):
            key, value = pair.split('__')
            try:
                series[header_dict[key]] = value
            except KeyError:
                pass
        
        df = df.append(series, ignore_index=True)
    return df

def save_dataframe(df, new_filename):
    df.to_csv(new_filename, sep='\t', index=False)


header_dict = {'s':'species', 'g':'genus', 'f':'family', 'o':'order', 'c':'class', 'p':'phylum', 'k':'superfamily'}
taxonomy_keys = ['k', 'p', 'c', 'o', 'f', 'g', 's']
taxlevels = [header_dict[k]for k in taxonomy_keys]


if args.input_file: 
    filename = args.input_file
    df = convert_file_format(filename, header_dict, taxlevels)
    save_dataframe(df, '.'.join(filename.split('.')[:-1])+args.suffix)
elif args.input_list:
    with open (args.input_list, 'r') as infile:
        for filename in infile:
            df = convert_file_format(filename.strip(), header_dict, taxlevels)
            save_dataframe(df, '.'.join(filename.split('.')[:-1])+args.suffix)
    



