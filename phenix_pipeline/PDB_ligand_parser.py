#!/usr/bin/env python
#last edited: 2019-05-08
#last edited by: Stephanie Wankowicz

#PDB Parser to identify 'drug like' ligand

import pandas as pd
import os
import datetime
import argparse
import sys
from biopandas.pdb import PandasPdb
from Bio.PDB import *


def get_lig_name(PDB,lig_list): #load in PDB
    #print(PDB)
    ppdb = PandasPdb()
    #structure = parser.get_structure(PDB, PDB+'.pdb')
    ppdb.read_pdb(PDB+'.pdb')
    HETATM=ppdb.df['HETATM']
    residue_names = set(HETATM['residue_name'])
    lig_res_number = 0
    atoms = 0 #base number of atoms for a ligand
    all_ligands=[]
    _lig_name = ''
    for i in residue_names:
        all_ligands.append(i)
        if i in set(lig_list['Lig_name']):
            continue
        else:
            subset=(ppdb.df['HETATM']['residue_name']==i)
            lig_res_nubmer = subset.values.sum()
            if lig_res_number >= atoms:
              _lig_name = i
              atoms = lig_res_nubmer
            else:
              continue
    
    #removing HOH from restrained ligand list
    all_ligands.remove('HOH')
    with open('ligand_name.txt', 'w') as file:
        file.write(_lig_name)
    with open('ligand_list.txt', 'w') as file:
        for i in range(0,len(all_ligands)):
            file.write('resname ' + str(all_ligands[i]) + ' or ')
    return _lig_name

def main(PDB, lig_list):
    ligand_list = pd.read_csv(lig_list)
    get_lig_name(PDB, ligand_list)
    sys.exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('PDB_name')
    parser.add_argument('lig_remove', help='Text File of ligands to remove')
    args = parser.parse_args()
    main(args.PDB_name, args.lig_remove)
