#!/usr/bin/env python
#last edited: 2019-05-04
#last edited by: Stephanie Wankowicz

#Ensemble Refinement Log File Parser

import pandas as pd
import os
import datetime
import argparse
import sys

def parse_log(log_file):
    ens_refine = pd.DataFrame()
    PDB = log_file.split('_')[0]
    pTLS = log_file.split('_')[1]
    weights_tmp = log_file.split('_')#[2][0:3]
    weights = weights_tmp[2].split('/')[0]
    print(log_file.split('_')[1])
    print(log_file.split('_')[2])
    ens_refine.loc[1,'PDB'] = PDB
    ens_refine.loc[1,'pTLS'] = pTLS
    ens_refine.loc[1,'weights'] = weights
    #ens_refine.loc[1,'output_location']=open(log_file, 'r').read().splitlines()[7]
    log_file.split()
    #output_location=open(log_file, 'r').read().splitlines()[7]
    log=open(log_file, 'r')
    for line in log:
        #if line.startswith('  RMSD (mean RMSD per structure)'):
            #bond=(next(log), end='')#.split(":")[1]
            #angle=(next(log), end='')#.split(":")[1]
            #bond=(next(log), end='')#.split(":")[1]
            #print(bond)
        if line.startswith('FINAL Rwork'):
            ens_refine.loc[1,'Final_Rwork']=line.split('=')[1][1:7]
            ens_refine.loc[1,'Final_Rfree']=line.split('=')[2][1:7]
        if line.startswith('Ensemble size'):
            ens_refine.loc[1,'Ens_Size']=line.split(':')[1][2:4]
    location=PDB+'_'+weights+'_'+pTLS+'_ens_refinement_output.csv' #output_location+'/'+
    print(ens_refine)
    ens_refine.to_csv(location, index=False)
    #with open('output_location.txt', 'w') as file: # this is going to overwrite
    #    file.write(output_location)
    #return output_location

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('Log_File')
    #parser.add_argument('PDB')
    #parser.add_argument('PDB_name')
    args = parser.parse_args()
    parse_log(args.Log_File)
