
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
    p.add_argument("-qFit", type=str)
    #p.add_argument("-b", type=str, help="B-factor csv file")
    #p.add_argument("-r", type=str, help="RMSF csv file")
    #p.add_argument("-i", type=str, help="baseline_ind")
    args = p.parse_args()
    return args


def main():
    args = parse_args()
    if not args.qFit == None:
            qFit = '_qFit'
    else:
            qFit = ''
    rmsd = None
    B_factor = None
    sasa = None
    rotamer = None
    
    try:
        rmsd = pd.read_csv(args.PDB + qFit + "_ind_baseline_rmsd_output.txt", sep=" ", header=None)
        rmsd.columns = ['resid','chain','rmsd','alt_loc']
    except IOError:
        pass
    
    try:
        B_factor = pd.read_csv(args.PDB + qFit + "_B_factors.csv")
        #B_factor['AA'] = B_factor.AA.str.replace('[','')
        #B_factor['AA'] = B_factor.AA.str.replace(']','')
        #B_factor['Chain'] = B_factor.Chain.str.replace(']','')
        #B_factor['Chain'] = B_factor.Chain.str.replace('[','')
        #B_factor['resseq'] = B_factor.resseq.str.replace('[','')
        #B_factor['resseq'] = B_factor.resseq.str.replace(']','')
        #B_factor['Chain'] = B_factor.Chain.str.replace("\'", '')
        #B_factor['resseq'] = B_factor['resseq'].astype(int)
    except IOError:
        pass
    
    try:
    	sasa = pd.read_csv(args.PDB + "_sasa.csv", index_col=0)
    except IOError:
        pass
    
    try:
        rmsf = pd.read_csv(args.PDB + qFit + "_qfit_RMSF.csv")
    except IOError:
        pass
    
    try:
        rotamer = pd.read_csv(args.PDB + qFit + "_rotamer_output.txt", sep = ':')
        print(rotamer.head())
        split = rotamer['residue'].str.split(" ") 
        for i in range(0,len(rotamer.index)-1):
            rotamer.loc[i,'chain'] = split[i][1]
            STUPID = str(rotamer.loc[i,'residue'])[3:8]
            rotamer.loc[i,'resi'] = [int(s) for s in STUPID.split() if s.isdigit()]
    except IOError:
        pass
    
    close_res = pd.read_csv(args.PDB + "_5.0_closeresidue.txt", header=None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.show_dimensions', False)

    close_res.columns = ['chain', 'resid']
    #rmsd.columns = ['resid','chain','rmsd','alt_loc']  
    if B_factor is not None:
        B_factor['AA'] = B_factor.AA.str.replace('[','')
        B_factor['AA'] = B_factor.AA.str.replace(']','')
        B_factor['Chain'] = B_factor.Chain.str.replace(']','')
        B_factor['Chain'] = B_factor.Chain.str.replace('[','')
        B_factor['resseq'] = B_factor.resseq.str.replace('[','')
        B_factor['resseq'] = B_factor.resseq.str.replace(']','')
        B_factor['Chain'] = B_factor.Chain.str.replace("\'", '')
        B_factor['resseq'] = B_factor['resseq'].astype(int)

    li_rmsd = []
    li_b = []
    li_rmsf = []
    li_r = []
    li_sasa = []
    li_rotamer = []
    
    for i in close_res.chain.unique():
        output = close_res[close_res['chain']==i]
        residue = output.resid.unique()
        rmsf_s = rmsf[(rmsf['Chain'] == i) & (rmsf['resseq'].isin(residue))]
        li_rmsf.append(rmsf_s)

        rmsd_s = rmsd[(rmsd['chain'] == i) & (rmsd['resid'].isin(residue))]
        li_rmsd.append(rmsd_s)
        if B_factor is not None:
          b_s = B_factor[(B_factor['Chain'] == i) & (B_factor['resseq'].isin(residue))]
          li_b.append(b_s)
        rot_s = rotamer[(rotamer['chain'] == i) & (rotamer['resi'].isin(residue))]
        li_rotamer.append(rot_s)
        sasa_s = sasa.loc[(sasa['chain'] == i) & (sasa['resnum'].isin(residue))]
        li_sasa.append(sasa_s)

    rmsf_subset = pd.concat(li_rmsf, axis=0, ignore_index=True)
    rmsd_subset = pd.concat(li_rmsd, axis=0, ignore_index=True)
    if B_factor is not None:
       b_factor_subset = pd.concat(li_b, axis=0, ignore_index=True)
       b_factor_subset.to_csv(args.PDB + '_' + args.dist + '_bfactor_subset.csv', index=False)
    rotamer_subset = pd.concat(li_rotamer, axis=0, ignore_index=True)
    sasa_subset = pd.concat(li_sasa, axis=0, ignore_index=True)
    rmsf_subset.to_csv(args.PDB + '_' + args.dist + '_rmsf_subset.csv', index=False)   
    rmsd_subset.to_csv(args.PDB + '_' + args.dist + '_rmsd_num_altloc_subset.csv', index=False) 
    #b_factor_subset.to_csv(args.PDB + '_' + args.dist + '_bfactor_subset.csv', index=False)
    rotamer_subset.to_csv(args.PDB + '_' + args.dist + '_rotamer_subset.csv', index=False)
    sasa_subset.to_csv(args.PDB+ '_' + args.dist + '_sasa_subset.csv', index=False)

main()
