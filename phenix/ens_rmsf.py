from __future__ import division
import iotbx.pdb
import sys
import os
import math
import iotbx.pdb.amino_acid_codes

aa_resnames = iotbx.pdb.amino_acid_codes.one_letter_given_three_letter

file_name = sys.argv[1]
pdb_obj = iotbx.pdb.hierarchy.input(file_name=file_name)
#n_models = len(pdb_obj.hierarchy.models()) -- deprecated in favor of atom_count[atom_name]

targ_atom_names_str = sys.argv[2]
targ_atom_names = []
for targ_atom_name in targ_atom_names_str.split(","):
  targ_atom_names.append(targ_atom_name)
print >> sys.stderr, "Calculating RMSF using these atoms:", " ".join(targ_atom_names)

assert sys.argv[3] in ['csv', 'pml']
output = sys.argv[3]

#if output == 'pml':
#  max_rmsf = float(sys.argv[3])

mean_xyz = {} # atom name --> xyz
atom_count = {} # atom name --> # of instances (multi-MODEL or alt confs)
for model in pdb_obj.hierarchy.models():
  for chain in model.chains():
    for rg in chain.residue_groups():
      if rg.atom_groups()[0].resname not in aa_resnames: continue
      for ag in rg.atom_groups():
        for atom in ag.atoms():
          if atom.name.strip() in targ_atom_names:
            atom_name = (chain.id, rg.resid(), atom.name.strip())
            if atom_name not in mean_xyz:
              mean_xyz[atom_name] = atom.xyz
              atom_count[atom_name] = 1
            else:
              mean_xyz[atom_name] = \
                tuple(i + j for i, j in zip(mean_xyz[atom_name], atom.xyz))
              atom_count[atom_name] = atom_count[atom_name] + 1

for atom_name in mean_xyz:
  xyz_sum = mean_xyz[atom_name]
  mean_xyz[atom_name] = tuple(i / atom_count[atom_name] for i in xyz_sum)
  #print atom_name, mean_xyz[atom_name]

rmsfs = {} # atom name --> dist
for model in pdb_obj.hierarchy.models():
  for chain in model.chains():
    for rg in chain.residue_groups():
      if rg.atom_groups()[0].resname not in aa_resnames: continue

      for ag in rg.atom_groups():
        for atom in ag.atoms():
          if atom.name.strip() not in targ_atom_names:
            continue
          atom_name = (chain.id, rg.resid(), atom.name.strip())
          xyz_pairs = zip(atom.xyz, mean_xyz[atom_name])
          sq_dist = sum((i - j)**2 for i, j in xyz_pairs)
          #print 'dist: %s' % math.sqrt(sq_dist)
          if atom_name not in rmsfs:
            rmsfs[atom_name] = sq_dist
          else:
            rmsfs[atom_name] = rmsfs[atom_name] + sq_dist
            
max_rmsf = max(rmsfs.values())
if len(sys.argv) > 4:
  max_rmsf = float(sys.argv[4])

for atom_name in rmsfs:
  sq_dist_sum = rmsfs[atom_name]
  rmsf = math.sqrt(sq_dist_sum / atom_count[atom_name])
  rmsfs[atom_name] = rmsf

file_basename = os.path.basename(file_name).split('.pdb')[0]
if output == 'csv':
  print 'dataset,chain,resseq,rmsf'
for atom_name in sorted(rmsfs):
  rmsf = rmsfs[atom_name]
  if output == 'csv':
    print '%s,%s,%s,%.4f' % \
      (file_basename, atom_name[0], atom_name[1].strip(), rmsf)
  elif output == 'pml':
    scaled_rmsf = (rmsf / max_rmsf) * 100
    print 'alter %s and chain %s and resi %s, b=%.3f' % \
      (file_basename, atom_name[0], atom_name[1].strip(), scaled_rmsf)
