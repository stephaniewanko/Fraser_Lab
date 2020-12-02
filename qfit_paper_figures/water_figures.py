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


os.chdir('/Users/stephaniewankowicz/Downloads/qfit_paper/water_partial')
path=os.getcwd()

all_files = glob.glob(path + "/*partialwatercloseresidue.txt")

li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=None)
    df['PDB'] = filename[61:65]
    li.append(df)

water_partial = pd.concat(li, axis=0, ignore_index=True)
water_partial = water_partial.rename(columns={0: "Water_Resi", 1: "Water_Chain", 2: "Chain", 3: "Resi"})
water_partial['Full_Partial'] ='Partial'

print(water_partial.head())
all_files = glob.glob(path + "/*watercloseresidue.txt")

li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=None)
    df['PDB'] = filename[61:65]
    li.append(df)

water = pd.concat(li, axis=0, ignore_index=True)
water= water.rename(columns={0: "Water_Resi", 1: "Water_Chain", 2: "Chain", 3: "Resi", 4: "Distance"})

print(water.head())


all_files = glob.glob("/Users/stephaniewankowicz/Downloads/qfit_paper/*_waterclosestresidue.txt")

li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=None)
    df['PDB'] = filename[47:51]
    li.append(df)

water_closest = pd.concat(li, axis=0, ignore_index=True)
water_closest= water_closest.rename(columns={0: "Water_Resi", 1: "Water_Chain", 2: "Distance"})

print(water_closest.head())

#merge and get water partial distance
water_closest.to_csv('water_closest.csv')
water_partial.to_csv('water_partial.csv')
water_merged = water_closest.merge(water_partial, on=['PDB','Water_Resi', 'Water_Chain'], how='left')  
water_merged = water_merged.drop_duplicates()
print(water_merged.head())

water_partial_dist = water_merged[water_merged['Full_Partial']=='Partial']
print(water_partial_dist.head())

#plot hist of distance of partial versus full occupancy water molecules
fig = plt.figure()
x = range(2)
f, axes = plt.subplots(1, 2, sharey=True, sharex=True)
p1 = sns.boxenplot(water_partial_dist['Distance'], orient='v', ax=axes[0]).set(xlabel = 'Partial', ylabel = 'Distance')
p2 = sns.boxenplot(water_merged['Distance'], orient='v', ax=axes[1]).set(xlabel = 'All', ylabel = '')
plt.savefig('water.png')


