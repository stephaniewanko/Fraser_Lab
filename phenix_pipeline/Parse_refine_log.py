#!/usr/bin/env python
#last edited: 2019-04-09
#last edited by: Stephanie Wankowicz

import pandas as pd
import os
import datetime
import datetime
import argparse

#create df
refine_df=pd.DataFrame(columns=['PDB','Date', 'Starting_Rfree', 'Ending_Rfree', 'Starting_Rwork', 'Ending_Rwork', 'Number of Refinement', 'delta_Rwork', 'delta_Rfree'])

#parse refinement output .log
def parse_refine_log(log_file, PDB):
    file=open(log_file, 'r') #take this in as an arguement
    start_rwork=0
    start_rfree=0
    final_rwork=0
    final_rfree=0
    now = datetime.datetime.now()
    
    for line in file:
        if line.startswith('Command line arguments'):
            pdb_name=line.split('.pdb')[0][-4:]
            
        elif line.startswith('Start R-work'):
            start_rwork=float(line.split('=')[1][1:7])
            start_rfree=float(line.split('=')[2][1:7])   
            
        elif line.startswith('Final R-work'):
            final_rwork=float(line.split('=')[1][1:7])
            final_rfree=float(line.split('=')[2][1:7])
            
    refine_df.loc[1,'PDB']=PDB
    refine_df.loc[1,'Starting_Rfree']=start_rfree
    refine_df.loc[1,'Ending_Rfree']=final_rfree
    refine_df.loc[1,'Starting_Rwork']=start_rwork
    refine_df.loc[1,'Ending_Rwork']=final_rwork
    refine_df.loc[1,'Number of Refinement']=2
    refine_df.loc[1,'delta_Rwork']=refine_df.loc[1,'Starting_Rwork']-refine_df.loc[1,'Ending_Rwork']
    refine_df.loc[1,'delta_Rfree']=refine_df.loc[1,'Starting_Rfree']-refine_df.loc[1,'Ending_Rfree']
    refine_df.loc[1,'Date']=now.strftime("%Y-%m-%d")


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('-log_file')
    p.add_argument('-PDB')
    args = p.parse_args()
    parse_refine_log(args.log_file, args.PDB)
    refine_df.to_csv(args.PDB+'_refine_df.csv')

