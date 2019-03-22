import pandas as pd
import numpy as np

def taxon_sample(df, group_rank):
    df = pd.read_csv(df)
    grouped = df.dropna(axis=0, subset=[group_rank])
    grouped.apply(lambda x: x.sample(n=1))
    grouped = grouped.drop_duplicates(subset=[group_rank], keep='first')    
    return(grouped)

def taxa_file(group_rank, name_column, min_column, max_column, new_taxon_column_name, new_age_column):
    grouped = taxon_sample('Data/higher_taxa.csv', group_rank)
    new_group = grouped[[name_column, min_column, max_column]]
    tip_age = grouped[[name_column, max_column]]
    tip_age.columns = [new_taxon_column_name, new_age_column]
    return(tip_age)
    
def final_ages(final_df):
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
    morph_slim = morph_temp.drop(['Fossil', 'min_yr', 'max_yr'], axis=1)
    morph_slim = morph_slim[morph_slim.age != 0.00]
    stacked = pd.concat([sample, morph_slim])
    return(stacked)
    
if __name__ == '__main__':
    tax_file = taxa_file('SubFamily', 'SpecimenName', 'min_yr', 'max_yr', 'taxon', 'age')
    tax_file.to_csv("Data/taxa_sample.tsv", sep='\t', index =False)
    final_tip_age = final_ages("Data/final_tip_ages.tsv")
    final_tip_age.to_csv("Data/ final_tip_age.tsv", sep = '\t', index=False)
    stacked = foss_int()
    stacked.to_csv("Data/foss_int.tsv", sep='\t', index =False)

