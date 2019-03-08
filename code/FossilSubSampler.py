import dendropy
import pandas as pd
from sys import argv
import argparse
from random import randint

def pull_data_taxon(fossil_df, tax_unit_outfile, **kwargs):
	'''Pull the oldest fossil in a group. Mandatory: what level (i.e., subfamily, tribe, etc).'''
	foss_list = []
	for key, value in kwargs.items():
		try:
		  kwargs["level"]
		except KeyError:
		  raise KeyError('level is required is a Required Argument that tells the program from which taxonomic group to sample. Options 						include subfamily,tribe,genus')  
		try:
		  kwargs["age"]
		except KeyError:
		  raise KeyError('age is required is a Required Argument that specifies how to sample within a taxonomic group. Options include 						oldest, youngest, random')		  
		if key == "level":
			group_key = value.lower()
		if key == "age":
			age_key = value.lower()
			if age_key == "oldest":
				if "fraction" in kwargs.keys():
					num_key = kwargs["fraction"]
					oldest_df = fossil_df.groupby(group_key).apply(lambda x: x.nlargest(round(len(x)*float(num_key)), 'max_ma'))[["taxon","max_ma", group_key]]
					oldest_df = oldest_df.drop_duplicates()
					oldest_df.to_csv(tax_unit_outfile, sep="\t", index=False)
					oldest_df = oldest_df.drop(group_key, axis=1) 
					oldest_df[["taxon","age"]] = oldest_df[["taxon","max_ma"]]
					sample_df = oldest_df.drop("max_ma", axis=1) 
				else:
					oldest_df = fossil_df.groupby([group_key]).max()[["max_ma", "taxon"]]
					oldest_df = oldest_df.reset_index()
					oldest_df = oldest_df.drop_duplicates()
					oldest_df.to_csv(tax_unit_outfile, sep="\t", index=False)
					oldest_df = oldest_df.drop(group_key, axis=1) 
					oldest_df[["taxon","age"]] = oldest_df[["taxon","max_ma"]]
					sample_df = oldest_df.drop("max_ma", axis=1) 

			elif age_key == "youngest":
				if "fraction" in kwargs.keys():
					num_key = kwargs["fraction"]
					oldest_df = fossil_df.groupby(group_key).apply(lambda x: x.nsmallest(round(len(x)*float(num_key)), 'max_ma'))[["taxon","max_ma", group_key]]
					oldest_df.to_csv(tax_unit_outfile, sep="\t", index=False)
					oldest_df = oldest_df.drop(group_key, axis=1, sort=True) 
					oldest_df = oldest_df.drop_duplicates()
					oldest_df[["taxon","age"]] = oldest_df[["taxon","max_ma"]]
					sample_df = oldest_df.drop("max_ma", axis=1) 
				else:
					oldest_df = fossil_df.groupby([group_key]).min()[["max_ma", "taxon"]]
					oldest_df = oldest_df.reset_index()
					oldest_df = oldest_df.drop_duplicates()
					oldest_df.to_csv(tax_unit_outfile, sep="\t", index=False)
					oldest_df = oldest_df.drop(group_key, axis=1) 
					oldest_df[["taxon","age"]] = oldest_df[["taxon","max_ma"]]
					sample_df = oldest_df.drop("max_ma", axis=1) 
			elif age_key == "random":					
				if "fraction" in kwargs.keys():
					num_key = kwargs["fraction"]
					oldest_df = fossil_df.groupby(group_key).apply(lambda x: x.sample(frac=float(num_key)))[["taxon","max_ma", group_key]]
					oldest_df = oldest_df.drop_duplicates()
					oldest_df.to_csv(tax_unit_outfile, sep="\t", index=False)
					oldest_df = oldest_df.drop(group_key, axis=1) 
					oldest_df[["taxon","age"]] = oldest_df[["taxon","max_ma"]]
					sample_df = oldest_df.drop("max_ma", axis=1) 				
				else:
					oldest_df = fossil_df.groupby(group_key).apply(lambda x: x.sample(1))[["max_ma", "taxon"]]
					oldest_df = oldest_df.drop_duplicates()
					oldest_df.to_csv(tax_unit_outfile, sep="\t", index=False)
					oldest_df[["taxon","age"]] = oldest_df[["taxon","max_ma"]]
					sample_df = oldest_df.drop("max_ma", axis=1) 
	return(oldest_df, sample_df)

