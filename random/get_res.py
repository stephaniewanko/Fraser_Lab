import os
import sys
from sys import stdout
import Bio
from Bio.PDB import PDBParser, PPBuilder, PDBIO


def get_res(pdb):
    pdb_parser = PDBParser(PERMISSIVE=0)                    # The PERMISSIVE instruction allows PDBs presenting errors.
    pdb_structure = pdb_parser.get_structure(pdb,pdb)
    print(pdb_structure.header['resolution'])

if __name__ == '__main__':
     get_res(sys.argv[1])
