from __future__ import division
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

#READ IN FILES
os.chdir('/Users/stephaniewankowicz/Downloads/qfit_paper/201116/')
path=os.getcwd()
all_files = glob.glob(path + "/*qFit_qfit_RMSF.csv")
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=0, header=0)
    li.append(df)
print(len(all_files))
RMSF = pd.concat(li, axis=0, ignore_index=True)
RMSF['PDB'] = RMSF['PDB_name'].astype(str).str[0:4]
RMSF = RMSF.rename(columns={"Chain": "chain", "resseq":"resi"})
#print(RMSF.head())


RMSF_merged = merge_apo_holo_df(RMSF)
RMSF_merged['rmsf_y'] = RMSF_merged['rmsf_y'].clip(upper=1.5)
RMSF_merged['rmsf_x'] = RMSF_merged['rmsf_x'].clip(upper=1.5)

make_dist_plot_AH(RMSF_merged['rmsf_x'], RMSF_merged['rmsf_y'],'RMSF Entire Protein', 'Number of Residues', 'RMSF across entrie protein', '/Users/stephaniewankowicz/Downloads/qfit_paper/RMSF', )
print('Difference of RMSF on Side Chains between Bound/Unbound [Entire Protein]')
paired_ttest(RMSF_merged['rmsf_x'], RMSF_merged['rmsf_y'])


RMSF_summary = pd.DataFrame()
n = 1
for i in RMSF['PDB'].unique():
    tmp = RMSF[RMSF['PDB'] == i]
    RMSF_summary.loc[n, 'PDB'] = i
    RMSF_summary.loc[n, 'Num_Residues'] = len(tmp.index)
    RMSF_summary.loc[n, 'Num_Alt_Loc'] = len(tmp[tmp['rmsf']>0].index)
    if tmp.rmsf.ge(0).any() == True:
        RMSF_summary.loc[n, 'Alt_Loc'] = 1
    else:
        RMSF_summary.loc[n, 'Alt_Loc'] = 0
    #RMSF_summary.loc[n, 'Apo_Holo'] = tmp['Apo_Holo'].unique()
    RMSF_summary.loc[n, 'Average_RMSF'] = tmp['rmsf'].mean()
    n += 1

RMSF_summary['per_altloc'] = RMSF_summary['Num_Alt_Loc'] / RMSF_summary['Num_Residues']
RMSF_summary['Num_Single'] = RMSF_summary['Num_Residues'] - RMSF_summary['Num_Alt_Loc']
#print(RMSF_summary.head())

RMSF_summary = RMSF_summary.merge(AH_key, on = ['PDB'])
RMSF_summary_holo = RMSF_summary[RMSF_summary['Apo_Holo'] == 'Holo']
RMSF_summary_apo = RMSF_summary[RMSF_summary['Apo_Holo'] == 'Apo']

test = RMSF_summary_holo.merge(AH_pairs, left_on='PDB', right_on='Holo')
RMSF_summary_m = test.merge(RMSF_summary_apo, left_on=['Apo'], right_on=['PDB'])  
RMSF_summary_m= RMSF_summary_m.drop_duplicates()


RMSF_summary_m['Apo_Holo_Multi_Diff'] = RMSF_summary_m['per_altloc_x'] - RMSF_summary_m['per_altloc_y']
#print(RMSF_summary_m.head())

same_qFit = (len((RMSF_summary_m[RMSF_summary_m['Apo_Holo_Multi_Diff']==0]).index))
gain_qFit = (len((RMSF_summary_m[RMSF_summary_m['Apo_Holo_Multi_Diff']>0]).index))
loss_qFit = (len((RMSF_summary_m[RMSF_summary_m['Apo_Holo_Multi_Diff']<0]).index))
total_qFit = same_qFit + gain_qFit + loss_qFit

print('Percent qFit Same:')
print(same_qFit/total_qFit)

print('Percent qFit Gain:')
print(gain_qFit/total_qFit)

print('Percent qFit Loss:')
print(loss_qFit/total_qFit)
print(type(loss_qFit))

same_org = 200
gain_org = 610
loss_org = 305
total_org = same_org + gain_org + loss_org

