#!/bin/bash

#this must be done before you submit to SGE since SGE cannot connect to the internet!

cd /wynton/home/fraserlab/swankowicz/output

pdb_filelist='/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/190408_HIV_Prot2.txt'
while read line; do

  echo $line
  PDB=$line

  #make sure you are in the home directory
  mkdir $PDB
  cd $PDB

  #download files
  wget https://files.rcsb.org/download/$PDB.pdb
  wget https://files.rcsb.org/download/$PDB-sf.cif
  wget http://edmaps.rcsb.org/coefficients/$PDB.mtz
done < $pdb_filelist
