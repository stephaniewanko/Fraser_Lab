#!/bin/bash
#Stephanie Wankowicz
#Started: 19-09-05
#Last Editted: 19-09-08


#__________________SET PATHS________________________________________________#
source /home/wankowicz/phenix-installer-1.16-3546-intel-linux-2.6-x86_64-centos6/phenix-1.16-3546/phenix_env.sh
which python
PDB_file=/data/wankowicz/190815_qfit_done/finished_pairs.csv
base_dir='/data/wankowicz/190815_qfit_done/'
cd $base_dir
  
  
  
 #________________________________________________Qfit Analysis________________________________________________#
for i in {2..2}; do
  holo=$(cat $PDB_file | awk '{ print $3 }' |head -n $i | tail -n 1)
  apo=$(cat $PDB_file | awk '{ print $4 }' | head -n $i | tail -n 1)
  echo $holo
  echo $apo
  echo 'phenix superpose:'
  cd $holo
  phenix.superpose_pdbs ../${apo}/${apo}_qFit.pdb ${holo}_qFit.pdb #> ${holo}/${holo}_superposed_qfit.pdb
  echo 'qfit scripts'
  cd ../$apo
  #generate_single_conformer $apo_PDB.pdb> baseline_summary_output.txt
  #get_metrics ${apo}.pdb > ${apo}_baseline_ind_rmsd_output.txt
  #get_metrics ${apo}_qFit.pdb > ${apo}_qFit_ind_rmsd_output.txt
  b_factor ${apo}.mtz ${apo}_qFit.pdb --pdb=${apo}_qFit
  RMSF ${apo}.mtz  ${apo}_qFit.pdb --pdb=${apo}_qFit
  find_altlocs_near_ligand -h=${apo}_qFit.pdb --pdb_name=${apo} 
  
  echo 'holo scripts:'
  cd ../$holo
  #get_metrics ${holo}_qFit.pdb > ${holo}_qFit_ind_rmsd_output.txt
  #get_metrics ${holo}.pdb > ${holo}_baseline_ind_rmsd_output.txt
  b_factor ${holo}.mtz ${holo}_qFit.pdb --pdb=${holo}_qFit
  RMSF ${holo}.mtz  ${holo}_qFit.pdb --pdb=${holo}_qFiti
  find_altlocs_near_ligand ${holo}_qFit.pdb --pdb=${holo}

  cd $base_dir
  compare_apo_holo ${apo}/${apo}_qFit.pdb ${holo}/${holo}_qFit.pdb_fitted.pdb

  echo 'pymol script'
