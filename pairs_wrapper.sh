#!/bin/bash
#Stephanie Wankowicz
#Started: 19-12-09


#__________________SET PATHS________________________________________________#
conda activate qfit3
PDB_file=/wynton/group/fraser/swankowicz/PDB_pairs_191202.txt 
base_dir='/wynton/group/fraser/swankowicz/qfit_pair_output/'
cd $base_dir

for i in {2001..3000}; do
  holo=$(cat $PDB_file | awk '{ print $1 }' |head -n $i | tail -n 1)
  apo=$(cat $PDB_file | awk '{ print $2 }' | head -n $i | tail -n 1)
  echo $holo
  echo $apo
  #get_metrics /wynton/group/fraser/swankowicz/mtz/191114/pdb${holo}.ent > /wynton/group/fraser/swankowicz/qfit_pair_output/${holo}_baseline_ind.csv 
  #get_metrics /wynton/group/fraser/swankowicz/mtz/191114/pdb${apo}.ent > /wynton/group/fraser/swankowicz/qfit_pair_output/${apo}_baseline_ind.csv
  find_altlocs /wynton/group/fraser/swankowicz/mtz/191114/pdb${apo}.ent ${apo} -dir='/wynton/group/fraser/swankowicz/qfit_pair_output/'
  find_altlocs /wynton/group/fraser/swankowicz/mtz/191114/pdb${holo}.ent ${holo} -dir='/wynton/group/fraser/swankowicz/qfit_pair_output/' 
  #python /wynton/group/fraser/swankowicz/script/get_sasa.py /wynton/group/fraser/swankowicz/mtz/191114/pdb${apo}.ent ${apo} '/wynton/group/fraser/swankowicz/qfit_pair_output/'
  #python /wynton/group/fraser/swankowicz/script/get_sasa.py /wynton/group/fraser/swankowicz/mtz/191114/pdb${holo}.ent ${holo} '/wynton/group/fraser/swankowicz/qfit_pair_output/'
done
