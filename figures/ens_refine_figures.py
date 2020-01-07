#packages
import pandas as pd
import numpy as np
import os
import re
import csv
import math
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import scipy
import sys
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
from scipy import stats
import matplotlib.patches as mpatches
from matplotlib import lines as mpl_lines

def extended(ax, x, y, **args):

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    x_ext = np.linspace(xlim[0], xlim[1], 100)
    p = np.polyfit(x, y , deg=1)
    y_ext = np.poly1d(p)(x_ext)
    ax.plot(x_ext, y_ext, **args)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    return ax
    
# Load in original Paper Data
os.chdir('/Users/stephaniewankowicz/Dropbox/Fraser_Rotation/')
ens_refine_org = pd.read_csv('ens_refine_graphing.csv')

# Load in Color info
os.chdir('/Users/stephaniewankowicz/Dropbox/Fraser_Rotation/190719_ens_refine_output/new_output/')
colors=pd.read_csv('PDB_colors.csv')

##OLD PHENIX

os.chdir('/Users/stephaniewankowicz/Dropbox/Fraser_Rotation/ens_write_up/old_phenix/')
path=os.getcwd()



all_files = glob.glob(path + "/*_ens_refinement_output.csv")
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)
old_phenix = pd.concat(li, axis=0, ignore_index=True)
print(len(all_files))

old_phenix_complete = old_phenix.dropna()
old_phenix_complete = ens_refine_org.merge(old_phenix_complete, on='PDB')
old_phenix_complete = old_phenix_complete.merge(colors, on='PDB')
old_phenix_complete.head()

##GRAPHING

#ENSEMBLE SIZE
test = old_phenix_complete
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)
x = np.linspace(0, 300, 300)
ax.set_ylim(0,300)
ax.set_xlim(0,300)
scatter=ax.scatter(test['Ens_Size'], test['Org_Ens_Size'], cmap='plasma', label=test['PDB'])#, s=test['weights']) #c=test['Color'],
slope, intercept, r_value, p_value, std_err = stats.linregress(test['Ens_Size'], test['Org_Ens_Size'])
predict_y = intercept + slope * test['Ens_Size']
#ax = extended(ax, test['Ens_Size'], predict_y,  color="black", lw=2, label='Regression Line r2={}'.format(r_value))
line = mpl_lines.Line2D(x, x, color='red', label="X=Y")
ax.add_line(line)
#black_patch = mpatches.Patch(color='black', label='Regression Line r2={}'.format(r_value))
red_patch  = mpatches.Patch(color='red', label='Y=X Line')
ax.set_xlabel('Re-run Ensemble Size', fontsize=16)
ax.set_ylabel('Original Ensemble Size', fontsize=16)
#legend1 = ax.legend(*scatter.legend_elements(prop="colors", alpha=0.6), loc="upper right", title="PDB")
#ax.add_artist(legend1)
ax.legend(handles=[red_patch])
plt.show()

#RESOLUTION
test = old_phenix_complete


fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)
x = np.linspace(0, 300, 300)
ax.set_ylim(0,3)
ax.set_xlim(0,100)
scatter=ax.scatter(test['Ens_Size'], test['Resolution'], cmap='plasma', label=test['PDB'])#, s=test['weights']) #c=test['Color'],
slope, intercept, r_value, p_value, std_err = stats.linregress(test['Ens_Size'], test['Org_Ens_Size'])
predict_y = intercept + slope * test['Ens_Size']
#ax = extended(ax, test['Ens_Size'], predict_y,  color="black", lw=2, label='Regression Line r2={}'.format(r_value))
line = mpl_lines.Line2D(x, x, color='red', label="X=Y")
#ax.add_line(line)
#black_patch = mpatches.Patch(color='black', label='Regression Line r2={}'.format(r_value))
red_patch  = mpatches.Patch(color='red', label='Y=X Line')
ax.set_xlabel('Re-run Ensemble Size', fontsize=16)
ax.set_ylabel('Resolution', fontsize=16)
#legend1 = ax.legend(*scatter.legend_elements(prop="colors", alpha=0.6), loc="upper right", title="PDB")
#ax.add_artist(legend1)
#ax.legend(handles=[red_patch])
plt.show()



#RFREE
test = old_phenix_complete
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)
x = np.linspace(100, 100)
ax.set_ylim(0.1,0.3)
ax.set_xlim(0.1,0.3)
scatter=ax.scatter(test['Final_Rfree'], test['Org_Rfree'], c=test['Color'], cmap='plasma', label=test['PDB'], s=100)
slope, intercept, r_value, p_value, std_err = stats.linregress(test['Final_Rfree'], test['Org_Rfree'])
predict_y = intercept + slope * test['Final_Rfree']
#ax = extended(ax, test['Final_Rfree'], predict_y,  color="black", lw=2, label='Regression Line r2={}'.format(r_value))
line = mpl_lines.Line2D(x, x, color='red', label="X=Y")
ax.add_line(line)
black_patch = mpatches.Patch(color='black', label='Regr ession Line r2={}'.format(r_value))
red_patch  = mpatches.Patch(color='red', label='Y=X Line')
ax.set_xlabel('Re-Run Rfree', fontsize=16)
ax.set_ylabel('Original Rfree', fontsize=16)
#legend1 = ax.legend(*scatter.legend_elements(prop="colors", alpha=0.6), loc="upper right", title="PDB")
#ax.add_artist(legend1)
#ax.legend(handles=[red_patch, black_patch])
#plt.legend(handles=[red_patch, black_patch, legend1])
plt.show()



#RWORK
test = old_phenix_complete
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)
x = np.linspace(100, 100)
#ax.set_ylim(0.1,0.3)
#ax.set_xlim(0.1,0.3)
scatter=ax.scatter(test['Final_Rwork'], test['Org_Rwork'], c=test['Color'], cmap='plasma', label=test['PDB'], s=100)
slope, intercept, r_value, p_value, std_err = stats.linregress(test['Final_Rwork'], test['pTLS'])
predict_y = intercept + slope * test['Final_Rwork']
#ax = extended(ax, test['Final_Rfree'], predict_y,  color="black", lw=2, label='Regression Line r2={}'.format(r_value))
line = mpl_lines.Line2D(x, x, color='red', label="X=Y")
#ax.add_line(line)
red_patch = mpatches.Patch(color='black', label='Regr ession Line r2={}'.format(r_value))
black_patch  = mpatches.Patch(color='red', label='Y=X Line')
ax.set_xlabel('Re-Run Rwork', fontsize=16)
ax.set_ylabel('Original Rwork', fontsize=16)
#legend1 = ax.legend(*scatter.legend_elements(prop="colors", alpha=0.6), loc="upper right", title="PDB")
#ax.add_artist(legend1)
#ax.legend(handles=[red_patch, black_patch])
#plt.legend(handles=[red_patch, black_patch, legend1])
plt.show()


##RMSF

os.chdir('/Users/stephaniewankowicz/Dropbox/Fraser_Rotation/qfit_refine_stru/190828_RMSF/')
path=os.getcwd()
all_files = glob.glob(path + "/*_qfit_RMSF.csv")
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)
ens_refine_rmsf_all = pd.concat(li, axis=0, ignore_index=True)
print(len(all_files))


