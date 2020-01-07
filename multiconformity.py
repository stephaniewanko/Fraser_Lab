####################  multiconformity.py  ####################
#
# Reads in two (or more) multi-conformer or ensemble models
# and compares them in terms of how many sidechain conformations
# at each position fall into the same rotamer well as assigned
# by MolProbity.
#
# There's also plenty of room to expand on this to look at 
# correlations between residues in one ensemble a la MutInf...
#
# Started by Daniel Keedy in May 2013
#
##############################################################

import sys
import os
import iotbx.pdb.hierarchy
from mmtbx.rotamer import rotamer_eval
from mmtbx.rotamer import sidechain_angles
import iotbx.pdb.amino_acid_codes

# These scorers are global variables since they hog memory (I think?)
rotamer_scorer = rotamer_eval.RotamerEval()
sc_angles_measurer = sidechain_angles.SidechainAngles(show_errs=True)

aa_resnames = iotbx.pdb.amino_acid_codes.one_letter_given_three_letter

class StructureEnsemble():
  
  def __init__(self, nm):
    self.name = nm
    self.conf_ensems = {} # CNIT --> ConformerEnsemble

  def add_structures(self, dirname):
    for filename in os.listdir(dirname):
      self.add_structure(filename)
  
  def add_structure(self, filename):
    pdb = iotbx.pdb.hierarchy.input(file_name=filename)
    hierarchy = pdb.hierarchy
    structure_name = os.path.basename(filename).strip(".pdb").strip()
    # We're using the "third view" of the PDB hierarchy here; 
    # see cctbx_project/iotbx/examples/pdb_hierarchy.py for what that means.
    # We're doing this basically because we want a complete conformation for 
    # every residue, which most pressingly means we want e.g. ' '+'A' for cases 
    # where the backbone is alt ' ' but the sidechain has alts 'A' and 'B'.
    # The "first view" is bad here because it gives separate pieces 
    # of each residue in ' ', 'A', and 'B'.
    # The "second view" is bad because it gives an entire structure for each 
    # alt conf, so even single-conformer residues get multiple appearances.
    for m, model in enumerate(hierarchy.models()):
      for chain in model.chains():
        for residue_group in chain.residue_groups():
          resseq = residue_group.resseq_as_int()
          icode = residue_group.icode
          for residue_conformer in residue_group.conformers():
            residue = residue_conformer.only_residue()
            resname = residue.resname
            if resname not in aa_resnames: continue
            cnit = (chain.id, resseq, icode, resname)
            if cnit in self.conf_ensems:
              conf_ensem = self.conf_ensems[cnit]
            else:
              conf_ensem = ConformerEnsemble(chain.id, resseq, icode, resname)
              self.conf_ensems[cnit] = conf_ensem
            assert conf_ensem is not None
            if resname in ["GLY", "ALA"]:
              chis = None
              value = None
              rotamer = "n/a"
            else:
              chis = sc_angles_measurer.measureChiAngles(residue)
              if None in chis: # probably some missing atoms because disordered
                continue # go to next atom_group
              else:
                value = rotamer_scorer.evaluate(resname, chis)
                rotamer = rotamer_scorer.evaluate_residue(residue)
            if rotamer is None:
              rotamer = "(disordered?)"
            altloc = None
            if len(residue_group.conformers()) > 1:
              altloc = residue_conformer.altloc
            modelnum=None
            if len(hierarchy.models()) > 1:
              modelnum = m+1
            conformer = Conformer(structure_name, chain.id, resseq, icode, 
              resname, chis, value, rotamer, a=altloc, m=modelnum)
            conf_ensem.add(conformer)

  def summarize(self, show_details=False):
    print self.name, 'StructureEnsemble:'
    for cnit in sorted(self.conf_ensems):
      conf_ensem = self.conf_ensems[cnit]
      conf_ensem.summarize(show_details)
  
  def compare_to(self, other):
    for cnit in sorted(self.conf_ensems):
      this = self.conf_ensems[cnit]
      that = other.conf_ensems[cnit]
      num_rotamers_comparison = 'same'
      if len(this.unique_rotamers) > len(that.unique_rotamers):
        num_rotamers_comparison = '1 has more'
      elif len(that.unique_rotamers) > len(this.unique_rotamers):
        num_rotamers_comparison = '2 has more'
      print "%s %s '%s' %s: %d vs. %d unique rotamers; %s" % \
        (cnit[0], cnit[1], cnit[2], cnit[3], \
         len(this.unique_rotamers), len(that.unique_rotamers), num_rotamers_comparison)
      continue
      # ...
      # ...
      # ...
      print "%s %s '%s' %s" % (cnit[0], cnit[1], cnit[2], cnit[3])
      if len(this.rotamer_prevalences) != len(this.unique_rotamers):
        this.calculate_rotamer_prevalences()
      if len(that.rotamer_prevalences) != len(that.unique_rotamers):
        that.calculate_rotamer_prevalences()
      this_that_rotamers = set()
      for rotamer in this.rotamer_prevalences:
        this_that_rotamers.add(rotamer)
      for rotamer in that.rotamer_prevalences:
        this_that_rotamers.add(rotamer)
      #for rotamer in this_that_rotamers:
      for rotamer in sorted(this_that_rotamers, 
                          key=this.rotamer_prevalences.get,
                          reverse=True):
        this_preval = that_preval = 0.
        if rotamer in this.rotamer_prevalences:
          this_preval = this.rotamer_prevalences[rotamer]
        if rotamer in that.rotamer_prevalences:
          that_preval = that.rotamer_prevalences[rotamer]
        print '  %s: %.3f vs. %.3f' % (rotamer, this_preval, that_preval)

  def rotamer_overlap(self, other):
    print "resname: in_1_not_2,in_both,in_2_not_1"
    for cnit in sorted(self.conf_ensems):
      these = self.conf_ensems[cnit].unique_rotamers
      those = other.conf_ensems[cnit].unique_rotamers
      print "%s %s %s: %d,%d,%d" % (cnit[0], cnit[1], cnit[3], \
        len(these - those), len(these & those), len(those - these))

