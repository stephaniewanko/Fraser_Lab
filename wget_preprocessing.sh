#!/bin/bash
#Stephanie Wankowicz
#04/25/2019

#this must be done before you submit to SGE since SGE cannot connect to the internet!

#________________________________________________INPUTS________________________________________________#
base_folder='/wynton/group/fraser/swankowicz/191227_qfit/' #base folder (where you want to put folders/pdb files

pdb_filelist=/wynton/group/fraser/swankowicz/script/comp_omit4.txt
while read -r line; do
  PDB=$line
  cd $base_folder
  if [ -d "/$PDB" ]; then
    echo "Folder exists." 
  else
    mkdir $PDB
  fi
  #mkdir $PDB
  cd $PDB
  wget https://files.rcsb.org/download/${PDB}.pdb
  wget https://files.rcsb.org/download/${PDB}-sf.cif
  wget http://edmaps.rcsb.org/coefficients/${PDB}.mtz
done < $pdb_filelist
