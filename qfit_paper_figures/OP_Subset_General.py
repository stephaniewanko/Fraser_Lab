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
os.chdir('/Users/stephaniewankowicz/Downloads/qfit_paper/201116/')
path=os.getcwd()

all_files = glob.glob(path + "/*qFit_methyl.out")
li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, sep=',', header=0)
    df['PDB'] = filename[54:58]
    li.append(df)
order_all = pd.concat(li, axis=0, ignore_index=True)


all_files = glob.glob(path + "/*_5.0_order_param_subset.csv")
li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, sep=',', header=0)
    df['PDB'] = filename[54:58]
    li.append(df)
order_5 = pd.concat(li, axis=0, ignore_index=True)


all_files = glob.glob(path + "/*_10.0_order_param_subset.csv")
li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, sep=',', header=0)
    df['PDB'] = filename[54:58]
    li.append(df)
order_10 = pd.concat(li, axis=0, ignore_index=True)

print('order all:')
print(order_all.head())

order_all[order_all.s2ang < 0] = 0
order_all[order_all.s2ortho < 0] = 0
order_all[order_all.s2calc < 0] = 0

order_10[order_10.s2ang < 0] = 0
order_10[order_10.s2ortho < 0] = 0
order_10[order_10.s2calc < 0] = 0

order_5[order_5.s2ang < 0] = 0
order_5[order_5.s2ortho < 0] = 0
order_5[order_5.s2calc < 0] = 0

order_all_tmp = order_all.merge(AH_key, on = ['PDB'])
order_all_apo = order_all_tmp[order_all_tmp['Apo_Holo'] == 'Apo']
order_all_holo = order_all_tmp[order_all_tmp['Apo_Holo'] == 'Holo']

print('order_all_holo')
print(order_all_holo.head())

order_5.to_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/201116/order_5.csv')

order_all_apo.to_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/201116/order_all_apo.csv', index=False)
order_all_holo.to_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/201116/order_all_holo.csv', index=False)

#MERGE
merged_order_all = merge_apo_holo_df(order_all)
merged_order_5 = merge_apo_holo_df(order_5)
merged_order_10 = merge_apo_holo_df(order_10)

merged_order_5.to_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/201116/merged_order_5.csv')

#All Order Parameter Distribution Plots
make_dist_plot_AH(merged_order_5['s2calc_x'], merged_order_5['s2calc_y'], '', 'Number of Residues', 'Bound/Unbound within 5A', '/Users/stephaniewankowicz/Downloads/qfit_paper/AH_s2calc_5A')
make_dist_plot_AH(merged_order_5['s2ortho_x'], merged_order_5['s2ortho_y'], '', 'Number of Residues', 'Bound/Unbound within 5A', '/Users/stephaniewankowicz/Downloads/qfit_paper/AH_s2ortho_5A')

make_dist_plot_AH(merged_order_10['s2calc_x'], merged_order_10['s2calc_y'], '', 'Number of Residues', 'Bound/Unbound within 10A', '/Users/stephaniewankowicz/Downloads/qfit_paper/AH_s2calc_10A')
make_dist_plot_AH(merged_order_10['s2ortho_x'], merged_order_10['s2ortho_y'], '', 'Number of Residues', 'Bound/Unbound within 10A', '/Users/stephaniewankowicz/Downloads/qfit_paper/AH_s2ortho_10A')
make_boxenplot_AH(merged_order_10['s2calc_x'], merged_order_10['s2calc_y'], '', 'Number of Residues', 'Bound/Unbound within 10A', '/Users/stephaniewankowicz/Downloads/qfit_paper/AH_s2calc_10A_boxen')


#merged_order_5.to_csv('merged_order_5.csv')
#STATS
print('Difference of s2calc on Side Chains with 5A between Bound/Unbound')
paired_ttest(merged_order_5['s2calc_x'], merged_order_5['s2calc_y'])

print('Difference of s2calc on Side Chains with 10A between Bound/Unbound')
paired_ttest(merged_order_10['s2calc_x'], merged_order_10['s2calc_y'])

#Create OP 5A Summary
order5_summary = pd.DataFrame()
n = 1
for i in order_5['PDB'].unique():
    tmp = order_5[order_5['PDB'] == i]
    order5_summary.loc[n, 'PDB'] = i
    order5_summary.loc[n, 'Average_Order5_Calc'] = tmp['s2calc'].mean()
    n += 1


order_5_summary_AH = order5_summary.merge(AH_key, left_on=['PDB'], right_on=['PDB'])
order_5_summary_holo = order_5_summary_AH[order_5_summary_AH['Apo_Holo']=='Holo']
order_5_summary_apo = order_5_summary_AH[order_5_summary_AH['Apo_Holo']=='Apo']
print('number of pairs:')
print(len(order_5_summary_AH.index))