print('Percent Original Same:')
print(same_org/total_org)

print('Percent Original Gain:')
print(gain_org/total_org)

print('Percent Original Loss:')
print(loss_org/total_org)


#ENTIRE PROTEIN
fig = plt.figure()
a = np.arange(3)
org = [same_org, gain_org, loss_org]
qFit = [same_qFit, gain_qFit, loss_qFit]

barWidth = 0.4
r1 = np.arange(len(org))
r2 = [x + barWidth for x in r1]


p1 = plt.bar(r1, org, color='#9400D3', width=barWidth, label='PDB Deposited')
p2 = plt.bar(r2, qFit, color='#8B0000', width=barWidth, label='qFit')

#plt.title('Holo - Apo Pairs')
plt.ylabel('Number of Pairs')
plt.xticks(a, ('Same','Increase', 'Decrease'))
plt.legend()
fig.savefig('/Users/stephaniewankowicz/Downloads/qfit_paper/SameGainLoss_postqfit.png')

fig = plt.figure()
a = np.arange(3)
f, axes = plt.subplots(1, 3, sharey=True, sharex=True)
p1 = sns.boxenplot(RMSF_summary['per_altloc'], orient='v', ax=axes[0]).set(xlabel='All', ylabel='% Residues with Alt Loc')
p2 = sns.boxenplot(RMSF_summary[RMSF_summary['Apo_Holo']=='Apo']['per_altloc'], orient='v', ax=axes[1]).set(xlabel='Unbound', ylabel='')
p3 = sns.boxenplot(RMSF_summary[RMSF_summary['Apo_Holo']=='Holo']['per_altloc'], orient='v', ax=axes[2]).set(xlabel='Bound', ylabel='')
plt.legend()
#plt.show()
plt.savefig('/Users/stephaniewankowicz/Downloads/qfit_paper/NumberAltConfBoundvUnbound_postqfit.png')


#RMSF SUBSET
os.chdir('/Users/stephaniewankowicz/Downloads/qfit_paper/201116/')
path=os.getcwd()

