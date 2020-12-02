import pandas as pd
from figure_functions import *	
import numpy as np
import glob

#slr =pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/slr_structure_ws.tab', sep='\t', low_memory=False)
qfit_ids = ['1jcz', '1pw9', '2bit', '2hnx', '2rcq', '3dai', '3sza', '4ank', '5k7m'] 

slr = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/slr_qfit.csv', sep=',', low_memory=False)

slr['pdb_pos'] = pd.to_numeric(slr.pdb_pos, errors='coerce')
apo = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/order_all_apo.csv', low_memory=False)
all = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/merged_order_all.csv', low_memory=False)

slr_apo = apo[apo['PDB'].isin(qfit_ids)]
slr_all = all[all['PDB_y'].isin(qfit_ids)]
print(slr_all.head())
slr_all['Difference'] = slr_all['s2calc_y'] - slr_all['s2calc_x'] #apo v. holo?

fig = plt.figure()
sns.distplot(slr_all['Difference'], kde=False, label='OP Difference All')
fig.savefig('OP_Difference_All.png')

slr_apo_merge = slr_apo.merge(slr, left_on=['PDB', 'chain', 'resi'], right_on=['pdb_id', 'pdb_chain', 'pdb_pos'])
slr_all_merge = slr_all.merge(slr, left_on=['PDB_y', 'chain', 'resi'], right_on=['pdb_id', 'pdb_chain', 'pdb_pos'])

slr_apo_merge_pos_TF = slr_apo_merge[slr_apo_merge['positive'] == True]
slr_apo_merge_notpos_TF = slr_apo_merge[slr_apo_merge['positive'] == False]
print('Ind ttest Positive Selction s2calc Apo T/F, column1=Positive Selection, column2=Not Positive Selection')
ind_MannWhit(slr_apo_merge_pos_TF['s2calc'], slr_apo_merge_notpos_TF['s2calc'])

slr_apo_merge_pos_TF = slr_apo_merge_pos_TF[slr_apo_merge_pos_TF['resn'] != 0]
plot_order = slr_apo_merge_pos_TF.groupby(by=["resn"])["s2calc"].mean().sort_values().index

print(slr_apo_merge_pos_TF.head())
#OP by AA type
fig = plt.figure()
sns.boxplot(x=slr_apo_merge_pos_TF["resn"], y=slr_apo_merge_pos_TF["s2calc"], order=plot_order)

plt.title('Order Parameter by Amino Acid Type Positive')
plt.ylabel('Order Parameter')
plt.xlabel('Amino Acids')
fig.savefig('AA_OrderParameter_OP_Positive.png')


plot_order = slr_apo_merge_notpos_TF.groupby(by=["resn"])["s2calc"].mean().sort_values().index

slr_apo_merge_notpos_TF = slr_apo_merge_notpos_TF[slr_apo_merge_notpos_TF['resn'] != 0]
plot_order = slr_apo_merge_notpos_TF.groupby(by=["resn"])["s2calc"].mean().sort_values().index

#OP by AA type
fig = plt.figure()
sns.boxplot(x=slr_apo_merge_notpos_TF["resn"], y=slr_apo_merge_notpos_TF["s2calc"], order=plot_order)

plt.title('Order Parameter by Amino Acid Type Positive')
plt.ylabel('Order Parameter')
plt.xlabel('Amino Acids')
fig.savefig('AA_OrderParameter_OP_NotPositive.png')



fig = plt.figure()
sns.kdeplot(slr_apo_merge_pos_TF['s2calc'], label='Positive Selection', bw=0.05)
sns.kdeplot(slr_apo_merge_notpos_TF['s2calc'], label='Not Positive Selection', bw=0.05)
sns.kdeplot(slr_apo_merge['s2calc'], label='All', bw=0.05)

plt.title('OP of positive selection residues')
plt.xlabel('s2calc')
plt.legend()
#plt.ylabel('Number')
fig.savefig('PositivevNotPositive_apo_Dist.png')

