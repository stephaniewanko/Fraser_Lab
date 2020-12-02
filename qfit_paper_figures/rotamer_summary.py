#packages
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


#REFERENCE FILE
os.chdir('/Users/stephaniewankowicz/Downloads/qfit/pair_docs/')
AH_key=pd.read_csv('qfit_AH_key_191218.csv')

os.chdir('/Users/stephaniewankowicz/Downloads/qfit_paper/')
path=os.getcwd()

all_files = glob.glob(path + "/*_qFit_rotamer_output.txt")

li = []
for filename in all_files:
	df = pd.read_csv(filename, index_col=None, header=0, sep=':')
	df['PDB'] = filename[47:51]
	li.append(df)
rotamer = pd.concat(li, axis=0, ignore_index=True)
print(rotamer.head())
rotamer = rotamer[rotamer['residue']!= 'SUMMARY'].reset_index()
split = rotamer['residue'].str.split(" ")
rotamer.to_csv('rotamer_all.csv')

for i in range(0,len(rotamer.index)-1):
	print(i)
	rotamer.loc[i,'chain'] = split[i][1]
	STUPID = str(rotamer.loc[i,'residue'])[3:10]
	print(STUPID)
	rotamer.loc[i,'resi'] = [int(s) for s in STUPID.split() if s.isdigit()]

rotamer.to_csv('rotamer_all.csv')

#ROTAMER SUBSET
all_files = glob.glob(path + "/*5.0_rotamer_subset.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    df['PDB'] = filename[47:51]
    li.append(df)

subset_rotamer = pd.concat(li, axis=0, ignore_index=True)
print(len(all_files))

subset_rotamer['chain_resi'] = subset_rotamer['resi'].map(str) + subset_rotamer['chain']
subset_rotamer['altloc'] = subset_rotamer['residue'].astype(str).str[7]

subset_rotamer = subset_rotamer[subset_rotamer['rotamer'] != 'OUTLIER']

AH_subset_rotamer = subset_rotamer.merge(AH_key, on='PDB')

subset_rotamer_apo = AH_subset_rotamer[AH_subset_rotamer['Apo_Holo'] == 'Apo']
subset_rotamer_holo = AH_subset_rotamer[AH_subset_rotamer['Apo_Holo'] == 'Holo']

summary_holo = rotamer_summary_AH(subset_rotamer_holo)
summary_apo = rotamer_summary_AH(subset_rotamer_apo)

summary_apo.to_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/rotamer_summary_apo.csv')
summary_holo.to_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/rotamer_summary_holo.csv')

print(summary_holo.head())
different_holo = len(summary_holo[summary_holo['Rotamer_Status'] == 'different'].index)
same_holo = len(summary_holo[summary_holo['Rotamer_Status'] == 'same'].index)

apo_len = len(summary_apo.index)
holo_len = len(summary_holo.index)
different_apo = len(summary_apo[summary_apo['Rotamer_Status'] == 'different'].index)
same_apo = len(summary_apo[summary_apo['Rotamer_Status'] == 'same'].index)


#FIGURE
fig, ax = plt.subplots()
barwidth = 0.4

holo = [(different_holo/holo_len), (same_holo/holo_len)]
apo = [(different_apo/apo_len), (same_apo/apo_len)]
print(holo, apo)

r1 = np.arange(len(holo))

ax.bar(r1 - barwidth/2, holo, width=barwidth, edgecolor='white', label='Holo')
ax.bar(r1 + barwidth/2, apo, width=barwidth, edgecolor='white', label='Apo')

#p1 = plt.bar(x[0], different, width=0.7)
#p2 = plt.bar(x[1], same, width=0.7)
#p3 = plt.bar(x[2], both, width=0.7)

ax.set_title('Rotamer Status by Bound/Unbound', fontsize=18)
ax.set_ylabel('Number of Residues', fontsize=18)
ax.set_xticks(r1)
ax.set_xticklabels(('Different','Same'), fontsize=12)
#plt.xticks(r1, ())
fig.tight_layout()
plt.savefig('/Users/stephaniewankowicz/Downloads/qfit_paper/RotamerStatus_by_AH.png')
#plt.show()


AH_rotamer = rotamer_compare(subset_rotamer)
print(AH_rotamer.head())

HA_single = AH_rotamer[(AH_rotamer['Holo_alt_loc'] == 1) & (AH_rotamer['Apo_alt_loc'] == 1)]
HA_multi = AH_rotamer[(AH_rotamer['Holo_alt_loc'] > 1) | (AH_rotamer['Apo_alt_loc'] > 1)]

multi_summary, single_summary= rotamer_AH_summary(HA_multi, HA_single)

AH_rotamer_summary = pd.concat([multi_summary, single_summary], axis=0)
print(AH_rotamer_summary.head())
#CREATE FIGURE
different = len(AH_rotamer_summary[AH_rotamer_summary['Rotamer'] == 'Different'].index)
same = len(AH_rotamer_summary[AH_rotamer_summary['Rotamer'] == 'Same'].index)
both = len(AH_rotamer_summary[AH_rotamer_summary['Rotamer'] == 'Same and Different'].index)
print(different, same, both)

fig = plt.figure
x = range(3)

p1 = plt.bar(x[0], different, width=0.7)
p2 = plt.bar(x[1], same, width=0.7)
p3 = plt.bar(x[2], both, width=0.7)

plt.title('Rotamer Status')
plt.ylabel('Number of Residues')
plt.xticks(x, ('All Different','All Same', 'Same & Different'))
plt.savefig('/Users/stephaniewankowicz/Downloads/qfit_paper/RotamerStatus_5A'+ '.png')


AH_rotamer_summary.to_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/AH_rotamer_summary.csv', index=False)



