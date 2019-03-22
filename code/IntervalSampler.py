import pandas as pd
import numpy as np
from numpy import random

def taxon_sample(df, group_rank):
    df = pd.read_csv(df)
    df = df.dropna(axis=0)
    samp = df.groupby(group_rank).apply(lambda x :x.iloc[random.choice(range(0,len(x)))])
    return(samp)

def taxa_file(group_rank, name_column, min_column, max_column, new_taxon_column_name, new_age_column):
    grouped = taxon_sample('Data/higher_taxa.csv', group_rank)
    new_group = grouped[[name_column, min_column, max_column]]
    tip_age = grouped[[name_column, max_column]]
    tip_age.columns = [new_taxon_column_name, new_age_column]
    new_group.columns = ['taxon', 'min_yr', 'max_yr']
    return(new_group)
    
def final_ages():
    morph_temp = pd.read_csv("Data/taxa_template.tsv", sep='\t')
    mol_temp = pd.read_csv("Data/Mol/mol_df.tsv", sep='\t')
    tip_age = pd.read_csv("Data/taxa_sample.tsv", sep='\t')
    morph_temp = morph_temp[['taxon', 'age']]
    stacked = pd.concat([morph_temp, mol_temp, tip_age])
    final_tip_age = stacked.drop_duplicates('taxon')
    return(final_tip_age)
        
def foss_int():
    morph_temp = pd.read_csv("Data/taxa_template.tsv", sep='\t')
    sample = taxa_file('SubFamily', 'SpecimenName', 'min_yr', 'max_yr', 'taxon', 'age')
    morph_slim = morph_temp[['taxon', 'min_yr', 'max_yr']]
    sample = sample[['taxon', 'min_yr', 'max_yr']]
    morph_slim = morph_slim[morph_slim.min_yr != 0.00]
    stacked = pd.concat([sample, morph_slim])
    return(stacked)
    
if __name__ == '__main__':
    tax_file = taxa_file('SubFamily', 'SpecimenName', 'min_yr', 'max_yr', 'taxon', 'age')
    tax_file.to_csv("Data/taxa_sample.tsv", sep='\t', index =False)
    final_tip_age = final_ages()
    final_tip_age.to_csv("Data/accessory/final_tip_age.tsv", sep = '\t', index=False)
    stacked = foss_int()
    stacked.to_csv("Data/accessory/foss_int.tsv", sep='\t', index =False)

