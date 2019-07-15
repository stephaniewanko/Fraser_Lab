!/usr/bin/env python
#last edited: 5-22-2019
#last edited by: Stephanie Wankowicz
#get psi/phi angles
#git: 07-12-2019

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
    p.add_argument("--pdb")
    p.add_argument("--pdb_name")
    args = p.parse_args()
    return args

#def main():
args = parse_args()
phi_psi_angles_fin = pd.DataFrame(columns=['Angles','AA', 'Residue_Number', 'Chain', 'Model'])
phi_psi_anlges = []
AA_sequence = []
for model in Bio.PDB.PDBParser(QUIET=True).get_structure(args.pdb_name, args.pdb):
    for chain in model:
        poly = Bio.PDB.Polypeptide.Polypeptide(chain)
        phi_psi_angles1 = poly.get_phi_psi_list()
        AA_sequence = poly.get_sequence()
        phi_psi_angles_tmp = pd.DataFrame()
        phi_psi_angles_tmp['Angles'] = list(phi_psi_angles1)
        phi_psi_angles_tmp['AA'] = list(AA_sequence)
        phi_psi_angles_tmp['Residue_Number'] = phi_psi_angles_tmp.index + 1
        phi_psi_angles_tmp['Chain'] = str(chain)[10:11]
        phi_psi_angles_tmp['Model'] = str(model)[10:12].replace(">", "")
        try:
            phi_psi_angles_fin = phi_psi_angles_fin.append(phi_psi_angles_tmp, ignore_index=True)
        except OSError:
            phi_psi_angles_fin = phi_psi_angles_tmp
phi_psi_angles_fin['PDB_name'] = args.pdb_name
model = str(model)[10:12].replace(">", "")
phi_psi_angles_fin=phi_psi_angles_fin[phi_psi_angles_fin['AA']!='X']
phi_psi_angles_fin.to_csv(args.pdb_name+'_'+model+'_phi_psi_angles.csv')