def pull_data_sampling(fossil_df, tax_unit_outfile, **kwargs):
	'''Pull fossils relative to time. Mandatory keyword: Strategy. Options: uniform (freq=int), time_dep, time stratified. If  time-	stratified, must also provide a list of time bins (with time_bins = list or df)'''
	oldest = float(fossil_df[["max_ma"]].max())
	assert len(kwargs.items()) > 0, "No required args provided. Must provide sampling strategy.	Options: uniform, diversified, time 									stratified."
	for key, value in kwargs.items():
		try:
		  kwargs["strategy"]
		except KeyError:
		  raise KeyError('strategy is a Required Argument that tells the program how to sample fossils through time. Options: uniform, 							time_dep, time stratified. If time-stratified, provide a list of bins.')  
		if "time-stratified" in kwargs.values():
			try:
				kwargs["time_bins"]
			except KeyError:
				raise KeyError('For time-binned sampling, time bins must be specified withe the time_bins kwarg. Input may be a list of 								lists specifying sampling, or a dataframe of time bins') 
		if key == "strategy":
			type_key = value.lower()
		if type_key == "uniform":
			if "freq" in kwargs.keys():
				samp_freq = kwargs["freq"]
			else:
				samp_freq = .1
				print("Uniform sampling indicated, but no sliding window width. Will assume window is 10% of age of oldest fossil")
		if type_key == "time-dep":
			if "multiplier" in kwargs.keys():
				multi = kwargs["multiplier"]
			else:
				print("Time dependent sampling indicated, but no multiplier. Will assume sampling frequency increases 10% each bin 							towards the present")
				samp_freq = 1.1
			if "freq" in kwargs.keys():
				samp_freq = kwargs["freq"]
			else:
				samp_freq = .1
				print("Time dependent sampling indicated, but no sliding window. Will assume window is 10% of age of oldest fossil")
	bin = float(oldest)*samp_freq
	num_bins = round(oldest/bin)
	bottom_interval = oldest - bin
	l = pd.DataFrame()
	
	if type_key == "uniform":

		for x in range(0,num_bins):
			bottom_interval = oldest - (bin*(x+1))
			top_interval = oldest - (bin*x)
			tmp_df = fossil_df[(fossil_df['max_ma'] >= bottom_interval) & (fossil_df['max_ma'] <= top_interval)]
			if len(tmp_df) > 1:
				if "number" in kwargs:
					numb = kwargs["number"]
					if len(tmp_df) >= numb:
						l = l.append(tmp_df.sample(numb))
					else:
						l = l.append(tmp_df.sample(len(tmp_df)))
				else: 
					l = l.append(tmp_df.sample(1)) 
			else:
				pass
			
	if type_key == "time-dep":
		for x in range(0,num_bins):

			bottom_interval = oldest - (bin*(x+1))
			top_interval = oldest - (bin*x)
			tmp_df = fossil_df[(fossil_df['max_ma'] >= bottom_interval) & (fossil_df['max_ma'] <= top_interval)]
			if len(tmp_df) > 1:
				if multi > 1:
					multi = 1
				numb = round(len(tmp_df)*multi)
				l = l.append(tmp_df.sample(numb))
			else:
				pass	  
			multi = multi * (1 + multi)
			
	l = l.drop(['notes', 'reference_no', 'tribe', 'min_ma', 'fossil'], axis=1)
	l[["taxon","age", "subfamily", "genus"]] = l[["taxon","max_ma", "subfamily", "genus"]]
	l.to_csv(tax_unit_outfile, index=False)
	sample_df = l.drop(['subfamily', 'genus','max_ma'], axis=1)
	sample_df.to_csv(sample_outfile, index=False)
	return(l, sample_df)

def make_combined_data(fossil_df, phylo_dat, extant_df, mol_df):
	names_taxon = pd.DataFrame()
	tree_names = phylo_dat.taxon_namespace
	for name in tree_names.labels():
		if name in fossil_df.taxon.values: 
			names_taxon = names_taxon.append(fossil_df[fossil_df['taxon'].str.contains(name)])
		elif name not in fossil_df.taxon.values:
			names_taxon = names_taxon.append(extant_df[extant_df['taxon'].str.contains(name)])
		elif name not in fossil_df.taxon.values or extant_df.taxon.values:
			names_taxon = names_taxon.append(mol_df[mol_df['taxon'].str.contains(name)])
		else:
			names_taxon = names_taxon.append(name)
			print("{} is not contained in any morphology file, added without data".format(name))  
	names_taxon = names_taxon[["taxon", "genus", "subfamily"]]
	return(names_taxon)

def taxa_tsv_file(sample_df, template_tsv, sample_outfile):
	total_tsv = pd.concat([sample_df, template_df])
	total_tsv = total_tsv.drop_duplicates()
	total_tsv.to_csv(sample_outfile, sep = "\t", index=False)
	return(total_tsv)

