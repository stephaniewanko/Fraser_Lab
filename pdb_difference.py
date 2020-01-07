#find differences between 2 PDB files
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

pdb1 = sys.argv[1]
pdb2 = sys.argv[2]


pdb_obj1 = iotbx.pdb.hierarchy.input(file_name=pdb1)
pdb_obj2 = iotbx.pdb.hierarchy.input(file_name=pdb2)

pdb_1_res = []
pdb1_res_location = {}
for model in pdb_obj1.hierarchy.models():
  print(model.id)
  for chain in model.chains():
    for res in chain.residue_groups():
      for ag in res.atom_groups():
        if res.atom_groups()[0].resname not in aa_resnames: continue
        else:
          for atom in ag.atoms():
          #print(res.resseq)
          #print(ag.resname)
          #print(chain.id)
           #print(atom.xyz)
           residue_atom = (model.id, chain.id, ag.resname, res.resseq, atom.name)
           pdb1_res_location[residue_atom] = atom.xyz
           pdb_1_res.append(residue_atom)

print(pdb1_res_location)
pdb2_res_location = {}
for model in pdb_obj2.hierarchy.models():
  for chain in model.chains():
    for res in chain.residue_groups():
      for ag in res.atom_groups():
         if res.atom_groups()[0].resname not in aa_resnames: continue
         else:
           for atom in ag.atoms():
             residue_atom2 = (model.id, chain.id, ag.resname, res.resseq, atom.name)
             pdb2_res_location[residue_atom2] = atom.xyz

for k,v in pdb1_res_location.items():
     if k in pdb2_res_location:
        print(match)
     else:
        print(pdb2_res_location[v])
