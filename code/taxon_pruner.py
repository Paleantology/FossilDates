import pandas as pd
import numpy as np
from numpy import random
import argparse

def pruner(morph1, morph2, mol, outmorph1, outmorph2):
    r = pd.read_csv(morph1, sep="\t")
    b = pd.read_csv(morph2, sep="\t")
    m = pd.read_csv(mol)
    merged1 = pd.merge(r, m, on=['taxon'], how='inner')
    merged1.to_csv(outmorph1, sept='\t')
    merged2 = pd.merge(b, m, on=['taxon'], how='inner')
    merged2.to_csv(outmorph2, sept='\t')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--morph1", help = "TSV Datafile of only taxa names requiring taxon column")
    parser.add_argument("--morph2", help = "TSV Datafile of only taxa names requiring taxon column")
    parser.add_argument("--mol", help = "CSV Datafile of only taxa names requiring taxon column")
    parser.add_argument("--outmorph1", help = "morph1 tsv outpath")
    parser.add_argument("--outmorph2", help = "morph2 tsv outpath")
    args = parser.parse_args()
    if args.morph1:
        morph1 = args.morph1
    if args.morph2:
        morph2 = args.morph2
    if args.mol:
        mol = args.mol
    if args.outmorph1:
        outmorph1 = args.outmorph1
    if args.outmorph2:
        outmorph2 = args.outmorph2

pruner(morph1, morph2, mol, outmorph1, outmorph2)