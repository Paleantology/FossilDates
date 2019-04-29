# Creates 2 files
# First file is random_fossil_int_(# of sample).tsv -- this file contains random specimens from each rank with a min and max
# Second file is random_sample_(# of sample).tsv -- this file contains radom specimens from each rank and max

import pandas as pd
import numpy as np
from numpy import random
import argparse

def taxon_sample(df, group_rank):
    df = pd.read_csv(df)
    samp = df.groupby(group_rank).apply(lambda x: x.sample(n=1, replace = False, axis=0))
    return(samp)

def taxa_file(group_rank, name_column, min_column, max_column, new_taxon_column_name, new_age_column):
    grouped = taxon_sample(df, group_rank)
    new_group = grouped[[name_column, min_column, max_column]]
    fossil_int = new_group[[name_column, min_column, max_column]]
    fossil_int.columns = [new_taxon_column_name, min_column, max_column]
    fossil_int.to_csv(int_outpath, sep='\t', index=False)
    tip_age = grouped[[name_column, max_column]]
    tip_age.columns = [new_taxon_column_name, new_age_column]
    tip_age.to_csv(samp_outpath, sep='\t', index =False)
    return(tip_age)
    
def get_constraints(samp, group_rank, molecular_data):
    l_ol = []
    working = []
    df = pd.read_csv(molecular_data)
    mol_groups = df.groupby(group_rank, as_index=True)
    for index, row in samp.iterrows():
        for group in mol_groups:
            if index[0] == group[0]:
                l_ol.append([index[0], group[1]['Specimen'].tolist()])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--df", help = "Datafile of taxa information requiring rank, max age, min age, ")
    parser.add_argument("--group_rank", help = "rank that will be groupedby and used for sampling 1 specimen from each rank")
    parser.add_argument("--int_outpath", help = "fossil_int tsv outpath")
    parser.add_argument("--samp_outpath", help = "random_sample tsv outpath")
    parser.add_argument("--molecular_data", help = "molecular data for clade constraints")
    
    args = parser.parse_args()
    if args.df:
        df = args.df
    if args.group_rank:
        group_rank = args.group_rank
    if args.int_outpath:
        int_outpath = args.int_outpath
    if args.samp_outpath:
        samp_outpath = args.samp_outpath
    if args.molecular_data:
        molecular_data = args.molecular_data

    samp = taxon_sample(df, group_rank)
    taxa_file(group_rank, 'SpecimenName', 'min_yr', 'max_yr', 'taxon', 'age')
    get_constraints(samp, group_rank, molecular_data)