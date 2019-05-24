# Creates 2 files
# First file is oldest_fossil_int.tsv -- this file contains oldest specimens from each rank with a min and max
# Second file is oldest_sample.tsv -- this file contains oldest specimens from each rank and max

import pandas as pd
import numpy as np
from numpy import random
import argparse

def taxon_sample(df, group_rank, min_column, max_column, name_column):
    df = pd.read_csv(df)
    df = df.dropna(axis=0)
    samp = df.groupby([group_rank]).max()[[min_column, max_column, name_column]]
    samp = samp.reset_index()
    return(samp)

def taxa_file(group_rank, name_column, min_column, max_column, new_taxon_column_name):
    grouped = taxon_sample(df, group_rank, min_column, max_column, name_column)
    new_group = grouped[[name_column, min_column, max_column]]
    fossil_int = new_group[[name_column, min_column, max_column]]
    fossil_int.columns = [new_taxon_column_name, min_column, max_column]
    fossil_int.to_csv(int_outpath, sep='\t', index=False)
    return(fossil_int)

def taxa_age(int_outpath, new_taxon_column_name, max_column, new_age_column):
    tip_age = pd.read_csv(int_outpath, sep='\t')
    tip_age = tip_age[[new_taxon_column_name, max_column]]
    tip_age.columns = [new_taxon_column_name, new_age_column]
    tip_age.to_csv(samp_outpath, sep='\t', index =False)
    return(tip_age)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--df", help = "Datafile of taxa information requiring rank, max age, min age, ")
    parser.add_argument("--group_rank", help = "rank that will be groupedby and used for sampling 1 specimen from each rank")
    parser.add_argument("--int_outpath", help = "oldest_fossil_int.tsv outpath")
    parser.add_argument("--samp_outpath", help = "oldest_sample.tsv outpath")
    args = parser.parse_args()
    if args.df:
        df = args.df
    if args.group_rank:
        group_rank = args.group_rank
    if args.int_outpath:
        int_outpath = args.int_outpath
    if args.samp_outpath:
        samp_outpath = args.samp_outpath

taxon_sample(df, group_rank,'max_yr', 'min_yr','SpecimenName')
taxa_file(group_rank, 'SpecimenName', 'min_yr', 'max_yr', 'taxon')
taxa_age(int_outpath, 'taxon', 'max_yr', 'age')