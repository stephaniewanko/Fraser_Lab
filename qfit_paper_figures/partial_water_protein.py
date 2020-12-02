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


#resi around partial water
#OP
merged_order_all = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/merged_order_all.csv')
order_all = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/order_all.csv')

merged_bfactor = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/merged_bfactor.csv')
all_bfactor = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/all_bfactor.csv')
high_bfactor_water = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/water_partial/high_bfactor_water.csv')

water_partial = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/water_partial/water_partial.csv')
water_closest = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/water_partial/water_closest.csv')

print(water_closest.head())
print(merged_bfactor.head())
print(merged_order_all.head())
print(order_all.head())

partial_order = water_partial.merge(order_all, left_on=['PDB', 'Resi'], right_on=['PDB', 'resi'])
all_order = water_closest.merge(order_all, left_on=['PDB', 'PDB_Resi'], right_on=['PDB', 'resi'])

print(partial_order.head())

fig = plt.figure()
x = range(2)
f, axes = plt.subplots(1, 2, sharey=True, sharex=True)
p1 = sns.boxenplot(partial_order['s2calc'], orient='v', ax=axes[0]).set(xlabel = 's2calc', ylabel = 'Distance')
p2 = sns.boxenplot(all_order['s2calc'], orient='v', ax=axes[1]).set(xlabel = 'All', ylabel = '')
#plt.show()
plt.savefig('water_order_param.png')

ind_MannWhit(partial_order['s2calc'], all_order['s2calc'])


#ROTAMER
