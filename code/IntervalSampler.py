    
if __name__ == '__main__':

    import pandas as pd
    from numpy import random
    import argparse 

    parser = argparse.ArgumentParser()
    parser.add_argument("--df", help = "TSV Containing data for sample taxa")
    parser.add_argument("--morph", help = "TSV Containing data for morph characters")
    parser.add_argument("--mol", help = "TSV Containing data for mol characters")
    parser.add_argument("--group_rank", help = "rank")
    parser.add_argument("--outfile", help = "The file path you wish to write the data to")
    args = parser.parse_args()
    #if args.sample:
        #tip_age = sample
    if args.morph:
        morph_temp = args.morph
    if args.mol:
        mol_temp = args.mol
    if args.group_rank:
        group_rank = args.group_rank
    if args.df:
        df = args.df

    #morph_temp = pd.read_csv("./Data/taxa_template.tsv", sep='\t')
    #mol_temp = pd.read_csv("./Data/Mol/mol_df.tsv", sep='\t')
    
    #morph_temp = pd.read_csv(morph_temp, sep='\t')
    #mol_temp = pd.read_csv(mol_temp, sep='\t')


def taxon_sample(df, group_rank):
    df = pd.read_csv(df)
    df = df.dropna(axis=0)
    samp = df.groupby(group_rank).apply(lambda x :x.iloc[random.choice(range(0,len(x)))])
    return(samp)

def final_ages(tax_samp):
    morph_temp = (morph_temp)
    mol_temp = (mol_temp)
    morph_temp = morph_temp[['taxon', 'age']]
    tax_samp = tax_samp[['SpecimenName', 'max_yr']]
    tax_samp.columns = ['taxon', 'age']
    stacked = pd.concat([morph_temp, mol_temp, tax_samp])
    final_tip_age = stacked.drop_duplicates('taxon')
    return(final_tip_age)
        
def foss_int(tax_samp):
    #morph_temp = pd.read_csv("Data/taxa_template.tsv", sep='\t')
    morph_slim = morph_temp[['taxon', 'min_yr', 'max_yr']]
    tax_samp = taxon_sample(df, group_rank)
    tax_samp = tax_samp[['SpecimenName', 'min_yr', 'max_yr']]
    tax_samp.columns = ['taxon', 'min_yr', 'max_yr']
    morph_slim = morph_slim[morph_slim.min_yr != 0.00]
    stacked = pd.concat([tax_samp, morph_slim])
    final_tip_age = final_ages(tax_samp)
    final_tip_age.to_csv("../Data/accessory/final_tip_age.tsv", sep = '\t', index=False)
    stacked = foss_int(tax_samp)
    stacked.to_csv(".../Data/accessory/foss_int.tsv", sep='\t', index =False)
    return(stacked)

