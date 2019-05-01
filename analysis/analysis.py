#Baseline Analysis
#Stephanie Wankowicz
#4/30/2019

#packages
import numpy as np
import pandas as pd
import os
import datetime
import argparse
import sys


def main(PDB, output, RMSD):
    main_df=pd.read_csv('/wynton/home/fraserlab/swankowicz/190430_Apo_Lig_Pairs/DF_output.txt')
    summary_df=pd.DataFrame(columns=['PDB','Date', 'Per_Multi_Conf', 'Num_Atom_Multi', 'Total_Atom_Structure', 'Multi_Res')
    now = datetime.datetime.now()
    file=open(output, 'r') #take this in as an arguement
    for line in file:
        all_atoms=line
        subset_atoms=line
        per_multi=line
    file=open(RMSD, 'r')
    multi_conf=0
    for line in file:
        if line.endswith(2):
            multi_conf=+1
    summary_df.loc[1,'PDB']=PDB
    summary_df.loc[1,'Date']=Now
    summary_df.loc[1,'Per_Multi_Conf']=per_multi
    summary_df.loc[1,'Num_Atom_Multi']=subset_atoms
    summary_df.loc[1,'Multi_Res']=multi_conf
    main_df=main_df.append(summary_df)
    main_df.to_csv('/wynton/home/fraserlab/swankowicz/190430_Apo_Lig_Pairs/DF_output.txt')
    



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-PDB','--PDB_name', type=float)
    p.add_argument("-dis", "--distance", type=float, default='1.0',
                  metavar="<float>", help="Distance from start site to identify ")
    p.add_argument("-sta", "--starting_site", type=float, default='1.0',
             metavar="<float>", help="Distance from start site to identify ")
    p.add_argument("-ls", "--ligand_start", help="Ligand in which you want to measure your distance from")
    p.add_argument('-output')
    p.add_argument('-RMSD_file')
    args = parser.parse_args()
    main(args.PDB_name, args.output, args.RMSD_file)
    
