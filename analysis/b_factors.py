#!/usr/bin/env python
#last edited: 5-28-2019
#last edited by: Stephanie Wankowicz
#get and plot B-factors

#packages
import numpy as np
import pandas as pd
import os
import re
import csv
import Bio.PDB
import argparse

def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pdb") #cat ligand.txt
    p.add_argument("--pdb_name")
    args = p.parse_args()

args = parse_args()
B_factor = pd.DataFrame()
atom_name = []
chain_ser = []
residue_name = []
b_factor = []
residue_num = []
model = []
parser = Bio.PDB.PDBParser()
print(args.pdb_name)
print(args.pdb)
for model in parser.get_structure(args.pdb_name, args.pdb):
    print(model)
    for chain in model.get_list():
        for residue in chain.get_list():
            for atom in residue.get_list():
                print(type(atom.get_name()))
                modle.append(mdoel.get_name())
                atom_name.append(atom.get_name())
                chain_ser.append(chain.get_id())
                residue_name.append(residue)
                residue_num.append(residue.get_full_id()[3][1])
                b_factor.append(atom.get_bfactor())
                n=+1

B_factor['Atom'] = atom_name
B_factor['Chain'] = chain_ser
B_factor['residue'] = residue_name
B_factor['residue_num'] = residue_num
B_factor['B_factor'] = b_factor
B_factor['PDB_name'] = args.pdb_name
B_factor.to_csv(args.pdb_name+'B_factors.csv')
