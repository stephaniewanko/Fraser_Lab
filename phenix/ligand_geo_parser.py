!/usr/bin/env python
#last edited: 2019-04-09
#last edited by: Stephanie Wankowicz

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
        if i == 40: #this is the bond line for selection
            bonds = line
            print(line)
        elif i == 41:
            angles = line
            print(line)
        elif i == 42:
            dihedral = line
            print(line)
        elif i == 45:
            break
    ligand_geo_df.loc[1,'PDB']=PDB
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
