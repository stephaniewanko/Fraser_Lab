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

#SUBSET DOWN TO PAIRS
pair_subset = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/close_RMSF_summary.csv')
AH_pairs = AH_pairs.loc[(AH_pairs['Apo'].isin(pair_subset['Apo'])) & (AH_pairs['Holo'].isin(pair_subset['Holo']))]

print(len(AH_pairs.index))
#AH_pairs["Holo_Res"] = AH_pairs["Holo_Res"].astype('float') #pd.to_numeric(
make_dist_plot_AH(AH_pairs['Holo_Res'], AH_pairs['Apo_Res'], 'Resolution', 'Number of Structures', 'Apo v. Holo s2calc (Entire Protein)', 'FullResolution')
print('Difference of s2calc on only Polar Side Chains between Holo/Apo [Entire Protein]')
paired_ttest(AH_pairs['Apo_Res'], AH_pairs['Holo_Res'])
print(AH_pairs['Holo_Res'].median())
print(AH_pairs['Apo_Res'].median())

print(AH_pairs['Apo_Res'].quantile(0.25))
print(AH_pairs['Holo_Res'].quantile(0.25))

#print(AH_pairs[AH_pairs['Apo_Res']<1.5])
#print(AH_pairs[AH_pairs['Holo_Res']<1.5])
AH_pairs[(AH_pairs['Holo_Res']<1.5) & (AH_pairs['Apo_Res']<1.5)].to_csv('for_aniso_refine.txt')

high_res = AH_pairs[(AH_pairs['Holo_Res']<1.5) | (AH_pairs['Apo_Res']<1.5)]

high_res['Holo'].to_csv('holo_highres.txt', index=False)
high_res['Apo'].to_csv('apo_highres.txt', index=False)


