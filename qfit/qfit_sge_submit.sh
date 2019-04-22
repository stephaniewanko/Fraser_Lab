#!/bin/bash

##$ -l h_vmem=80G
##$ -l mem_free=64G
##$ -t 1-5
##$ -l h_rt=100:00:00

#This script will be used to submit and parse through qfit.


input_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/HIV_Prot2.txt
for i in {1..6}; do echo $i
  echo $i
  PDB=$(cat $input_file | head -n $i | tail -n 1)
  echo $PDB
  mkdir $PDB_qfit
  cd $PDB_qfit
  wget https://files.rcsb.org/download/$PDB.pdb
  wget http://edmaps.rcsb.org/coefficients/$PDB.mtz
  phenix.composite_omit_map ${PDB}_phases.mtz ${PDB}.pdb omit-type=refine
  qfit_protein composite_omit_map.mtz -l 2FOFCWT,PH2FOFCWT ${PDB}.pdb
done
