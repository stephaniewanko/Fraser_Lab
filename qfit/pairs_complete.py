#Stephanie Wankowicz

import pandas as pd
import os
import datetime
import argparse
import sys
import fileinput

def find_pairs_done(file):
    #file = open(file, 'r') #take this in as an arguement
    finished_apo = []
    finished_holo = []
    AH_key=pd.read_csv('/mnt/home1/wankowicz/scripts/190503_Apo_Holo_Key.csv')
    pairs=pd.read_csv(file, sep='\t', header=None, names=["PDB"])
    pairs=pairs.merge(AH_key,on='PDB', how='left')
    #print(pairs.head())
    finished_apo=pairs[pairs['Apo_Holo']=='Apo']
    finished_holo=pairs[pairs['Apo_Holo']=='Holo']
    print('apo done:')
    print(len(finished_apo.index))
    print('holo done:')
    print(len(finished_holo.index))
    #print(finished_holo.head())
    #os.chdir('/Users/stephaniewankowicz/Dropbox/Fraser_Rotation/outputs/')
    master_pairs=pd.read_csv('/mnt/home1/wankowicz/scripts/master_pair_list.csv')
    print(master_pairs.head())
    finished_holo_pairs=finished_holo.merge(master_pairs,left_on='PDB', right_on='Holo', how='left')
    print(finished_holo_pairs)
    print(len(finished_holo_pairs.index))
    #print(finished_apo.PDB.isin(finished_holo_pairs.Apo))
    finished_holo_pairs['Pair']=finished_apo.PDB.isin(finished_holo_pairs.Apo).astype(str)
    print(finished_holo_pairs.head())
    finished_pairs=finished_holo_pairs[finished_holo_pairs['Pair']=='True']
    print(len(finished_pairs.index))
    finished_pairs.to_csv('finished_pairs.csv')
    #print(finished_holo_pairs.head())#with open('holo_190904_complete.txt', 'w') as file:
    #    for i in range(0,len(finished_pdbs)):
    #        file.write(str(finished_pdbs[i]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()
    find_pairs_done(args.file)
