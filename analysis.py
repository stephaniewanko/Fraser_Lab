#Baseline Analysis
#Stephanie Wankowicz
#4/30/2019
#git: 07-12-2019

#packages
import numpy as np
import pandas as pd
import os
import datetime
import argparse
import sys

print(sys.version_info)

def main(PDB, output, RMSD, ah, qfit, dis):
    #try else:
    main_df=pd.read_csv('/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/multi_res_summary2.csv')
    print(main_df)
    summary_df=pd.DataFrame(columns=['PDB','Date', 'Percent_Multi_Conf', 'Num_Atom_Multi', 'Num_Multi_Res', 'AH','qfit', 'distance'])
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
    summary_df.loc[1,'AH']=ah
    summary_df.loc[1,'qfit']=qfit
    summary_df.loc[1,'distance']=dis
    print(per_multi)
    summary_df.loc[1,'Percent_Multi_Conf']=per_multi
    print(all_atoms-subset_atoms)
    summary_df.loc[1,'Num_Atom_Multi']=(all_atoms-subset_atoms)
    print(multi_conf)
    summary_df.loc[1,'Multi_Res']=multi_conf
    main_df=main_df.append(summary_df)
    main_df.to_csv('/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/multi_res_summary2.csv', index=False)




if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('-PDB','--PDB_name')
    p.add_argument('-sum', '--summary_output_file')
    p.add_argument('-ind', '--individual_output_file')
    p.add_argument('-h_a', '--holo_or_apo')
    p.add_argument('-qfit', '--qfit_structure')
    p.add_argument('-dis', '--distance')
    args = p.parse_args()
    main(args.PDB_name, args.summary_output_file, args.individual_output_file, args.holo_or_apo, args.qfit_structure, args.distance)
