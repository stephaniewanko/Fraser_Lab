import pandas as pd
import numpy as np

#import 
gnomad = pd.read_csv('gnomad.v2.1.1.lof_metrics.by_gene.txt', comment='#', sep='\t', header=0)
targets = pd.read_csv('final_targets.txt', header=None)
drugs = pd.read_csv('final_drug.txt', header=None)
refseq = pd.read_csv('refseq.txt', header=None)


targets = genes.rename(columns={0: "Genes"}) 
drugs = genes.rename(columns={0: "Genes"})
refseq = genes.rename(columns={0: "Genes"})

targets_np = targets['Genes'].to_numpy()
drugs_np = drugs['Genes'].to_numpy()
refseq_np = refseq['Genes'].to_numpy()


gnomad_subset_target = gnomad[gnomad['gene'].isin(target_np)]
gnomad_subset_drug = gnomad[gnomad['gene'].isin(drug_np)]
gnomad_subset_refseq = gnomad[gnomad['gene'].isin(refseq_np)]

gnomad_subset_refseq.to_csv('gnomad_subset_refseq.csv', sep=',', index=False)
gnomad_subset_drug.to_csv('gnomad_subset_drug.csv', sep=',', index=False)
gnomad_subset_target.to_csv('gnomad_subset_target.csv', sep=',', index=False)