order_5_summary_holo.to_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/holo_order_summary_5.csv')
order_5_summary_apo.to_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/apo_order_summary_5.csv')


test = order_5_summary_holo.merge(AH_pairs, left_on='PDB', right_on='Holo')
merged_order_summary_5 = test.merge(order_5_summary_apo, left_on=['Apo'], right_on=['PDB']) 
merged_order_summary_5 = merged_order_summary_5.drop_duplicates()

print('merged oder summary 5:')
print(merged_order_summary_5.head())
fig = plt.figure()
sns.boxplot(x=merged_order_summary_5["Ligand"], y=merged_order_summary_5["Average_Order5_Calc_x"])

plt.title('Order Parameter by Ligand')
plt.ylabel('Order Parameter')
plt.xlabel('Ligand')
plt.show()
#fig.savefig('AA_OrderParameter.png')
print(merged_order_summary_5.head())
merged_order_summary_5.to_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/merged_order_summary_5.csv')

#Create OP Far
#order_far = pd.DataFrame()
#for i in order_all['PDB'].unique():
#    tmp_all = order_all[order_all['PDB'] == i]
#    tmp_10 = order_10[order_10['PDB']==i] 
#    merged = tmp_all.merge(tmp_10.drop_duplicates(), on=['resn','resi', 'chain'], 
#                   how='left', indicator=True)
#    tmp_far = merged[merged['_merge'] == 'left_only']
#    order_far = order_far.append(tmp_far, ignore_index=True)

#print(order_far.head())
#order_far = order_far.merge(AH_key, left_on = ['PDB_x'], right_on=['PDB'])
#order_far_holo = order_far[order_far['Apo_Holo'] == 'Holo']
#order_far_apo = order_far[order_far['Apo_Holo'] == 'Apo']

#test = order_far_holo.merge(AH_pairs, left_on='PDB_x', right_on='Holo')
#merged_order_far = test.merge(order_far_apo, left_on=['Apo', 'chain', 'resi'], right_on=['PDB_x', 'chain', 'resi'])  
#merged_order_far = merged_order_far.drop_duplicates()

merged_order_far = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/merged_order_far.csv')
make_dist_plot_AH(merged_order_far['s2calc_x_x'], merged_order_far['s2calc_x_y'], 's2calc', 'Number of Residues', 'Bound v. Unbound s2calc (Further than 10A)', '/Users/stephaniewankowicz/Downloads/qfit_paper/AH_s2calc_>10A')
make_dist_plot_AH(merged_order_far['s2ortho_x_x'], merged_order_far['s2ortho_x_y'], 's2ortho', 'Number of Residues', 'Bound v. Unbound s2ortho (Further than 10A)', '/Users/stephaniewankowicz/Downloads/qfit_paper/AH_s2ortho_>10A')

print('Difference of s2calc on Side Chains >10 A between Bound/Unbound [Entire Protein]')
paired_ttest(merged_order_far['s2calc_x_x'], merged_order_far['s2calc_x_y'])

order_all = order_all[order_all['resn'] != 0]
plot_order = order_all.groupby(by=["resn"])["s2calc"].mean().sort_values().index



#OP by AA type
fig = plt.figure()
sns.boxplot(x=order_all["resn"], y=order_all["s2calc"], order=plot_order)

plt.title('Order Parameter by Amino Acid Type')
plt.ylabel('Order Parameter')
plt.xlabel('Amino Acids')
fig.savefig('AA_OrderParameter.png')

merged_order_all = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/merged_order_all.csv')
print(merged_order_all.head())
merged_order_all['Difference'] = merged_order_all['s2calc_x'] - merged_order_all['s2calc_y']


fig = plt.figure()
merged_order_far['Difference'] = merged_order_far['s2calc_x_x'] - merged_order_far['s2calc_x_y']
merged_order_5['Difference'] = merged_order_5['s2calc_x'] - merged_order_5['s2calc_y']
sns.kdeplot(merged_order_far['Difference'], label='>10A', bw=0.02)
sns.kdeplot(merged_order_5['Difference'], label='5A', bw=0.02)
sns.kdeplot(merged_order_all['Difference'],label='All', bw=0.02 )
fig.savefig('/Users/stephaniewankowicz/Downloads/qfit_paper/merged_order_far_difference.png')
#print(merged_order_far['Difference'].describe())

fig = plt.figure()
merged_order_5['Difference'] = merged_order_5['s2calc_x'] - merged_order_5['s2calc_y']
sns.kdeplot(merged_order_5['Difference'], label='Difference', bw=0.02)
fig.savefig('/Users/stephaniewankowicz/Downloads/qfit_paper/merged_order_5_difference.png')
#print((merged_order_5['Difference'].describe()))