slr_apo_merge_pos_TF = slr_apo_merge[slr_apo_merge['Adj.Pval'] <= slr_apo_merge['Adj.Pval'].quantile(0.25)]
slr_apo_merge_notpos_TF = slr_apo_merge[slr_apo_merge['Adj.Pval'] >= slr_apo_merge['Adj.Pval'].quantile(0.75)]

print('Ind ttest Positive Selction s2calc Apo Quartile, column1=Positive Selection, column2=Not Positive Selection')
ind_MannWhit(slr_apo_merge_pos_TF['s2calc'], slr_apo_merge_notpos_TF['s2calc'])


fig = plt.figure()
sns.kdeplot(slr_apo_merge_pos_TF['s2calc'], label='Positive Selection', bw=0.05)
sns.kdeplot(slr_apo_merge_notpos_TF['s2calc'], label='Not Positive Selection', bw=0.05)
sns.kdeplot(slr_apo_merge['s2calc'], label='All', bw=0.05)

plt.title('OP of positive selection residues by quartile')
plt.xlabel('s2calc')
plt.legend()
#plt.ylabel('Number')
fig.savefig('PositivevNotPositive_quartile_apo_Dist.png')



slr_all_merge_pos = slr_all_merge[slr_all_merge['Adj.Pval'] <= slr_all_merge['Adj.Pval'].quantile(0.25)]
slr_all_merge_nopos = slr_all_merge[slr_all_merge['Adj.Pval'] >= slr_all_merge['Adj.Pval'].quantile(0.75)]
print('Ind ttest Positive Selction Across Protein Difference Quartile, column1=Positive Selection, column2=Not Positive Selection')
ind_MannWhit(slr_all_merge_pos['Difference'], slr_all_merge_nopos['Difference'])

fig = plt.figure()
sns.kdeplot(slr_all_merge_pos['Difference'], label='Positive Selection', bw=0.05)
sns.kdeplot(slr_all_merge_nopos['Difference'], label='Not Positive Selection', bw=0.05)
sns.kdeplot(slr_all_merge['Difference'], label='All', bw=0.05)
plt.xlabel('s2calc')
plt.title('quartile')
plt.legend()
plt.ylabel('')
fig.savefig('PositivevNotPositive_Difference_Dist_All_Quartile.png')

slr_apo_merge_pos_TF = slr_all_merge[slr_all_merge['positive'] == True]
slr_apo_merge_notpos_TF = slr_all_merge[slr_all_merge['positive'] == False]

print('Ind ttest Positive Selction Across Protein Difference T/F, column1=Positive Selection, column2=Not Positive Selection')
ind_MannWhit(slr_all_merge_pos['Difference'], slr_all_merge_nopos['Difference'])

fig = plt.figure()
sns.kdeplot(slr_all_merge_pos['Difference'], label='Positive Selection', bw=0.05)
sns.kdeplot(slr_all_merge_nopos['Difference'], label='Not Positive Selection', bw=0.05)
sns.kdeplot(slr_all_merge['Difference'], label='All', bw=0.05)
plt.xlabel('s2calc')
plt.title('T/F')
plt.legend()
plt.ylabel('')
fig.savefig('PositivevNotPositive_Difference_Dist_All.png')



make_boxenplot_chem(slr_all_merge_pos['Difference'], slr_all_merge_nopos['Difference'], 
	'Positive Selection', 'Not Positive Selection', 'Scalc Order Parameter Difference', '/Users/stephaniewankowicz/Downloads/qfit_paper/slr_s2calc')





#WITHIN 5A

order_5A = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/order_5.csv')
slr_apo_5A = order_5A.merge(slr, left_on=['PDB', 'chain', 'resi'], right_on=['pdb_id', 'pdb_chain', 'pdb_pos'])
print('number of close residues:')
print(len(slr_apo_5A.index))

