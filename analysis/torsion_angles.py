#!/usr/bin/env python
#last edited: 5-22-2019
#last edited by: Stephanie Wankowicz
#get psi/phi angles

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

args = parse_args()

#phi_psi_angles_fin = pd.DataFrame()
phi_psi_angles = pd.DataFrame()
phi_psi_anlges = []
AA_sequence = []
for model in Bio.PDB.PDBParser().get_structure(args.pdb_name, args.pdb):
    for chain in model:
        poly = Bio.PDB.Polypeptide.Polypeptide(chain)
        print(poly)
        phi_psi_angles = poly.get_phi_psi_list()
        AA_sequence = poly.get_sequence()
        #print(phi_psi_angles)
        print(type(AA_sequence))
        phi_psi_angles['AA'] = list(AA_sequence)
        phi_psi_angles['Angle'] = list(phi_psi_anlges)
    phi_psi_angles[['Phi_Angle', 'Psi_Angle']] = pd.DataFrame(phi_psi_angles['Angle'].tolist(), index=phi_psi_angles.index)
    phi_psi_angles['Residue_Number'] = phi_psi_angles.index + 1
    phi_psi_angles['PDB_name'] = args.pdb_name
    #phi_psi_angles_fin.append(phi_psi_angles)
        #rmsf['resseq'] = rmsf['resseq'].str.replace('[', '')
#print(type(phi_psi_angles.loc[1][1]))
    print(phi_psi_angles)
#print(phi_psi_angles_fin)
    phi_psi_angles.to_csv(args.pdb_name+'_'+model+'_phi_psi_angles.csv')