class ConformerEnsemble():
  
  def __init__(self, ch, rs, ic, rn):
    
    self.chain = ch
    self.resseq = rs
    self.icode = ic
    self.resname = rn
    
    # Not a dictionary -- the Conformers themselves store their own 
    # identifying information
    self.conformers = set()
    
    self.unique_rotamers = set()   # simple rotamer names
    self.rotamer_counts = {}       # rotamer name --> count
    self.rotamer_prevalences = {}  # rotamer name --> prevalence (%)
  
  def add(self, conformer):
    self.conformers.add(conformer)
    self.unique_rotamers.add(conformer.rotamer)
  
  def get(self, structure_name=None, altloc=None, modelnum=None):
    print 'TODO'
    # make this parse through the Conformers
    # and find one that matches the criterion provided
    # (e.g. altloc or model # or pdb name)

  def calculate_rotamer_prevalences(self):
    if len(self.rotamer_prevalences) == len(self.unique_rotamers):
      # We've already run this method to completion!
      return
    for unique_rotamer in self.unique_rotamers:
      count = 0
      for conformer in self.conformers:
        rotamer = conformer.rotamer
        if rotamer == unique_rotamer:
          count += 1
      prevalence = float(count) / float(len(self.conformers))
      self.rotamer_counts[unique_rotamer] = count
      self.rotamer_prevalences[unique_rotamer] = prevalence
    assert len(self.rotamer_prevalences) == len(self.unique_rotamers), \
      "Number of unique rotamers doesn't match number of prevalences!"
    assert sum(self.rotamer_prevalences.values()) <= 1.00000001, \
      "Unique rotamer prevalences add up to more than 1.0:  "+ \
        ("%.10f" % (sum(self.rotamer_prevalences.values())))

  def summarize(self, show_details=False, prevalent_rotamers_only=False):
    if len(self.rotamer_prevalences) != len(self.unique_rotamers):
      self.calculate_rotamer_prevalences()
    print "%s %d %s %s" % (self.chain, self.resseq, self.icode, self.resname)
    if show_details:
      for conformer in sorted(self.conformers):
        conformer.summarize()
    else:
      for rotamer in sorted(self.rotamer_prevalences, 
                          key=self.rotamer_prevalences.get,
                          reverse=True):
        if prevalent_rotamers_only and self.rotamer_prevalences[rotamer] < 0.1:
          continue
        print "  %.3f (%d): %s" % (self.rotamer_prevalences[rotamer],
                                   self.rotamer_counts[rotamer], rotamer)
  
