import pandas as pd
from figure_functions import *	
import numpy as np
import glob
#from scipy.interpolate import spline

os.chdir('/Users/stephaniewankowicz/Downloads/qfit/pair_docs/')
AH_key=pd.read_csv('qfit_AH_key_191218.csv')

os.chdir('/Users/stephaniewankowicz/Downloads/qfit_paper/')
path=os.getcwd()

apo = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/order_all_apo.csv')
holo = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/order_all_holo.csv')
dist_all_collapse = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/dist_all_collapse.csv')
print(len(dist_all_collapse.index))
dist_all_collapse = dist_all_collapse.merge(AH_key, on = ['PDB'])
dist_all_collapse = dist_all_collapse.drop_duplicates()
print(dist_all_collapse.head())
print(len(dist_all_collapse.index))

dist_all_collapse.to_csv('dist_all_collapse')
dist_all_collapse_holo = dist_all_collapse[dist_all_collapse['Apo_Holo'] == 'Holo']
dist_all_collapse_apo = dist_all_collapse[dist_all_collapse['Apo_Holo'] == 'Apo']
print(len(dist_all_collapse_holo.index))
print(len(dist_all_collapse_apo.index))
test = dist_all_collapse_holo.merge(AH_pairs, left_on='PDB', right_on='Holo')
dist_all_collapse_m = test.merge(dist_all_collapse_apo, left_on='Apo', right_on='PDB')
dist_all_collapse_m = dist_all_collapse_m.drop_duplicates()
print('dist_all_collapse_m')
print(dist_all_collapse_m.head())
merged_order_all = pd.read_csv('/Users/stephaniewankowicz/Downloads/qfit_paper/merged_order_all.csv')
merged_order_all['Difference'] = merged_order_all['s2calc_x'] - merged_order_all['s2calc_y']

print(len(apo.index))
print(len(holo.index))
apo = apo.dropna(subset=['resi'])
holo = holo.dropna(subset=['resi'])


holo['resi'] = holo['resi'].astype(int)
holo['res'] = holo['resi'].astype(str) + holo['chain']

apo['resi'] = apo['resi'].astype(int)
apo['res'] = apo['resi'].astype(str) + apo['chain']

print(len(apo.index))
print(apo.head())
merged_order_all['resi'] = merged_order_all['resi'].astype(int)
merged_order_all['res'] = merged_order_all['resi'].astype(str) + merged_order_all['chain']

dist_holo_order = dist_all_collapse_holo.merge(holo, left_on=['PDB', 'res'], right_on=['PDB', 'res'])
dist_apo_order = dist_all_collapse_apo.merge(apo, left_on=['PDB', 'res'], right_on=['PDB', 'res'])
dist_holo_order = dist_holo_order.drop_duplicates()
dist_apo_order = dist_apo_order.drop_duplicates()
dist_apo_order.to_csv('dist_apo_order.csv')
dist_holo_order.to_csv('dist_holo_order.csv')
#test = pd.concat(dist_apo_order, dist_holo_order)
print('test')
#print(test.head())
print('dist_apo_order')
print(dist_apo_order.head())

fig = plt.figure()
sns.relplot(data=dist_apo_order, kind="line",
    x="Distance", y="s2calc", col="PDB",
    hue="PDB", style="Apo_Holo_x",
)
plt.show()
