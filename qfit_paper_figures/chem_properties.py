 #packages
import pandas as pd
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
from scipy import stats
import matplotlib.patches as mpatches
from figure_functions import *	

#import DF
order5_summary = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/merged_order_summary_5.csv')
chem = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/Chemical_Descriptors_PDB.csv')
print(order5_summary.head())
order5_summary['Difference'] = order5_summary['Average_Order5_Calc_x'] - order5_summary['Average_Order5_Calc_y']
print(order5_summary.head())

order5_chem = order5_summary.merge(chem, on='Holo')
print(order5_chem.head())
print(len(order5_chem['PDB_x'].unique()))
order5_chem['Average_Order5_Calc_x'] = order5_chem['Average_Order5_Calc_x'].clip(lower=0)

order5_chem['NumHAcceptors_PerHeavyAtom'] = order5_chem['NumHAcceptors']/order5_chem['HeavyAtomCount']
order5_chem['NumHDonors_PerHeavyAtom'] = order5_chem['NumHDonors']/order5_chem['HeavyAtomCount']
order5_chem['NumHTotal'] = order5_chem['NumHAcceptors'] + order5_chem['NumHDonors']
order5_chem['NumHTotal_PerHeavyAtom'] = order5_chem['NumHTotal']/order5_chem['HeavyAtomCount']
order5_chem['NumRotatableBonds_PerHeavyAtom'] = order5_chem['NumRotatableBonds']/order5_chem['HeavyAtomCount']

order5_chem_lowMolWeight = order5_chem[order5_chem['MolWeight'] <= order5_chem['MolWeight'].quantile(0.25)]
order5_chem_highMolWeight = order5_chem[order5_chem['MolWeight'] >= order5_chem['MolWeight'].quantile(0.75)]

order5_chem_lowRotBonds = order5_chem[order5_chem['NumRotatableBonds'] <= order5_chem['NumRotatableBonds'].quantile(0.25)]
order5_chem_highRotBonds = order5_chem[order5_chem['NumRotatableBonds'] >= order5_chem['NumRotatableBonds'].quantile(0.75)]

order5_chem_lowlogP = order5_chem[order5_chem['MolLogP'] <= order5_chem['MolLogP'].quantile(0.25)]
order5_chem_highlogP = order5_chem[order5_chem['MolLogP'] >= order5_chem['MolLogP'].quantile(0.75)]

order5_chem_lowRotBonds_PerHeavyAtom = order5_chem[order5_chem['NumRotatableBonds_PerHeavyAtom'] <= order5_chem['NumRotatableBonds_PerHeavyAtom'].quantile(0.25)]
order5_chem_highRotBonds_PerHeavyAtom = order5_chem[order5_chem['NumRotatableBonds_PerHeavyAtom'] >= order5_chem['NumRotatableBonds_PerHeavyAtom'].quantile(0.75)]

order5_chem_lowHdonor_PerHeavyAtom= order5_chem[order5_chem['NumHDonors_PerHeavyAtom'] <= order5_chem['NumHDonors_PerHeavyAtom'].quantile(0.25)]
order5_chem_highHdonor_PerHeavyAtom= order5_chem[order5_chem['NumHDonors_PerHeavyAtom'] >= order5_chem['NumHDonors_PerHeavyAtom'].quantile(0.75)]

order5_chem_lowHaccept_PerHeavyAtom = order5_chem[order5_chem['NumHAcceptors_PerHeavyAtom'] <= order5_chem['NumHAcceptors_PerHeavyAtom'].quantile(0.25)]
order5_chem_highHaccept_PerHeavyAtom = order5_chem[order5_chem['NumHAcceptors_PerHeavyAtom'] >= order5_chem['NumHAcceptors_PerHeavyAtom'].quantile(0.75)]

order5_chem_lowHtotal_PerHeavyAtom = order5_chem[order5_chem['NumHTotal_PerHeavyAtom'] <= order5_chem['NumHTotal_PerHeavyAtom'].quantile(0.25)]
order5_chem_highHtotal_PerHeavyAtom = order5_chem[order5_chem['NumHTotal_PerHeavyAtom'] >= order5_chem['NumHTotal_PerHeavyAtom'].quantile(0.75)]


fig = plt.figure()
p1 = sns.scatterplot(order5_chem_highRotBonds_PerHeavyAtom['Average_Order5_Calc_x'], order5_chem_highRotBonds_PerHeavyAtom['Difference'], color='r')
p2 = sns.scatterplot(order5_chem_lowRotBonds_PerHeavyAtom['Average_Order5_Calc_x'], order5_chem_lowRotBonds_PerHeavyAtom['Difference'], color='b')
plt.xlabel('Bound OP')
plt.ylabel('Bound-Unbound OP Difference')
#plt.title(title)
fig.savefig('Rotatable_Bonds_Difference_Order5.png')


make_boxenplot_chem(order5_chem_lowlogP['Average_Order5_Calc_x'], order5_chem_highlogP['Average_Order5_Calc_x'], 
	'Low LogP', 'High LogP', 'Scalc Order Parameters', '/Users/stephaniewankowicz/Downloads/qfit_paper/logp_orderparameters')
print('Ind ttest order5-logP, column1=low, column2=high')
ind_MannWhit(order5_chem_lowlogP['Average_Order5_Calc_x'], order5_chem_highlogP['Average_Order5_Calc_x'])

