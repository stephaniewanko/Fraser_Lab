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

print(sys.version_info)

def main(PDB, output, RMSD):
    #try else:
    main_df=pd.read_csv('/wynton/home/fraserlab/swankowicz/190430_Apo_Lig_Pairs/multi_res_summary.csv')
    print(main_df)
    summary_df=pd.DataFrame(columns=['PDB','Date', 'Percent_Multi_Conf', 'Num_Atom_Multi', 'Num_Multi_Res'])
    now = datetime.datetime.now()
    file=pd.read_csv(output, sep=' ', header=None) #take this in as an arguement
    print('this is the output file:')
    print(file)
    all_atoms = float(file.loc[0,0])
    subset_atoms = float(file.loc[1,0])
    per_multi = file.loc[2,0]
    print(all_atoms)
    file2=pd.read_csv(RMSD, header=None, sep=' ', names=['Residue', 'Chain', 'Per', 'Num_Conf'])
    subset=(file2.loc[file2['Num_Conf'] == 2])
    multi_conf=len(subset.index)
    summary_df.loc[1,'PDB']=PDB
    summary_df.loc[1,'Date']=now
    print(per_multi)
    summary_df.loc[1,'Percent_Multi_Conf']=per_multi
    print(all_atoms-subset_atoms)
    summary_df.loc[1,'Num_Atom_Multi']=(all_atoms-subset_atoms)
    print(multi_conf)
    summary_df.loc[1,'Multi_Res']=multi_conf
    main_df=main_df.append(summary_df)
    main_df.to_csv('/wynton/home/fraserlab/swankowicz/190430_Apo_Lig_Pairs/multi_res_summary.csv', index=False)




if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('-PDB','--PDB_name')
    args = p.parse_args()
    main(args.PDB_name, 'summary_output.txt', 'ind_rmsd_output.txt')
