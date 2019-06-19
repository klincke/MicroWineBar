#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
#converts Bracken output into format which can be read by microwinebar
#gets the NCBI taxonomy

#Franziska Klincke
import os, sys
import argparse
import pandas as pd
from ete3 import NCBITaxa

parser = argparse.ArgumentParser(description='')
parser.add_argument('--input_file', type=str,help='')
parser.add_argument('--input_list', type=str,help='')

args = parser.parse_args()



def get_taxonomy(taxlevels, ncbi, taxid, t_level, name, taxlevels_dict):
    lineage = ncbi.get_lineage(taxid)
    names = ncbi.get_taxid_translator(lineage)
    lineage2ranks = ncbi.get_rank(names)
    new_taxoxnomy_dict = dict()
    for k in lineage2ranks:
        if lineage2ranks[k] in taxlevels:
            new_taxoxnomy_dict[lineage2ranks[k]] = names[k]
    new_taxonomy_list = []
    for k in taxlevels:
        try:
            new_taxonomy_list.append(new_taxoxnomy_dict[k])
        except KeyError:
            if k == taxlevels_dict[t_level]:
                new_taxonomy_list.append(name)
            else:
                new_taxonomy_list.append('-')
    return new_taxonomy_list
    

def convert_file_format(taxlevels, ncbi, ncbi_taxonomy_dict, taxlevels_dict, filename):
    in_df = pd.read_csv(filename, header=0, sep='\t')
    df = pd.DataFrame(columns = ['R_Abundance (%)', 'Reads'] + taxlevels)
    for idx in in_df.index:
        taxid = in_df.loc[idx,'taxonomy_id']
        abund = [str(item) for item in in_df.loc[idx,['fraction_total_reads', 'new_est_reads']].tolist()]
        t_level = in_df.loc[idx,'taxonomy_lvl']
        name = in_df.loc[idx,'name']
        if taxid not in ncbi_taxonomy_dict:
            ncbi_taxonomy_dict[taxid] = get_taxonomy(taxlevels, ncbi, taxid, t_level, name, taxlevels_dict)
        df = df.append(pd.DataFrame(columns=df.columns,data=[abund + ncbi_taxonomy_dict[taxid]]), ignore_index=True)
    return df

def save_dataframe(df, new_filename):
    df.to_csv(new_filename, sep='\t', index=False)

ncbi = NCBITaxa()
ncbi_taxonomy_dict = dict()

#taxlevels = ['species', 'genus', 'family', 'order', 'class', 'phylum', 'superkingdom']
taxlevels = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
taxlevels_dict = {'D':'superkingdom', 'P':'phylum', 'C':'class', 'O':'order', 'F':'family' ,'G':'genus' ,'S':'species'}


if args.input_file: 
    filename = args.input_file
    df = convert_file_format(taxlevels, ncbi, ncbi_taxonomy_dict, taxlevels_dict, filename)
    save_dataframe(df, '.'.join(filename.split('.')[:-1])+'_mwb.tab')
elif args.input_list:
    with open (args.input_list, 'r') as infile:
        for filename in infile:
            df = convert_file_format(taxlevels, ncbi, ncbi_taxonomy_dict, taxlevels_dict, filename.strip())
            save_dataframe(df, '.'.join(filename.split('.')[:-1])+'_mwb.tab')
    