make_boxenplot_chem(order5_chem_lowRotBonds_PerHeavyAtom['Average_Order5_Calc_x'], order5_chem_highRotBonds_PerHeavyAtom['Average_Order5_Calc_x'], 
	'Low Rotable Bonds per Heavy Atom', 'High Rotable Bonds per Heavy Atom', 'Scalc Order Parameters', '/Users/stephaniewankowicz/Downloads/qfit_paper/rotatablebonds_orderparameters')
print('Ind ttest order5-Rotatable Bonds, column1=low, column2=high')
ind_MannWhit(order5_chem_lowRotBonds_PerHeavyAtom['Average_Order5_Calc_x'], order5_chem_highRotBonds_PerHeavyAtom['Average_Order5_Calc_x'])

make_boxenplot_chem(order5_chem_lowMolWeight['Average_Order5_Calc_x'], order5_chem_highMolWeight['Average_Order5_Calc_x'], 
	'Low Molecular Weight', 'High Molecular Weight', 'Scalc Order Parameters', '/Users/stephaniewankowicz/Downloads/qfit_paper/MW_orderparameters')
print('Ind ttest order5-MW, column1=low, column2=high')
ind_MannWhit(order5_chem_lowMolWeight['Average_Order5_Calc_x'], order5_chem_highMolWeight['Average_Order5_Calc_x'])

make_boxenplot_chem(order5_chem_lowHdonor_PerHeavyAtom['Average_Order5_Calc_x'], order5_chem_highHdonor_PerHeavyAtom['Average_Order5_Calc_x'], 
	'Low H-Bond Donors per Heavy Atom', 'High H-Bond Donors per Heavy Atom', 'Scalc Order Parameters', '/Users/stephaniewankowicz/Downloads/qfit_paper/Hdonor_orderparameters')
print('Ind ttest order5-Hbond Donor, column1=low, column2=high')
ind_MannWhit(order5_chem_lowHdonor_PerHeavyAtom['Average_Order5_Calc_x'], order5_chem_highHdonor_PerHeavyAtom['Average_Order5_Calc_x'])

make_boxenplot_chem(order5_chem_lowHaccept_PerHeavyAtom['Average_Order5_Calc_x'], order5_chem_highHaccept_PerHeavyAtom['Average_Order5_Calc_x'], 
	'Low H-Bond Accept per Heavy Atom', 'High H-Bond Accept per Heavy Atom', 'Scalc Order Parameters', '/Users/stephaniewankowicz/Downloads/qfit_paper/Haccept_orderparameters')
print('Ind ttest order5-Hbond acceptor, column1=low, column2=high')
ind_MannWhit(order5_chem_lowHaccept_PerHeavyAtom['Average_Order5_Calc_x'], order5_chem_highHaccept_PerHeavyAtom['Average_Order5_Calc_x'])

make_boxenplot_chem(order5_chem_lowHtotal_PerHeavyAtom['Average_Order5_Calc_x'], order5_chem_highHtotal_PerHeavyAtom['Average_Order5_Calc_x'], 
	'Low H-Bond Total per Heavy Atom', 'High H-Bond Total per Heavy Atom', 'Scalc Order Parameters', '/Users/stephaniewankowicz/Downloads/qfit_paper/Htotal_orderparameters')
print('Ind ttest order5-Hbond total, column1=low, column2=high')
ind_MannWhit(order5_chem_lowHtotal_PerHeavyAtom['Average_Order5_Calc_x'], order5_chem_highHtotal_PerHeavyAtom['Average_Order5_Calc_x'])


#Rotatable Bonds with Ligand B-Factor
bfactor_ligand_merged = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/Bfactor_Ligand_Summary.csv')
print(bfactor_ligand_merged.head())
order5_chem_ligand_b = order5_chem.merge(bfactor_ligand_merged, left_on='PDB_x', right_on='PDB')

order5_chem_lowRotBonds_PerHeavyAtom_ligand_b = order5_chem_ligand_b[order5_chem_ligand_b['NumRotatableBonds_PerHeavyAtom'] <= order5_chem_ligand_b['NumRotatableBonds_PerHeavyAtom'].quantile(0.25)]
order5_chem_highRotBonds_PerHeavyAtom_ligand_b = order5_chem_ligand_b[order5_chem_ligand_b['NumRotatableBonds_PerHeavyAtom'] >= order5_chem_ligand_b['NumRotatableBonds_PerHeavyAtom'].quantile(0.75)]

make_boxenplot_chem(order5_chem_lowRotBonds_PerHeavyAtom_ligand_b['Average_Bfactor_y'], order5_chem_highRotBonds_PerHeavyAtom_ligand_b['Average_Bfactor_y'], 
	'Low Rotable Bonds per Heavy Atom', 'High Rotable Bonds per Heavy Atom', 'Ligand B-factors', '/Users/stephaniewankowicz/Downloads/qfit_paper/rotatablebonds_ligandbfactors')
print('Ind ttest ligand b factors-Rotatable Bonds, column1=low, column2=high')
ind_MannWhit(order5_chem_lowRotBonds_PerHeavyAtom_ligand_b['Average_Bfactor_y'], order5_chem_highRotBonds_PerHeavyAtom_ligand_b['Average_Bfactor_y'])


#Ouput
order5_chem.to_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/merged_order_summary_5_chem.csv')
