#import packages
import pandas as pd
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
from scipy import stats
import matplotlib.patches as mpatches
from matplotlib import rc
plt.rcParams['font.family'] = 'Helvetica'

#load in files 
bait_prey = pd.read_csv('bait_preys.txt', sep='\t')
all_lung=pd.read_csv('gTEX_alllung.csv')
gtex_subset=pd.read_csv('gTEX_subset.csv')
gnomad_subset=pd.read_csv('gnomad_subset.csv')
gtex_subset_drugs = pd.read_csv('gTEX_subset_drugs.csv')
gnomad_subset_drugs = pd.read_csv('gnomad_subset_drugs.csv')
gnomad_random = pd.read_csv('gnomad_subset_random_5000.csv')


#creating figure GTEX
gtex_subset['label'] = 'Interacting Proteins'
gtex_subset_drugs['label'] = 'Drug Target'

#subset drug list to those that have targets
interacting_proteins = gtex_subset['Description'].to_numpy()
gtex_subset_drugs2 = gtex_subset_drugs[gtex_subset_drugs['Description'].isin(interacting_proteins)].reset_index()
gtex_all_figure = pd.concat([gtex_subset, gtex_subset_drugs2]) ignore_index=True)

#calculate median TPM, Lung/Median TPM
gtex_all_figure['median'] = gtex_all_figure.iloc[:,3:].mean(axis=1) #first three columns contain descriptions
gtex_all_figure['Lung/Median'] = gtex_all_figure['Lung'] / gtex_all_figure['median']

gtex_subset_drugs2['median'] = gtex_subset_drugs2.iloc[:,3:].mean(axis=1)
gtex_subset_drugs2['Lung/Median'] = gtex_subset_drugs2['Lung'] / gtex_subset_drugs['median']

#log10 values
gtex_all_figure['Lung_log'] = np.log10(gtex_all_figure['Lung'])
gtex_subset_drugs2['Lung_log'] = np.log10(gtex_subset_drugs2['Lung'])

gtex_all_figure['Lung_Median_log'] = np.log10(gtex_all_figure['Lung/Median'])
gtex_subset_drugs2['Lung_Median_log'] = np.log10(gtex_subset_drugs2['Lung/Median'])


#GTEX MAIN TEXT FIGURE
plt.figure(figsize=(7, 7))
sns.set(font_scale = 1.5)

ax = sns.scatterplot(gtex_all_figure['Lung_log'], gtex_all_figure['Lung_Median_log'], hue=gtex_all_figure['label'], palette=['lightgrey','red'])

for line in range(0,gtex_subset_drugs2.shape[0]):
    ax.text(gtex_subset_drugs2.Lung_log[line], gtex_subset_drugs2.Lung_Median_log[line], gtex_subset_drugs2.Description[line], size=15, color='black', verticalalignment='center', horizontalalignment='left')

plt.xlabel('Lung Expression: log10(GTeX Median Lung TPM)', size=15)
plt.ylabel('Lung Enrichment: log10(GTeX Median Lung/All Tissue TPM)', size=15)
plt.title('')
plt.axhline(y=0.0, color='darkblue', linestyle='-', linewidth=3, alpha=0.3)
ax.patch.set_facecolor('white')
inter = mpatches.Patch(color='lightgrey', label='Interacting Proteins')
drug = mpatches.Patch(color='red', label='Drug Targets')
plt.legend(handles=[inter, drug], loc='upper right', bbox_to_anchor=(1.05, 1), fontsize=15)
plt.savefig("GTEX_figure.svg")  
 
 


#gnomad supplementary figure
gnomad_subset_drugs['label'] = 'drug'
gnomad_subset['label'] = 'subset'
gnomad_random2['label'] = 'random'

gnomad_subset_random = pd.concat([gnomad_random2, gnomad_subset])
gnomad_subset_random['blank'] = '' #for weird matplotlib formating

#GNOMAD FIGURE
sns.set(font_scale=1.5)
plt.figure(figsize=(15, 15)) 
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)
plt.style.use('seaborn-whitegrid')
sns.violinplot(y=gnomad_subset_random['oe_lof'], x=gnomad_subset_random['test'],hue=gnomad_subset_random['label'], orient='v', split=True, inner=None, palette={"lightgrey", "dodgerblue"}, ax=ax1).set(xlabel='Loss of Function', ylabel='Observed/Expected Score')
sns.violinplot(y=gnomad_subset_random["oe_mis"], x=gnomad_subset_random["test"], hue=gnomad_subset_random["label"], orient='v', split=True, inner=None,  palette={"lightgrey", "dodgerblue"}, ax=ax2).set(xlabel='Missense', ylabel='')
sns.violinplot(y=gnomad_subset_random["oe_syn"], x=gnomad_subset_random["test"], hue=gnomad_subset_random["label"],  orient='v', split=True, inner=None, palette={"lightgrey", "dodgerblue"}, ax=ax3).set(xlabel='Synonymous', ylabel='')
ax1.get_legend().remove()
ax2.get_legend().remove()
ax3.get_legend().remove()
all_genes = mpatches.Patch(color='lightgrey', label='All RefSeq Genes')
inter_prot = mpatches.Patch(color='dodgerblue', label='Interacting Proteins')
plt.legend(handles=[all_genes, inter_protein], fontsize=15, loc='upper right', bbox_to_anchor=(3, 0))
sns.set_style("white")
plt.savefig("gnomad_figure_supplementary.jpg", bbox_inches = "tight", dpi=800)
