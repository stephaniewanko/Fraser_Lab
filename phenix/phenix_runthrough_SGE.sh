#!/bin/bash
#SGE!

##$ -l h_vmem=80G
##$ -l mem_free=64G
##$ -t 1-5
##$ -l h_rt=100:00:00

#set up a new refinement
#Stephanie Wankowicz 4/5/2019

for i in {1..5}; do echo $i
  PDB_list=$(cat $HIV_Prot2.txt | head -n $i | tail -n 1)
  echo $PDB_list
  ./phenix_prep.sh PDB_list
done
