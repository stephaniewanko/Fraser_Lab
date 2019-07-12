#!/usr/bin/env python
#last edited: 5-23-2018
#last edited by: Stephanie Wankowicz
'''
for pdbs with ensemble refinement and qfit done, we are going to collect some metrics
'''
#packages
import numpy as np
import pandas as pd
import os
import re
import csv
from argparse import ArgumentParser


def parse_args():
    p = ArgumentParser(description=__doc__)
    p.add_argument("--ligand") #cat ligand.txt
    p.add_argument("--average_conf_org") #
    p.add_argument("--average_conf_qfit")
    p.add_argument("--pdb_name")
    p.add_argument("--num_res")
    p.add_argument("--refine_log")
    p.add_argument("--ens_refine_log")
    p.add_argument("--pdb_num")
    args = p.parse_args()
    return args

#number of models


def create_table(count, pdb, ligand, num_res, org_mutli_atoms, org_num_multi, qfit_mutli_atoms, qfit_num_multi, refine, ens_refine):
    combined_df.loc[count,'PDB_name'] = pdb #combined_df is a global variable
    combined_df.loc[count,'Ligand'] = ligand
    combined_df.loc[count,'Num_Residues'] = num_res
    combine_df.loc[count, 'Num_Atoms_Multi_Org'] = org_multi_atoms
    combine_df.loc[count, 'Num_Multi_Org'] = org_num_multi
    combine_df.loc[count, 'Num_Atoms_Multi_Qfit'] = qfit_multi_atoms
    combine_df.loc[count, 'Num_Multi_Qfit'] = qfit_num_multi
    combine_df.loc[count, 'Num_Residue'] = num_res
    refine_log=pd.read_csv(refine)
    print(refine_log)
    ens_ref_log=pd.read_csv(ens_refine)
    print(ens_ref_log)
    print(combined_df)
    #combined_df = pd.concat([combined_df, refine_log, ens_ref_log], axis=1, join_axes=[combined_df.index])
    combined_df = combined_df.merge(refine_log, left_on='PDB_name', right_on='PDB')
    combined_df = combined_df.merge(ens_ref_log, left_on='PDB_name', right_on='PDB')
    print(combined_df)
    final_df = final_df.append(combined_df, ignore_index=True)
    final_df.to_csv('/wynton/home/fraserlab/swankowicz/190503_Targets/summary_table.csv', index=False)
    print(final_df)
    return combined_df

def parse_qfit_summary(file):
    print(file)
    sum = pd.read_csv(file, sep=' ', header=None) #take this in as an arguement
    all_atoms = float(sum.loc[0,0])
    subset_atoms = float(sum.loc[1,0])
    num_multi = sum.loc[2,0]
    multi_atoms = all_atoms - subset_atoms
    return multi_atoms, num_multi

def main():
    args = parse_args()
    print('I am here')
    org_mutli_atoms, org_num_multi=parse_qfit_summary(args.average_conf_org)
    qfit_mutli_atoms, qfit_num_multis=parse_qfit_summary(args.average_conf_qfit)
    print('Creating Table')
    create_table(count=args.pdb_num, pdb=args.pdb_name, ligand=args.ligand, num_res=args.num_res, org_mutli_atoms=org_mutli_atoms, org_num_multi=org_num_multi, qfti_mutli_atoms=qfti_mutli_atoms, qfit_num_multi=qfit_num_multi, refine=args.refine_log, ens_refine=args.ens_refine_log)


if __name__ == '__main__':
    #try:
    #    combined_df=pd.read_csv('/wynton/home/fraserlab/swankowicz/190503_Targets/summary_table.csv')
    #except OSError:
    combined_df=pd.DataFrame()
    print(combined_df)
    main()
    print(combined_df)

