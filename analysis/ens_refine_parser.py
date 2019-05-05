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
    ens_refine=pd.DataFrame()
    ens_refine.loc[1,'PDB']=open(log_file, 'r').read().splitlines()[2]
    ens_refine.loc[1,'pTLS']=open(log_file, 'r').read().splitlines()[4]
    ens_refine.loc[1,'weights']=open(log_file, 'r').read().splitlines()[6]
    ens_refine.loc[1,'output_location']=open(log_file, 'r').read().splitlines()[7]
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('Log_File')
    args = parser.parse_args()
    parse_log(args.Log_File)
