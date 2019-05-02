for i in {1..1}
do
python code/random_sampler.py --df Data/accessory/higher_taxa.csv --int_outpath int.tsv --samp_outpath samp.tsv --group_rank subfamily --molecular_data Data/Mol/mol_df.csv
cat int.tsv Data/accessory/interval_template.tsv > $i/intervals.tsv
cat samp.tsv Data/accessory/taxa_template.tsv > $i/taxa.tsv
sed 's/\[//g' clades > clades1
sed 's/]//g' clades1 > clades2
sed "s/'//g" clades2 > $i/clades

cp code/*.Rev $i/
cat  $i/model_FBDP_TEFBD.Rev $i/clades  $i/model_FBDP_TEFBD2.Rev > $i/model_FBDP_TEFBD_final.Rev


done
