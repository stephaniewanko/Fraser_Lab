#Edited by Stephanie Wankowicz
#began: 2019-05-01
'''
Excited States software: qFit 3.0

Contributors: Saulo H. P. de Oliveira, Gydo van Zundert, Henry van den Bedem, Stephanie Wankowicz
Contact: vdbedem@stanford.edu
'''

import pkg_resources  # part of setuptools
from .qfit import QFitRotamericResidue, QFitRotamericResidueOptions
from .qfit import QFitSegment, QFitSegmentOptions
from .qfit import print_run_info
from .qfit_protein import QFitProteinOptions, QFitProtein
import multiprocessing as mp
import os.path
import os
import sys
import time
import copy
import numpy as np
import pandas as pd
from argparse import ArgumentParser
from math import ceil
from . import MapScaler, Structure, XMap
from .structure.base_structure import _BaseStructure


os.environ["OMP_NUM_THREADS"] = "1"

def parse_args():
    p = ArgumentParser(description=__doc__)
    p.add_argument("structure", type=str,
                   help="PDB-file containing structure.")

    # Map prep options
    p.add_argument("-ns", "--no-scale", action="store_false", dest="scale",
            help="Do not scale density.")
    p.add_argument("-dc", "--density-cutoff", type=float, default=0.3, metavar="<float>",
            help="Densities values below cutoff are set to <density_cutoff_value")
    p.add_argument("-dv", "--density-cutoff-value", type=float, default=-1, metavar="<float>",
            help="Density values below <density-cutoff> are set to this value.")

    # Output options
    p.add_argument("-d", "--directory", type=os.path.abspath, default='.',
                   metavar="<dir>", help="Directory to store results.")
    p.add_argument("--debug", action="store_true",
                   help="Write intermediate structures to file for debugging.")
    p.add_argument("-v", "--verbose", action="store_true",
                   help="Be verbose.")
    p.add_argument("--pdb", help="Name of the input PDB.")

    #new RMSF arguments
    args = p.parse_args()
    return args

class num_res_options(QFitRotamericResidueOptions, QFitSegmentOptions):
    def __init__(self):
        super().__init__()
        self.nproc = 1
        self.verbose = True
        self.omit = False
        self.pdb = None



class number_residues():
    def __init__(self, structure, options):
        self.structure = structure #PDB with HOH at the bottom
        self.options = options #user input
    def run(self):
        if not self.options.pdb==None:
            self.pdb=self.options.pdb+'_'
        else:
            self.pdb=''
        self.num_residues()


    def num_residues(self):
        select = self.structure.extract('record', 'ATOM', '==')
        num_residues=[]
        n=0
        for chain in np.unique(select.chain):
            select2=select.extract('chain', chain, '==')
            print(max(select2.resi))
            num_residues.append(max(select2.resi))
        print(num_residues)
        tot_res=sum(num_residues)
        print(tot_res)
        with open(self.pdb+'num_residues.txt', 'w') as file:
            file.write(str(tot_res))


def main():
    args = parse_args()
    try:
        os.mkdir(args.directory)
    except OSError:
        pass
    structure = Structure.fromfile(args.structure).reorder()
    R_options = num_res_options()
    R_options.apply_command_args(args)

    time0 = time.time()
    num_resn = number_residues(structure, R_options)
    num_resn.run()
