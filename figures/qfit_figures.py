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
#import mdanalysis

os.chdir('/Users/stephaniewankowicz/Dropbox/Fraser_Rotation/')
AH_key=pd.read_csv('190503_Apo_Holo_Key.csv')
Resolution_key=pd.read_csv('Resolution.csv')

os.chdir('/Users/stephaniewankowicz/Dropbox/Fraser_Rotation/outputs/')
pairs=pd.read_csv('pairs.csv')

os.chdir('/Users/stephaniewankowicz/Dropbox/Fraser_Rotation/qfit_refine_stru/190828_RMSF/')
path=os.getcwd()



all_files = glob.glob(path + "/*_qfit_RMSF.csv")
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)
ens_refine_rmsf_all = pd.concat(li, axis=0, ignore_index=True)
print(len(all_files))

ens_refine_rmsf_all['type']=ens_refine_rmsf_all['PDB_name'].astype(str).str[5:9]
ens_refine_rmsf_all['PDB']=ens_refine_rmsf_all['PDB_name'].astype(str).str[0:4]

RMSF=ens_refine_rmsf_qfit.merge(ens_refine_rmsf_reg, on=['PDB','resseq', 'Chain', 'AA'])


RMSF_Apo=RMSF2[RMSF2['Apo_Holo']=='Apo']
RMSF_Holo=RMSF2[RMSF2['Apo_Holo']=='Holo']
RMSF_Apo = RMSF_Apo.rename(columns={"rmsf_x": "RMSF_Apo"})
RMSF_Holo = RMSF_Holo.rename(columns={"rmsf_x": "RMSF_Holo"})
test=RMSF_Holo.merge(pairs,left_on='PDB', right_on='Holo', how='left')
RMSF_AH=test.merge(RMSF_Apo, left_on=['Apo','resseq', 'AA', 'Chain'], right_on=['PDB', 'resseq', 'AA', 'Chain'], how='left')

#RMSF_AH['AH_diff']=RMSF_AH['rmsf_x_x']-RMSF_AH['rmsf_x_y']
sns.kdeplot(RMSF_Apo['RMSF_Apo'], shade=True)
sns.kdeplot(RMSF_Holo['RMSF_Holo'], shade=True)