class Conformer:
  
  def __init__(self, sn, ch, rs, ic, rn, c, v, r, a=None, m=None):
    
    self.structure_name = sn  # often just PDB ID
    self.chain = ch
    self.resseq = rs
    self.icode = ic
    self.resname = rn
    self.chis = c
    self.value = v
    self.rotamer = r
    
    self.altloc = a    # from a multi-alt-conf structure
    self.modelnum = m  # from a multi-MODEL NMR-style structure
    
    self.nearest_nonout = None
    self.dist_to_nearest_nonout = None

  def find_closest_nonoutlier_chis(self, rotamer_scorer):
    from mmtbx.rotamer import rotamer_eval
    ndt = rotamer_scorer.aaTables.get(self.resname.lower())
    self.nearest_nonout = \
      ndt.findNearestNonOutlierPoint(self.chis, min_val=0.01)
    self.dist_to_nearest_nonout = \
      ndt.distanceBetween(self.chis, self.nearest_nonout)

  def summarize(self):
    if self.chis is None:
      if self.resname in ["GLY", "ALA"]:
        chi_string = "n/a"
      else:
        chi_string = "at least one chi None"
      value_string = "??????"
    else:
      chi_strings = ("%.3f" % chi for chi in self.chis)
      chi_string = ", ".join(chi_strings)
      value_string = "%.4f" % self.value
    altloc_string = modelnum_string = ''
    if self.altloc not in [None, '', ' ']:
      altloc_string = "alt'"+self.altloc+"'" 
    if self.modelnum is not None:
      modelnum_string = "model"+str(self.modelnum)
    out_string = "  %s %d '%s' %s %s %s %s %s [%s]" % \
       (self.chain, self.resseq, self.icode, self.resname, 
        altloc_string, modelnum_string,
        value_string, self.rotamer, chi_string)
    if not None in (self.nearest_nonout, self.dist_to_nearest_nonout):
      nearest_chi_strings = ("%.3f" % chi for chi in self.nearest_nonout)
      nearest_chi_string = ", ".join(nearest_chi_strings)
      out_string += ", %.3f to [%s]" % \
        (self.dist_to_nearest_nonout, nearest_chi_string)
    print out_string

if __name__ == "__main__":
  
  print "Oh -- hello there!  Welcome to multiconformity."
  print "You are about to gain insight into multiple protein conformers."
  print "*Everyone* does...\n"
  
  if len(sys.argv) != 3:
    s = os.path.basename(__file__)
    print 'Usage: python', s, '[1.pdb | 1/] [2.pdb | 2/]'
    print '       #.pdb is a multi-conformer model or ensemble model'
    print '       #/ is a directory of (single-conformer only?) models'
    sys.exit()
  
  filename = sys.argv[1]
  struc_ensem_1 = StructureEnsemble(os.path.basename(filename).rstrip(".pdb"))
  struc_ensem_1.add_structure(filename)
  struc_ensem_1.summarize(show_details=False)
  
  filename = sys.argv[2]
  struc_ensem_2 = StructureEnsemble(os.path.basename(filename).rstrip(".pdb"))
  struc_ensem_2.add_structure(filename)
  struc_ensem_2.summarize(show_details=False)
  
  #struc_ensem_1.compare_to(struc_ensem_2)

  struc_ensem_1.rotamer_overlap(struc_ensem_2)
