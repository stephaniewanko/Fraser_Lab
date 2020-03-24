import pandas as pd
import numpy as np

#import GTEX
GTEX = pd.read_csv('GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct', comment='#', sep='\t', header=1, low_memory=False)

#import gene lists
drugs = pd.read_csv('drug_targets.txt', header=None)
genes = pd.read_csv('final_targets.txt', header=None)

#subset gtex for interacting proteins
genes = genes.rename(columns={0: "Genes"})
genes_np = genes['Genes'].to_numpy()
gtex_subset = GTEX[GTEX['Description'].isin(genes_np)]
gtex_subset.to_csv('gtex_interacting_proteins.csv', sep=',', index=False)


#subset gtex for drug targets
drugs = drugs.rename(columns={0: "Genes"})
drugs_np = drugs['Genes'].to_numpy()
gtex_subset = GTEX[GTEX['Description'].isin(drugs_np)]
gtex_subset.to_csv('gtex_drugs_target.csv', sep=',', index=False)

#subset gtex for all lung expression
gtex_all_lung = GTEX[['Description', 'Lung']]
gtex_all_liung.to_csv('gtex_all_lung.csv', sep=',', index=False)
