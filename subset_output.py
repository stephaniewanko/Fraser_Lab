
import numpy as np
import pandas as pd
import argparse
import os
import sys

def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("PDB", type=str, help="name of PDB")
    p.add_argument("dist", type=str,
                   help="distance of close residues")
    #p.add_argument("-b", type=str, help="B-factor csv file")
    #p.add_argument("-r", type=str, help="RMSF csv file")
    #p.add_argument("-i", type=str, help="baseline_ind")
    args = p.parse_args()
    return args


def main():
    args = parse_args()
    try:
        rmsd = pd.read_csv(args.PDB + "_baseline_ind_rmsd_output.txt", sep=" ", header=None)
    except OSError:
        pass
    #rmsd = pd.read_csv(args.PDB + "_baseline_ind_rmsd_output.txt", sep=" ", header=None)
    try:
        B_factor = pd.read_csv(args.PDB + "_B_factors.csv")
    except OSError:
        pass
    try:
        rmsf = pd.read_csv(args.PDB + "_qfit_RMSF.csv")
    except OSError:
        pass
   # try:
   #     sasa = pd.read_csv(args.PDB + "_sasa.csv")
   # except OSError:
   #     pass
    #B_factor = pd.read_csv(args.PDB + "_B_factors.csv")
    #rmsf = pd.read_csv(args.PDB + "_qfit_RMSF.csv")
    close_res = pd.read_csv(args.PDB + "_5.0_closeresidue.txt", header=None)
    #sasa = pd.read_csv(args.PDB + "_sasa.csv")

    close_res.columns = ['chain', 'resid']
    rmsd.columns = ['resid','chain','rmsd','alt_loc']
    B_factor['AA'] = B_factor.AA.str.replace('[','')
    B_factor['AA'] = B_factor.AA.str.replace(']','')
    B_factor['Chain'] = B_factor.Chain.str.replace(']','')
    B_factor['Chain'] = B_factor.Chain.str.replace('[','')
    B_factor['resseq'] = B_factor.resseq.str.replace('[','')
    B_factor['resseq'] = B_factor.resseq.str.replace(']','')

    li_rmsd = []
    li_b = []
    li_rmsf = []
    li_r = []
    li_sasa = []

    for i in close_res.chain.unique():
        print(i)
        output = close_res[close_res['chain']==i]
        residue = output.resid.unique()
        print(residue)

        rmsf_s = rmsf[(rmsf['Chain'] == i) & (rmsf['resseq'].isin(residue))]
        li_rmsf.append(rmsf_s)

        rmsd_s = rmsd[(rmsd['chain'] == i) & (rmsd['resid'].isin(residue))]
        li_rmsd.append(rmsd_s)

        b_s = B_factor[(B_factor['Chain'] == i) & (B_factor['resseq'].isin(residue))]
        li_b.append(b_s)

        #sasa_s = sasa[(sasa['chain'] == i) & (sasa['resnum'].isin(residue))]
        #li_sasa.append(sasa_s)

    rmsf_subset = pd.concat(li_rmsf, axis=0, ignore_index=True)
    rmsd_subset = pd.concat(li_rmsd, axis=0, ignore_index=True)
    b_factor_subset = pd.concat(li_b, axis=0, ignore_index=True)
    #sasa_subset = pd.concat(li_sasa, axis=0, ignore_index=True)
    
    rmsf_subset.to_csv(args.PDB+ '_' + args.dist + '_rmsf_subset.csv', index=False)   
    rmsd_subset.to_csv(args.PDB+ '_' + args.dist + '_rmsd_num_altloc_subset.csv', index=False) 
    b_factor_subset.to_csv(args.PDB+ '_' + args.dist + '_bfactor_subset.csv', index=False)
    #sasa_subset.to_csv(args.PDB+ '_' + args.dist + '_sasa_subset.csv', index=False)

main()
