#!/usr/bin/env python
#last edited: 2019-04-09
#last edited by: Stephanie Wankowicz
#07-12-2019

import pandas as pd
import os
import datetime
import argparse
import sys
import re


def create_table(log_file,time,PDB):
    now = datetime.datetime.now()
    bonds=''
    for i, line in enumerate(log_file):
        if i == 41: #this is the bond line for selection
            bonds = line
            print(line)
        elif i == 42:
            angles = line
            print(line)
        elif i == 43:
            dihedral = line
            print(line)
        elif i == 44:
            break
    ligand_geo_df.loc[1,'PDB']=PDB
    print(bonds)
    print(bonds.split(')'))
    ligand_geo_df.loc[1,'%s%s' % (time, '_z_bond_all')] = float(bonds.split(')')[3][3:8])
    ligand_geo_df.loc[1,'%s%s' % (time, '_z_bond_none')] = float(bonds.split(')')[4][3:8])
    ligand_geo_df.loc[1,'%s%s' % (time, '_z_bond_alt')] = float(bonds.split(')')[5][3:8])
    ligand_geo_df.loc[1,'%s%s' % (time, '_z_angle_all')] = float(angles.split(')')[3][3:8])
    ligand_geo_df.loc[1,'%s%s' % (time, '_z_angle_none')] = float(angles.split(')')[4][3:8])
    ligand_geo_df.loc[1,'%s%s' % (time, '_z_angle_alt')] = float(angles.split(')')[5][3:8])
    ligand_geo_df.loc[1,'%s%s' % (time, '_z_di_all')] = float(dihedral.split(')')[3][3:8])
    ligand_geo_df.loc[1,'%s%s' % (time, '_z_di_none')] = float(dihedral.split(')')[4][3:8])
    ligand_geo_df.loc[1,'%s%s' % (time, '_z_di_alt')] = float(dihedral.split(')')[5][3:8])
    ligand_geo_df.loc[1,'Date']=now.strftime("%Y-%m-%d")
    return ligand_geo_df


#parse refinement output .log
def parse_lig_refine_log(pre_refine, post_refine, PDB):
    pre_refine = open(pre_refine, 'r') #take this in as an arguement #columns=['PDB','Starting_Z_All', 'Starting_Z_None', 'Starting_Z_Alt', 'Ending_Z_All', 'Ending_Z_None', 'Ending_Z_Alt'])
    global ligand_geo_df
    ligand_geo_df = pd.DataFrame()
    create_table(pre_refine,'start', PDB)
    post_refine = open(post_refine, 'r')
    print('starting post refine')
    create_table(post_refine, 'post_ref', PDB)
    ligand_geo_df.loc[1,'Difference_Bond']=(ligand_geo_df.loc[1,'start_z_bond_all']-ligand_geo_df.loc[1,'post_ref_z_bond_all'])
    ligand_geo_df.loc[1,'Difference_Angle']=(ligand_geo_df.loc[1,'start_z_angle_all']-ligand_geo_df.loc[1,'post_ref_z_angle_all'])
    ligand_geo_df.loc[1,'Difference_Di']=(ligand_geo_df.loc[1,'start_z_di_all']-ligand_geo_df.loc[1,'post_ref_z_di_all'])
    print(ligand_geo_df)
    return ligand_geo_df


def main(pre,post,PDB):
    ligand_geo_df = parse_lig_refine_log(pre,post,PDB)
    output_name = PDB+'_ligand_verification.csv'
    ligand_geo_df.to_csv(output_name, index=False)
    sys.exit(0)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('-pre_refine')
    p.add_argument('-post_refine')
    p.add_argument('-PDB')
    args = p.parse_args()
    main(args.pre_refine, args.post_refine, args.PDB)
