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

#read in files
os.chdir('/Users/stephaniewankowicz/Downloads/qfit_paper/201116/')
path=os.getcwd()


all_files = glob.glob(path + "/*_methyl.out")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, sep=',', header=0)
    df['PDB'] = filename[54:58]
    li.append(df)

order_all = pd.concat(li, axis=0, ignore_index=True)
print(len(all_files))

order_all[order_all.s2ang < 0] = 0
order_all[order_all.s2ortho < 0] = 0
order_all[order_all.s2calc < 0] = 0

print(order_all.head())

#MERGE
merged_order_all = merge_apo_holo_df(order_all)
print('merged_order_all')
print(merged_order_all.head())
order_all.to_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/201116/order_all.csv')
merged_order_all.to_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/201116/merged_order_all.csv', index=False)

#All Order Parameters by Residue Type
merged_order_all['s2calc_x'] = merged_order_all['s2calc_x'].clip(lower=0)
merged_order_all['s2calc_y'] = merged_order_all['s2calc_y'].clip(lower=0) 

#SUBSET
merged_order_all_polar = merged_order_all[merged_order_all['resn_x'].isin(['R','N','D','C','Q','E', 'H', 'K', 'S', 'T', 'Y'])]
merged_order_all_nonpolar = merged_order_all[merged_order_all['resn_x'].isin(['V','W','P','F','M','L','I','G','A'])]

#All Order Parameter Distribution Plots
make_dist_plot_AH(merged_order_all['s2calc_x'], merged_order_all['s2calc_y'], 's2calc', 'Number of Residues', 'Bound/Unbound OP (Entire Protein)', '/Users/stephaniewankowicz/Downloads/qfit_paper/OP_all_s2calc')
make_dist_plot_AH(merged_order_all['s2ortho_x'], merged_order_all['s2ortho_y'], 's2ortho', 'Number of Residues', 'Bound/Unbound s2ortho (Entire Protein)', '/Users/stephaniewankowicz/Downloads/qfit_paper/OP_all_s2ortho')
make_dist_plot_AH(merged_order_all['s2ang_x'], merged_order_all['s2ang_y'], 's2ang', 'Number of Residues', 'Bound/Unbound s2ang (Entire Protein)', '/Users/stephaniewankowicz/Downloads/qfit_paper/OP_all_s2ang')

make_boxenplot_AH(merged_order_all['s2calc_x'], merged_order_all['s2calc_y'], 's2calc', 'Number of Residues', 's2calc', '/Users/stephaniewankowicz/Downloads/qfit_paper/OP_calc_boxen')

print('Difference of s2calc between Bound/Unbound [Entire Protein]')
paired_ttest(merged_order_all['s2calc_x'], merged_order_all['s2calc_y'])

print('Difference of s2ang between Bound/Unbound [Entire Protein]')
paired_ttest(merged_order_all['s2ang_x'], merged_order_all['s2ang_y'])

#STATS
print('Difference of s2calc on only Polar Side Chains between Bound/Unbound [Entire Protein]')
paired_ttest(merged_order_all_polar['s2calc_x'], merged_order_all_polar['s2calc_y'])

print('Difference of s2calc on only nonpolar Side Chains between Bound/Unbound [Entire Protein]')
paired_ttest(merged_order_all_nonpolar['s2calc_x'], merged_order_all_nonpolar['s2calc_y'])

print('number of pairs:')
print(len(merged_order_all['Holo'].unique()))

#FIGURE 
fig = plt.figure()
f, axes = plt.subplots(1, 4, sharey=True, sharex=True)

p1 = sns.boxenplot(merged_order_all_polar['s2calc_x'], orient='v', 
ax=axes[0]).set(xlabel='Polar Bound', ylabel='S2calc Order Parameter')
p2 = sns.boxenplot(merged_order_all_polar['s2calc_y'], orient='v', ax=axes[1]).set(xlabel='Polar Unbound', ylabel='')
p3 = sns.boxenplot(merged_order_all_nonpolar['s2calc_x'], orient='v', ax=axes[2]).set(xlabel='NonPolar Bound', ylabel='')
p4 = sns.boxenplot(merged_order_all_nonpolar['s2calc_y'], orient='v', ax=axes[3]).set(xlabel='NonPolar Unbound', ylabel='')
fig.savefig('/Users/stephaniewankowicz/Downloads/qfit_paper/FullProtein_OP_byResidueType.png')

fig = plt.figure()
merged_order_all['Difference'] = merged_order_all['s2calc_x'] - merged_order_all['s2calc_y']
sns.kdeplot(merged_order_all['Difference'], label='Difference', bw=0.02)
fig.savefig('/Users/stephaniewankowicz/Downloads/qfit_paper/difference.png')
