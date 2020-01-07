#determine if alt loc occupancies add up to 1
#Stephanie Wankowicz
#19-11-07
#run using phenix.python

from __future__ import division
import iotbx.pdb
import sys
import os
import math
import iotbx.pdb.amino_acid_codes

aa_resnames = iotbx.pdb.amino_acid_codes.one_letter_given_three_letter

pdb = sys.argv[1]
pdb_obj = iotbx.pdb.hierarchy.input(file_name=pdb)

def determine_occ(dict):
  if all(value == 1 for value in dict.values()):
     print('All occupancies are one')
  else:
     print(occ)
     return "Failed Occupancy"

occ = {}
for model in pdb_obj.hierarchy.models():
  for chain in model.chains():
    for res in chain.residue_groups():
      for ag in res.atom_groups():
        if res.atom_groups()[0].resname not in aa_resnames: continue
        else:
          for atom in ag.atoms():
            if atom.name == ' CB ':
              if atom.occ == 1: continue
              else:
                atom_name =  (chain.id, res.resseq, res.atom_groups()[0].resname)
                atom_name2 = "_".join(atom_name)
                if atom_name2 not in occ:
                   occ[atom_name2] = atom.occ
                else:
                   occ[atom_name2] = occ[atom_name2] + atom.occ

determine_occ(occ)
                 
