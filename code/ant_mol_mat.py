always_present_ants = dendropy.DnaCharacterMatrix.get_from_path("../Data/Mol/satejob10.marker001.18s.aln.nex", 
                                                                     schema = "nexus")


mol_taxa = []
for ant in always_present_ants.taxon_namespace[:]:
    mol_taxa.append([ant.label, 0])
mol_df = pd.DataFrame(mol_taxa, columns=['taxon', 'age'])
mol_df.to_csv("../Data/Mol/mol_df.tsv", sep = "\t", index = False)