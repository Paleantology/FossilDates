import pandas as pd
import dendropy
import os
import sys

estimated_tree = dendropy.Tree.get_from_path(sys.argv[1], schema = "newick", preserve_underscores = True, rooting='force-unrooted')
barden_tree = dendropy.Tree.get_from_path(sys.argv[2], schema = "nexus", preserve_underscores = True, taxon_namespace = estimated_tree.taxon_namespace, rooting='force-unrooted')

est_label = []

for tax in barden_tree.taxon_namespace:
    est_label.append(tax.label)

shared_labs = []

for lab in estimated_tree.taxon_namespace:
    if lab.label in est_label:
        shared_labs.append(lab.label)

unshared = []

for lab in estimated_tree.taxon_namespace:
    if lab.label not in shared_labs:
        unshared.append(lab.label)

pruned = estimated_tree.extract_tree_without_taxa_labels(unshared)

print(pruned.symmetric_difference(barden_tree))