def make_taxon_set(names_df, rb_file, **kwargs):
	n_l = []
	nl_dict = {}
	lines = []
	new_file_name = rb_file
	assert len(kwargs.items()) > 0, "No required args provided. Must provide taxonomic level to construct taxon sets"
	for key, value in kwargs.items():
		try:
		  kwargs["level"]
		except KeyError:
		  raise KeyError('level is a Required Argument that tells the program how to construct clade contraints')  
	if key == "level":
		group_key = str(value.lower()) 
		n_l = names_df[group_key].unique()
		results = names_df.groupby(group_key)['taxon']
	for name in n_l:
		nl_dict[name] = results.get_group(name).tolist()
	for key, value in nl_dict.items():
		for item in value:
			item = item.strip()
			sentence = key + " = clade(\"" + "\",\"".join(value) + "\")" + "\n"
			lines.append(sentence)
	lines=set(lines)
	tax_list = "constraints=v(" + ",".join(str(x) for x in nl_dict.keys()) + ")"
	try:
		outfile = open(new_file_name,'r+')
	except:
# if file does not exist, create it
		outfile = open(new_file_name,'w')
	with open("code/model_FBDP_template.Rev", "r") as infile:
		for line in infile: 
			if "INSERT1" in line:
				outfile.write(line.replace("INSERT1", "".join(str(x) for x in lines)))
			elif "INSERT2" in line:
				outfile.write(line.replace("INSERT2", tax_list))
			else:
				outfile.write(line)
	outfile.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("--fossil", help="Path to the csv of fossils.")
	parser.add_argument("--mol", required=False, help="Path to the csv of molecular tips.")
	parser.add_argument("--extant", help="Path to TSV or CSV file containing contemporaneous tips, if any exist in your analysis.")
	parser.add_argument("--template", help="Path to TSV of all the names and ages of tips.")
	parser.add_argument("--phylo", help="Path to Nexus-formatted data file of taxa for which morphological data exist.")
	parser.add_argument("--sample", help="How to sample fossils. Options: taxon, time.")
	parser.add_argument("--level", required=False, help="If you will sample fossils clade-biased, from what clade level? Options: Subfamily, tribe, genus")
	parser.add_argument("--age", required=False, help="If you will sample fossils clade-biased, do you want age structure within the clade? Options: oldest, youngest, random.")
	parser.add_argument("--freq", required=False, help="If sampling fossils clade-biased, what percent of the clade do you want to sample? Float value.")
	parser.add_argument("--mult", required=False, help="For diversified sampling, per time-bin multiplier. Float value.")
	parser.add_argument("--sample_out", help="Name of the taxa file for input to revbayes")
	parser.add_argument("--rb_FBDP", help="Where to write the clade-constrained RB_FBDP file")
	args = parser.parse_args()
	if args.fossil:
		fossil_set = args.fossil
	if args.mol:
		mol_set = args.mol
	if args.extant:
		extant = args.extant
	if args.template:
		template = args.template
	if args.phylo:
		phylo_dat = args.phylo
	if args.sample:
		samp_strat = args.sample
	if args.level:
		level = args.level		
	if args.age:
		age = args.age
	if args.freq:
		fraction = args.freq
	if args.mult:
		mult = args.mult
	if args.sample_out:
		tax_unit_outfile = args.sample_out
		sample_outfile = tax_unit_outfile + "_plt"
	if args.rb_FBDP:
		rb_file = args.rb_FBDP
	fossil_df = pd.read_csv(fossil_set)
	extant_df = pd.read_csv(extant)
	template_df = pd.read_csv(template, sep="\t")
	mol_df = pd.read_csv(mol_set)
	phylo_dat = dendropy.StandardCharacterMatrix.get_from_path(phylo_dat, schema="nexus", preserve_underscores=True)
	if samp_strat == "taxon":
		oldest_df, sample_df = pull_data_taxon(fossil_df, tax_unit_outfile, level=level, age=age, fraction=fraction )
		names_df = make_combined_data(fossil_df, phylo_dat, extant_df, mol_df)
		taxa_tsv_file(sample_df, template_df, tax_unit_outfile)
		make_taxon_set(names_df, rb_file, level = level)
	elif samp_strat == "time":
		pull_data_sampling(fossil_df,sample_outfile, tax_unit_outfile, strategy="time-dep", multiplier = mult, freq = freq)
		names_df = make_combined_data(fossil_df, phylo_dat, extant_df, mol_df)
		make_taxon_set(names_df, rb_file, level = level)

