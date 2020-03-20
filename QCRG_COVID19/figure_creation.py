#import packages
import pandas as pd
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
from scipy import stats
import matplotlib.patches as mpatches
from matplotlib import rc
plt.rcParams['font.family'] = 'Helvetica'

#load in files 
os.chdir('/Users/stephaniewankowicz/Downloads/')
bait_prey = pd.read_csv('bait_preys.txt', sep='\t')

os.chdir('/Users/stephaniewankowicz/Dropbox/Fraser_Rotation/outputs/')
all_lung=pd.read_csv('gTEX_alllung.csv')
gtex_subset=pd.read_csv('gTEX_subset.csv')
gnomad_subset=pd.read_csv('gnomad_subset.csv')
gtex_subset_drugs = pd.read_csv('gTEX_subset_drugs.csv')
gtex_subset_interest = pd.read_csv('gTEX_subset_highinterest.csv')
gnomad_subset_drugs = pd.read_csv('gnomad_subset_drugs.csv')
gnomad_subset_interest = pd.read_csv('gnomad_subset_high_interest.csv')
gnomad_random = pd.read_csv('gnomad_subset_random_5000.csv')


#creating figure files
gtex_subset['label'] = 'Interacting Proteins'
gtex_subset_drugs['label'] = 'Drug Target'
gtex_subset_interest['label'] = 'High Interest'
gtex_all = pd.concat([gtex_subset, gtex_subset_interest, gtex_subset_drugs], ignore_index=True)
