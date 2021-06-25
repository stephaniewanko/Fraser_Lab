#!/usr/bin/env python
#last edited: 2019-05-04
#last edited by: Stephanie Wankowicz
#git: 07-12-2019

#Ensemble Refinement Log File Parser

import pandas as pd
import os
import argparse
import sys

def parse_log(log_file, PDB):
    ens_refine = pd.DataFrame()
    print(log_file)
    PDB = log_file.split('_')[0]
    pTLS = log_file.split('_')[1]
    weights_tmp = log_file.split('_')#[2][0:3]
    weights = weights_tmp[2].split('/')[0]
    print(log_file.split('_')[1])
    print(log_file.split('_')[2])
    ens_refine.loc[1,'PDB'] = PDB
    ens_refine.loc[1,'pTLS'] = pTLS
    ens_refine.loc[1,'weights'] = weights
    log_file.split()
    log=open(log_file, 'r')
    for line in log:
        if line.startswith('FINAL Rwork'):
            ens_refine.loc[1,'Final_Rwork']=line.split('=')[1][1:7]
            ens_refine.loc[1,'Final_Rfree']=line.split('=')[2][1:7]
        elif line.startswith('Ensemble size :'):
            ens_refine.loc[1,'Ens_Size']=line.split(':')[1].strip('\n')
        elif line.startswith('  ensemble_reduction_rfree_tolerance'):
           #print(line)   
           ens_refine.loc[1,'Ens_Red_Rfree_Tol'] = line.split('=')[1].strip('\n')
        elif line.startswith('  ensemble_reduction'):
           #print(line)
           ens_refine.loc[1,'Ens_Red'] = line.split('=')[1].strip('\n')
        elif line.startswith('  tx = '):
           #print(line)
           ens_refine.loc[1,'tx'] = line.split('=')[1].strip('\n')
    location=PDB + '_' + weights + '_' + pTLS + '_ens_refinement_output.csv'
    ens_refine.to_csv(location, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-log_file')
    parser.add_argument('-PDB')
    args = parser.parse_args()
    parse_log(args.Log_File, args.PDB)
