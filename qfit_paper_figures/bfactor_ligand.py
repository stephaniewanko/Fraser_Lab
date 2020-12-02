#packages
import pandas as pd
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import sys
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
from scipy import stats
import matplotlib.patches as mpatches
from figure_functions import *	

#reference files
os.chdir('/Users/stephaniewankowicz/Downloads/qfit/pair_docs/')
pairs = pd.read_csv('ligand_supplementary_table1.txt', sep=' ', header=None)
pairs = pairs.rename(columns={0: "Apo", 1: "Apo_Res", 2: "Holo", 3: "Holo_Res", 5:"Ligand"})
AH_pairs = pairs.drop_duplicates()

AH_key=pd.read_csv('qfit_AH_key_191218.csv')

#read in files

#MERGE
#merged_order_all = merge_apo_holo_df(order_all)


#All Order Parameter Distribution Plots
#make_dist_plot_AH(merged_order_5['s2calc_x'], merged_order_5['s2calc_y'], 's2calc', 'Number of Residues', 'Apo v. Holo s2calc (Within 5A)', 'AH_s2calc_5A')

#STATS
#print('Difference of s2calc on Side Chains with 5 A between Holo/Apo')
#paired_ttest(merged_order_5['s2calc_x'], merged_order_5['s2calc_y'])

#print('Difference of s2calc on Side Chains with 10 A between Holo/Apo')
#paired_ttest(merged_order_10['s2calc_x'], merged_order_10['s2calc_y'])

#SUBSET
os.chdir('/Users/stephaniewankowicz/Downloads/qfit_paper/')
path=os.getcwd()


all_files = glob.glob(path + "/*_5.0_bfactor_subset.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    df['PDB'] = filename[47:51]
    li.append(df)

bfactor_subset = pd.concat(li, axis=0, ignore_index=True)
print(len(all_files))

#Summary
bfactor_sub_summary = pd.DataFrame()
n = 1
for i in bfactor_subset['PDB'].unique():
    #print(i)
    tmp = bfactor_subset[bfactor_subset['PDB'] == i]
    bfactor_sub_summary.loc[n, 'PDB'] = i
    bfactor_sub_summary.loc[n, 'Average_Bfactor'] = tmp['Average_Bfactor'].mean()
    n += 1


#LIGAND B-FACTOR
os.chdir('/Users/stephaniewankowicz/Downloads/qfit_paper/')
path=os.getcwd()

all_files = glob.glob(path + "/*_ligand_B_factors.csv")

li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    df['PDB'] = filename[47:51]
    li.append(df)

bfactor_ligand = pd.concat(li, axis=0, ignore_index=True)
print(len(all_files))

fig = plt.figure()
sns.distplot(bfactor_ligand['Average_Bfactor'], kde=False)
plt.xlabel('Histogram of Average Ligand B-factors')
plt.legend()
plt.ylabel('Number of Structures')
plt.savefig('/Users/stephaniewankowicz/Downloads/qfit_paper/Ligand_BFactor_Dist.png')

bfactor_ligand_merged = bfactor_sub_summary.merge(bfactor_ligand, on='PDB')
bfactor_ligand_merged['ligand_close_bfactors'] = bfactor_ligand_merged['Average_Bfactor_y']/bfactor_ligand_merged['Average_Bfactor_x']

bfactor_ligand_merged_upper = bfactor_ligand_merged[bfactor_ligand_merged['ligand_close_bfactors']>1.4]
bfactor_ligand_merged_lower = bfactor_ligand_merged[bfactor_ligand_merged['ligand_close_bfactors']<0.85]

print(bfactor_ligand_merged.head())
bfactor_ligand_merged.to_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/Bfactor_Ligand_Summary.csv', index=False)
