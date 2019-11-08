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

pdb1 = sys.argv[1]


pdb_obj1 = iotbx.pdb.hierarchy.input(file_name=pdb1)

pdb_1_res = []
for model in pdb_obj1.hierarchy.models():
  print(model)
  for chain in model.chains():
    for res in chain.residue_groups():
      for ag in res.atom_groups():
        if res.atom_groups()[0].resname not in aa_resnames: continue
        else:
          residue = (chain.id, ag.resname, res.resseq)
          if ag.atom.name == 'CA':
            print('alpha carbon')
