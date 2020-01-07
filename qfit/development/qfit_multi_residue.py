#Edited by Stephanie Wankowicz
#began: 2019-04-10
#last edited: 2019-04-22
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
from argparse import ArgumentParser
from math import ceil
from . import MapScaler, Structure, XMap
from .structure.base_structure import _BaseStructure
#from .structure.ligand import
#from .structure,.residue import residue_type


os.environ["OMP_NUM_THREADS"] = "1"

def parse_args():
    p = ArgumentParser(description=__doc__)
    p.add_argument("map", type=str,
                   help="Density map in CCP4 or MRC format, or an MTZ file "
                        "containing reflections and phases. For MTZ files "
                        "use the --label options to specify columns to read.")
    p.add_argument("structure", type=str,
                   help="PDB-file containing structure.")

    # Map input options
    p.add_argument("-l", "--label", default="FWT,PHWT", metavar="<F,PHI>",
                   help="MTZ column labels to build density.")
    p.add_argument('-r', "--resolution", type=float, default=None, metavar="<float>",
            help="Map resolution in angstrom. Only use when providing CCP4 map files.")
    p.add_argument("-m", "--resolution_min", type=float, default=None, metavar="<float>",
            help="Lower resolution bound in angstrom. Only use when providing CCP4 map files.")
    p.add_argument("-z", "--scattering", choices=["xray", "electron"], default="xray",
            help="Scattering type.")
    p.add_argument("-rb", "--randomize-b", action="store_true", dest="randomize_b",
            help="Randomize B-factors of generated conformers.")
    p.add_argument('-o', '--omit', action="store_true",
            help="Map file is an OMIT map. This affects the scaling procedure of the map.")

    # Map prep options
    p.add_argument("-ns", "--no-scale", action="store_false", dest="scale",
            help="Do not scale density.")
    p.add_argument("-dc", "--density-cutoff", type=float, default=0.3, metavar="<float>",
            help="Densities values below cutoff are set to <density_cutoff_value")
    p.add_argument("-dv", "--density-cutoff-value", type=float, default=-1, metavar="<float>",
            help="Density values below <density-cutoff> are set to this value.")

    # Sampling options
    p.add_argument('-bb', "--backbone", dest="sample_backbone", action="store_true",
            help="Sample backbone using inverse kinematics.")
    p.add_argument('-bbs', "--backbone-step", dest="sample_backbone_step",
                   type=float, default=0.1, metavar="<float>",
                   help="Sample N-CA-CB angle.")
    p.add_argument('-bba', "--backbone-amplitude", dest="sample_backbone_amplitude",
                   type=float, default=0.3, metavar="<float>",
                   help="Sample N-CA-CB angle.")
    p.add_argument('-sa', "--sample-angle", dest="sample_angle", action="store_true",
            help="Sample N-CA-CB angle.")
    p.add_argument('-sas', "--sample-angle-step", dest="sample_angle_step",
                   type=float, default=3.75, metavar="<float>",
                   help="Sample N-CA-CB angle.")
    p.add_argument('-sar', "--sample-angle-range", dest="sample_angle_range",
                   type=float, default=7.5, metavar="<float>",
                   help="Sample N-CA-CB angle.")
    p.add_argument("-b", "--dofs-per-iteration", type=int, default=2, metavar="<int>",
            help="Number of internal degrees that are sampled/build per iteration.")
    p.add_argument("-s", "--dofs-stepsize", type=float, default=6, metavar="<float>",
            help="Stepsize for dihedral angle sampling in degree.")
    p.add_argument("-rn", "--rotamer-neighborhood", type=float,
            default=60, metavar="<float>",
            help="Neighborhood of rotamer to sample in degree.")
    p.add_argument("--no-remove-conformers-below-cutoff", action="store_false",
                   dest="remove_conformers_below_cutoff",
                   help=("Remove conformers during sampling that have atoms "
                         "that have no density support for, ie atoms are "
                         "positioned at density values below cutoff value."))
    p.add_argument('-cf', "--clash_scaling_factor", type=float, default=0.75, metavar="<float>",
            help="Set clash scaling factor. Default = 0.75")
    p.add_argument('-ec', "--external_clash", dest="external_clash", action="store_true",
            help="Enable external clash detection during sampling.")
    p.add_argument("-bs", "--bulk_solvent_level", default=0.3, type=float,
                   metavar="<float>", help="Bulk solvent level in absolute values.")
    p.add_argument("-c", "--cardinality", type=int, default=5, metavar="<int>",
                   help="Cardinality constraint used during MIQP.")
    p.add_argument("-t", "--threshold", type=float, default=0.2,
                   metavar="<float>", help="Treshold constraint used during MIQP.")
    p.add_argument("-hy", "--hydro", dest="hydro", action="store_true",
                   help="Include hydrogens during calculations.")
    p.add_argument("-M", "--miosqp", dest="cplex", action="store_false",
                   help="Use MIOSQP instead of CPLEX for the QP/MIQP calculations.")
    p.add_argument("-T", "--threshold-selection", dest="bic_threshold",
                   action="store_true", help="Use BIC to select the most parsimonious MIQP threshold")
    p.add_argument("-p", "--nproc", type=int, default=1, metavar="<int>",
                   help="Number of processors to use.")

    # Output options
    p.add_argument("-d", "--directory", type=os.path.abspath, default='.',
                   metavar="<dir>", help="Directory to store results.")
    p.add_argument("--debug", action="store_true",
                   help="Write intermediate structures to file for debugging.")
    p.add_argument("-v", "--verbose", action="store_true",
                   help="Be verbose.")


    #new multiresidue arguments
    p.add_argument("-dis", "--distance", type=float, default='1.0',
                  metavar="<float>", help="Distance from start site to identify ")
    p.add_argument("-sta", "--starting_site", type=float, default='1.0',
             metavar="<float>", help="Distance from start site to identify ")
    p.add_argument("-ls", "--ligand_start", help="Ligand in which you want to measure your distance from")
    args = p.parse_args()
    return args