slr_apo_merge_pos_TF = slr_apo_5A[slr_apo_5A['positive'] == True]
slr_apo_merge_notpos_TF = slr_apo_5A[slr_apo_5A['positive'] == False]
print('Ind ttest Positive Selction s2calc Apo T/F in close residues, column1=Positive Selection, column2=Not Positive Selection')
ind_MannWhit(slr_apo_merge_pos_TF['s2calc'], slr_apo_merge_notpos_TF['s2calc'])
print('positive residues:')
print(len(slr_apo_merge_pos_TF.index))

print('not positive residues:')
print(len(slr_apo_merge_notpos_TF.index))

fig = plt.figure()
sns.kdeplot(slr_apo_merge_pos_TF['s2calc'], label='Positive Selection', bw=0.05)
sns.kdeplot(slr_apo_merge_notpos_TF['s2calc'], label='Not Positive Selection', bw=0.05)
sns.kdeplot(slr_apo_merge['s2calc'], label='All', bw=0.05)

plt.title('OP of positive selection residues within 5A')
plt.xlabel('s2calc')
plt.legend()
#plt.ylabel('Number')
fig.savefig('PositivevNotPositive_apo_Dist_5A.png')


slr_apo_merge_noexposed = slr_apo_merge[slr_apo_merge['buried']=='buried']
slr_apo_merge_pos_TF = slr_apo_merge_noexposed[slr_apo_merge_noexposed['positive'] == True]
slr_apo_merge_notpos_TF = slr_apo_merge_noexposed[slr_apo_merge_noexposed['positive'] == False] 

print('slr_apo_merge_notpos_TF')
print(len(slr_apo_merge_notpos_TF.index))

print('slr_apo_merge_pos_TF')
print(len(slr_apo_merge_pos_TF.index))

print('Ind ttest Positive Selction s2calc Apo T/F Not exposed, column1=Positive Selection, column2=Not Positive Selection')
ind_MannWhit(slr_apo_merge_pos_TF['s2calc'], slr_apo_merge_notpos_TF['s2calc'])


fig = plt.figure()
sns.kdeplot(slr_apo_merge_pos_TF['s2calc'], label='Positive Selection', bw=0.05)
sns.kdeplot(slr_apo_merge_notpos_TF['s2calc'], label='Not Positive Selection', bw=0.05)
sns.kdeplot(slr_apo_merge['s2calc'], label='All', bw=0.05)

plt.title('OP of positive selection residues buried')
plt.xlabel('s2calc')
plt.legend()
#plt.ylabel('Number')
fig.savefig('PositivevNotPositive_buried.png')


print('Exposed Residues:')
slr_apo_merge_exposed = slr_apo_merge[slr_apo_merge['buried']=='exposed']
slr_apo_merge_pos_TF = slr_apo_merge_exposed[slr_apo_merge_exposed['positive'] == True]
slr_apo_merge_notpos_TF = slr_apo_merge_exposed[slr_apo_merge_exposed['positive'] == False] 

print('slr_apo_merge_notpos_TF')
print(len(slr_apo_merge_notpos_TF.index))

print('slr_apo_merge_pos_TF')
print(len(slr_apo_merge_pos_TF.index))

print('Ind ttest Positive Selction s2calc Apo T/F exposed, column1=Positive Selection, column2=Not Positive Selection')
ind_MannWhit(slr_apo_merge_pos_TF['s2calc'], slr_apo_merge_notpos_TF['s2calc'])


fig = plt.figure()
sns.kdeplot(slr_apo_merge_pos_TF['s2calc'], label='Positive Selection', bw=0.05)
sns.kdeplot(slr_apo_merge_notpos_TF['s2calc'], label='Not Positive Selection', bw=0.05)
sns.kdeplot(slr_apo_merge['s2calc'], label='All', bw=0.05)

plt.title('OP of positive selection residues exposed')
plt.xlabel('s2calc')
plt.legend()
#plt.ylabel('Number')
fig.savefig('PositivevNotPositive_exposed.png')
