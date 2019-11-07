#find differences between 2 PDB files
#Stephanie Wankowicz
#19-11-07

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
for model in pdb_obj1.hierarchy.models():
  print(model)
  for chain in model.chains():
    for res in chain.residue_groups():
      for ag in res.atom_groups():
        if res.atom_groups()[0].resname not in aa_resnames: continue
        else:
          #print(res.resseq)
          #print(ag.resname)
          #print(chain.id)
          residue = (chain.id, ag.resname, res.resseq)
          pdb_1_res.append(residue)


for model in pdb_obj2.hierarchy.models():
  for chain in model.chains():
    for res in chain.residue_groups():
      for ag in res.atom_groups():
         if res.atom_groups()[0].resname not in aa_resnames: continue
         else:
           residue = (chain.id, ag.resname, res.resseq)
         if residue in pdb_1_res:
            continue
         else:
            print(residue)
      #else:
         #print(rg.atom_groups()[0].resname)