class _Counter:
    """Thread-safe counter object to follow progress"""
    def __init__(self):
        self.val = mp.RawValue('i', 0)
        self.lock = mp.Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    def value(self):
        with self.lock:
            return self.val.value


class QFitMultiResOptions(QFitRotamericResidueOptions, QFitSegmentOptions):
    def __init__(self):
        super().__init__()
        self.nproc = 1
        self.verbose = True
        self.omit = False
        self.ligand_start = None
        self.distance = None

class QFitMultiResidue:
    def __init__(self, structure, xmap, options):
        self.xmap = xmap #user input
        self.structure = structure #PDB with HOH at the bottom
        self.options = options #user input

    def run(self):
        lig_strucutre= self.select_lig()
        substructure=self.select_close_residues()
        return substructure

    def select_lig(self):
        '''
        Select the residue IDs of the ligands you want to extract; get a central value of all atoms in that ligand
        '''
        #first we are going to check which resiudes are ligands
        #lig_list=Structure.residue.residue_type(structure)
        #print('lig:')
        #print(self.options.ligand_start)
        #hetatms = self.structure.extract('record', 'HETATM', '==')
        lig_structure=self.structure.extract('resn', self.options.ligand_start) #
        #calculate center distance structure.residue.calc_coordinates
        atoms=len(lig_structure.name)
        #print(atoms)
        center_x=np.mean(lig_structure.coor[:][0])
        center_y=np.mean(lig_structure.coor[:][1])
        center_z=np.mean(lig_structure.coor[:][2])
        self.lig_center=[center_x,center_y,center_z]
        print(self.lig_center)
        return lig_structure

    def select_close_residues(self):
        print(self.lig_center)
        self.atoms = self.structure.extract('record', 'ATOM', '==')
        print(self.atoms)
        print(len(self.atoms.name))
        #print(self.atoms.coor[:][:])
        dist=np.linalg.norm(self.atoms.coor[:][:]-self.lig_center, axis=1)
        mask = dist < self.options.distance
        sel_residue=self.atoms.resi[mask]
        sel_chain=self.atoms.chain[mask]
        print(sel_chain)
        print(sel_residue)
        for chain in set(sel_chain):
            mask2 = sel_chain == chain
            sel_residue2 = sel_residue[mask2]
            print(sel_residue2)
            for residue in sel_residue2:
                try:
                    res_atoms=self.atoms.extract(f'chain {chain} and resi {residue}')
                    close_atoms_chain=close_atoms_chain.combine(res_atoms)
                    print(close_atoms_chain)
                except NameError:
                    close_atoms_chain=self.atoms.extract(f'chain {chain} and resi {residue}')
                    print(close_atoms_chain)
        self.close_atoms_chain=close_atoms_chain
        #print(self.close_atoms_chain)
        return self.close_atoms_chain


def main():
    args = parse_args()
    print(args)
    try:
        os.mkdir(args.directory)
    except OSError:
        pass
    # Load structure and prepare it
    structure = Structure.fromfile(args.structure).reorder() #put H20 on the bottom
    print(structure)
    if not args.hydro:
        structure = structure.extract('e', 'H', '!=')
    options_multi= QFitMultiResOptions()
    options_multi.apply_command_args(args)

    xmap = XMap.fromfile(args.map, resolution=args.resolution,
                         label=args.label)
    xmap = xmap.canonical_unit_cell()

    time0 = time.time()
    qfit=QFitMultiResidue(structure, xmap, options_multi)
    substructure = qfit.run()
    print(substructure)

    options = QFitProteinOptions()
    options.apply_command_args(args)
    qfit_prot=QFitProtein(substructure, xmap, options)
    multiconformer = qfit_prot.run()

    print(f"Total time: {time.time() - time0}s")
