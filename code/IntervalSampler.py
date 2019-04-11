#########################################
#python IntervalSampler.py --df "../Data/higher_taxa.csv" --group_rank "SubFamily" --s_of "../Data/stacked_data_2.csv"
#########################################



import pandas as pd
from numpy import random
import argparse 
import dendropy

def taxon_sample(df, group_rank):
    group_rank = group_rank
    df = pd.read_csv(df)
    df = df.dropna(axis=0)
    tax_samp = df.groupby(group_rank).apply(lambda x :x.iloc[random.choice(range(0,len(x)))])
    return(tax_samp)

def final_ages(tax_samp):
    #morph_temp = dendropy.StandardCharacterMatrix.get(path=morph_temp, schema="nexus")
    #mol_temp = dendropy.StandardCharacterMatrix.get(path=mol_temp, schema="nexus")
    #tax_samp = tax_samp[['taxon', 'age']]
    tax_samp = tax_samp[['SpecimenName', 'max_yr']]
    tax_samp.columns = ['taxon', 'age']
    #stacked = pd.concat([morph_temp, mol_temp, tax_samp])
    final_tip_age = tax_samp.drop_duplicates('taxon')
    return(final_tip_age)
        
def foss_int(tax_samp, final_tip_age):
    #morph_temp = pd.read_csv(morph_temp, sep='\t')
    morph_slim = final_tip_age[['taxon', 'age']]
    #tax_samp = tax_samp[['SpecimenName', 'min_yr', 'max_yr']]
    #tax_samp.columns = ['taxon', 'min_yr', 'max_yr']
    morph_slim = morph_slim[morph_slim.age != 0.00]
    stacked = pd.concat([final_tip_age, morph_slim])
    return(stacked)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--df", help = "TSV Containing data for sample taxa")
    #parser.add_argument("--morph", help = "TSV Containing data for morph characters")
    #parser.add_argument("--mol", help = "TSV Containing data for mol characters")
    parser.add_argument("--group_rank", help = "rank")
    parser.add_argument("--outfile", help = "The file path you wish to write the data to")
    parser.add_argument("--fta_of", help = "The file path you wish to write the final_tip_age data to")
    parser.add_argument("--s_of", help = "The file path you wish to write the stacked data to")

    args = parser.parse_args()

    #if args.morph:
      #  morph_temp = args.morph
    #if args.mol:
     #   mol_temp = args.mol
    if args.group_rank:
        group_rank = args.group_rank
    if args.df:
        df = args.df
    if args.fta_of:
        final_tip_age_of = args.fta_of
    if args.s_of:
        stacked_of = args.s_of

    tax_samp = taxon_sample(df, group_rank)
    final_tip_age = final_ages(tax_samp)
    final_tip_age.to_csv(args.fta_of, sep = '\t', index=False)
    stacked = foss_int(tax_samp, final_tip_age)
    stacked.to_csv(stacked_of, sep='\t', index =False)
    

    #df = pd.read_csv(df_i, header=None, sep='\t')
    #group_rank = group_rank_i
    #morph_temp = pd.read_csv(morph_temp_df, sep='\t')
    #mol_temp = pd.read_csv(mol_temp_df, sep='\t')
    #stacked_of = s_of
    #final_tip_age_of = fta_of

    #samp = taxon_sample(df, group_rank)
    #final_tip_age = final_ages(mol_temp, morph_temp)
    #stacked = fossil_int(tax_samp)
    print("welp.")
    #final_tip_age.to_csv(fta_of, sep = '\t', index=False)
    #"Data/accessory/final_tip_age.tsv"
    #stacked = foss_int(tax_samp)
    #stacked.to_csv(s_of, sep='\t', index =False)
    #"Data/accessory/foss_int.tsv"

    #morph_temp = pd.read_csv("./Data/taxa_template.tsv", sep='\t')
    #mol_temp = pd.read_csv("./Data/Mol/mol_df.tsv", sep='\t')
    
    #morph_temp = pd.read_csv(morph_temp, sep='\t')
    #mol_temp = pd.read_csv(mol_temp, sep='\t')