all_files = glob.glob(path + "/*5.0_rmsf_subset.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=0, header=0)
    li.append(df)

close_RMSF = pd.concat(li, axis=0, ignore_index=True)
#print(len(all_files))
close_RMSF['PDB'] = close_RMSF['PDB_name'].astype(str).str[0:4]
close_RMSF = close_RMSF.rename(columns={"Chain": "chain", "resseq":"resi"})
#print(close_RMSF.head())
merged_close_RMSF = merge_apo_holo_df(close_RMSF)


#print(merged_close_RMSF.head())
make_dist_plot_AH(merged_close_RMSF['rmsf_x'], merged_close_RMSF['rmsf_y'], 'RMSF', 'Number of Residues', 'Bound v. Unbound RMSF (Close Residues)', '/Users/stephaniewankowicz/Downloads/qfit_paper/AH_RMSF_5A')

#STATS
print('Difference of RMSF between Holo/Apo [5A]')
paired_ttest(merged_close_RMSF['rmsf_x'], merged_close_RMSF['rmsf_y'])

close_RMSF_summary = pd.DataFrame()
n = 1
for i in close_RMSF['PDB'].unique():
    tmp = close_RMSF[close_RMSF['PDB'] == i]
    close_RMSF_summary.loc[n, 'PDB'] = i
    close_RMSF_summary.loc[n, 'Num_Residues'] = len(tmp.index)
    close_RMSF_summary.loc[n, 'Num_Alt_Loc'] = len(tmp[tmp['rmsf']>0].index)
    if tmp.rmsf.ge(0).any() == True:
        close_RMSF_summary.loc[n, 'Alt_Loc'] = 1
    else:
        close_RMSF_summary.loc[n, 'Alt_Loc'] = 0
    #close_RMSF_summary.loc[n, 'Apo_Holo'] = tmp['Apo_Holo'].unique()
    close_RMSF_summary.loc[n, 'Average_RMSF'] = tmp['rmsf'].mean()
    n += 1

close_RMSF_summary['per_altloc'] = close_RMSF_summary['Num_Alt_Loc'] / close_RMSF_summary['Num_Residues']

#close_RMSF_summary_merge = merge_apo_holo_df(close_RMSF_summary)
#close_RMSF_summary_merge.to_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/close_RMSF_summary.csv')


close_RMSF_summary = close_RMSF_summary.merge(AH_key)
close_RMSF_sum_holo = close_RMSF_summary[close_RMSF_summary['Apo_Holo']=='Holo']
close_RMSF_sum_apo = close_RMSF_summary[close_RMSF_summary['Apo_Holo']=='Apo']
test = close_RMSF_sum_holo.merge(AH_pairs, left_on='PDB', right_on='Holo')
merged_close_sum_RMSF = test.merge(close_RMSF_sum_apo, left_on='Apo', right_on='PDB')

merged_close_sum_RMSF['Percent_Holo_Close'] = merged_close_sum_RMSF['Num_Alt_Loc_x']/ merged_close_sum_RMSF['Num_Residues_x']
merged_close_sum_RMSF['Percent_Apo_Close'] = merged_close_sum_RMSF['Num_Alt_Loc_y']/ merged_close_sum_RMSF['Num_Residues_y']
merged_close_sum_RMSF['Apo_Holo_Multi_Diff'] = merged_close_sum_RMSF['Percent_Holo_Close'] - merged_close_sum_RMSF['Percent_Apo_Close']
merged_close_sum_RMSF.to_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/close_RMSF_summary.csv')

same_qFit = len((merged_close_sum_RMSF[merged_close_sum_RMSF['Apo_Holo_Multi_Diff']==0]).index)/4
gain_qFit = len(merged_close_sum_RMSF[merged_close_sum_RMSF['Apo_Holo_Multi_Diff']>0].index)/4
loss_qFit = len((merged_close_sum_RMSF[merged_close_sum_RMSF['Apo_Holo_Multi_Diff']<0]).index)/4

total_qFit = same_qFit + gain_qFit + loss_qFit

print('Percent qFit Same:')
print(same_qFit/total_qFit)

print('Percent qFit Gain:')
print(gain_qFit/total_qFit)

print('Percent qFit Loss:')
print(loss_qFit/total_qFit)

same_org = 780
gain_org = 307
loss_org = 256
total_org = same_org + gain_org + loss_org

print('Percent Original Same:')
print(same_org/total_org)

print('Percent Original Gain:')
print(gain_org/total_org)

print('Percent Original Loss:')
print(loss_org/total_org)


#WITHN 5A
fig = plt.figure()
a = range(3)

org = [same_org, gain_org, loss_org]
qFit = [same_qFit, gain_qFit, loss_qFit]

barWidth = 0.4
r1 = np.arange(len(org))
r2 = [x + barWidth for x in r1]


p1 = plt.bar(r1, org, color='#9400D3', width=barWidth, label='Deposited PDB')
p2 = plt.bar(r2, qFit, color='#8B0000', width=barWidth, label='qFit')

plt.ylabel('Number of Pairs')
plt.xticks(a, ('Same','Increase', 'Decrease'))
plt.legend()
fig.savefig('/Users/stephaniewankowicz/Downloads/qfit_paper/GainSameLoss_within5A_postqfit.png')
#plt.show()

fig = plt.figure()
f, axes = plt.subplots(1, 3, sharey=True, sharex=True)
p1 = sns.boxenplot(close_RMSF_summary['per_altloc'], orient='v', ax=axes[0])#.set(xlabel='All', ylabel='% Residues with Alt Loc')
p2 = sns.boxenplot(close_RMSF_summary[close_RMSF_summary['Apo_Holo']=='Apo']['per_altloc'], orient='v', ax=axes[1])#.set(xlabel='Unbound', ylabel='')
p3 = sns.boxenplot(close_RMSF_summary[close_RMSF_summary['Apo_Holo']=='Holo']['per_altloc'], orient='v', ax=axes[2])#.set(xlabel='Bound', ylabel='')
plt.legend()
plt.savefig('/Users/stephaniewankowicz/Downloads/qfit_paper/NumberAltConfBoundvUnbound_wihtin5A_postqfit.png')
