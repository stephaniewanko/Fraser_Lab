#!/bin/bash
#Stephanie Wankowicz
#Started: 19-09-05
#Last Editted: 19-09-20


#__________________SET PATHS________________________________________________#
#source /wynton/home/fraserlab/swankowicz/phenix-installer-dev-3594-intel-linux-2.6-x86_64-centos6/phenix-dev-3594/phenix_env.sh
source /wynton/group/fraser/swankowicz/phenix-1.17rc5-3630/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate qfit3
which python

#PDB_file=/wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/200115_pdbnames.txt
PDB_file=/wynton/group/fraser/swankowicz/script/text_files/qfit_pairs_191218.txt
base_dir='/wynton/group/fraser/swankowicz/qfit_pair_output/qfit_output/'
cd $base_dir

#________________________________________________Qfit Analysis________________________________________________#
for i in {396..1268}; do
  holo=$(cat $PDB_file | awk '{ print $1 }' |head -n $i | tail -n 1)
  apo=$(cat $PDB_file | awk '{ print $2 }' | head -n $i | tail -n 1)
  echo $holo
  echo $apo
  echo 'phenix superpose:'
  cd $base_dir
  lig_name=$(grep -A 1 ${holo} /wynton/group/fraser/swankowicz/PDB_2A_lig_name_111419.txt)
  lig_name=$(echo $lig_name | cut -c5-8)
  echo $lig_name
  if [[ ! -f /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${holo}/${holo}_qFit.pdb ]]; then
     continue
  fi
  if [[ ! -f /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${apo}/${apo}_qFit.pdb ]]; then
     continue
  fi
  phenix.superpose_pdbs /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${holo}/${holo}_qFit.pdb /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${apo}/${apo}_qFit.pdb > ${apo}_${holo}_superpose.txt
  #phenix.superpose_pdbs /wynton/group/fraser/swankowicz/mtz/191114/pdb${holo}.ent /wynton/group/fraser/swankowicz/mtz/191114/pdb${apo}.ent > ${apo}_${holo}_superpose.txt
  renaming_chain /wynton/group/fraser/swankowicz/mtz/191114/pdb${holo}.ent /wynton/group/fraser/swankowicz/qfit_pair_output/pdb${apo}.ent_fitted.pdb ${holo} ${apo} ${base_dir}
  if [[ -f ${base_dir}/${holo}renamed.txt ]]; then
      get_metrics /wynton/group/fraser/swankowicz/mtz/191114/pdb${holo}.ent_renamed.pdb > ${base_dir}/${holo}_baseline_ind_rmsd_output.txt
      b_factor /wynton/group/fraser/swankowicz/mtz/191114/pdb${holo}.ent_renamed.pdb_renamed.pdb --pdb=${holo}
      RMSF /wynton/group/fraser/swankowicz/mtz/191114/pdb${holo}.ent_renamed.pdb_renamed.pdb --pdb=${holo}
      find_altlocs /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${holo}/${holo}_qFit.pdb_renamed.pdb ${holo}_qFit
  else
      get_metrics /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${holo}/${holo}_qFit.pdb > ${base_dir}/${holo}_qFit_baseline_ind_rmsd_output.txt
      b_factor /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${holo}/${holo}_qFit.pdb --pdb=${holo}_qFit
      RMSF /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${holo}/${holo}_qFit.pdb --pdb=${holo}_qFit
  fi
  if [[ -f ${base_dir}/${apo}renamed.txt ]]; then
     holo_renamed='Y'
     get_metrics /wynton/group/fraser/swankowicz/qfit_pair_output/qfit_output/${apo}.ent_fitted.pdb_renamed.pdb> ${base_dir}/${apo}_qFit_ind_baseline_rmsd_output.txt
     b_factor /wynton/group/fraser/swankowicz/qfit_pair_output/qfit_output/${apo}.ent_fitted.pdb_renamed.pdb --pdb=${apo}_qFit
     RMSF /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${apo}/${apo}_qFit.pdb_renamed.pdb --pdb=${apo}_qFit
  else
     get_metrics /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${apo}/${apo}_qFit.pdb > ${base_dir}/${apo}_qFit_ind_baseline_rmsd_output.txt
     b_factor /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${apo}/${apo}_qFit.pdb --pdb=${apo}_qFit
     RMSF /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${apo}/${apo}_qFit.pdb --pdb=${apo}_qFit
  fi
  get_metrics /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${apo}/${apo}_qFit.pdb > ${base_dir}/${apo}_qFit_ind_baseline_rmsd_output.txt
  b_factor /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${apo}/${apo}_qFit.pdb --pdb=${apo}_qFit
  RMSF /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${apo}/${apo}_qFit.pdb --pdb=${apo}_qFit
  #get_metrics /wynton/group/fraser/swankowicz/mtz/191114/pdb${apo}.ent > ${base_dir}/${apo}_baseline_ind_rmsd_output.txt
  #b_factor /wynton/group/fraser/swankowicz/mtz/191114/pdb${apo}.ent --pdb=${apo}
  #RMSF /wynton/group/fraser/swankowicz/mtz/191114/pdb${apo}.ent --pdb=${apo}

  #get_metrics /wynton/group/fraser/swankowicz/mtz/191114/pdb${holo}.ent > ${base_dir}/${holo}_baseline_ind_rmsd_output.txt
  #b_factor /wynton/group/fraser/swankowicz/mtz/191114/pdb${holo}.ent --pdb=${holo}
  #RMSF /wynton/group/fraser/swankowicz/mtz/191114/pdb${holo}.ent --pdb=${holo}
  
  get_metrics /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${holo}/${holo}_qFit.pdb > ${base_dir}/${holo}_qFit_baseline_ind_rmsd_output.txt
  b_factor /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${holo}/${holo}_qFit.pdb --pdb=${holo}_qFit
  RMSF /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${holo}/${holo}_qFit.pdb --pdb=${holo}_qFit
  
  echo ${lig_name}
  find_altlocs_AH /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${holo}/${holo}_qFit.pdb ${base_dir}/${apo}_qFit.pdb_fitted.pdb ${holo} ${apo} -lig ${lig_name} -dist 5
  
#compare_apo_holo_rmsd /wynton/group/fraser/swankowicz/mtz/191114/pdb${holo}.ent ${base_dir}/pdb${apo}.ent_fitted.pdb ${holo} ${apo}
  find_altlocs /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${holo}/${holo}_qFit.pdb ${holo}_qFit
  find_altlocs /wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${apo}/${apo}_qFit.pdb ${apo}_qFit
  #find_altlocs /wynton/group/fraser/swankowicz/mtz/191114/pdb${holo}.ent ${holo} 
  #find_altlocs /wynton/group/fraser/swankowicz/mtz/191114/pdb${apo}.ent ${apo}

  #phenix.rotalyze model=/wynton/group/fraser/swankowicz/mtz/191114/pdb${apo}.ent outliers_only=False > ${base_dir}/${apo}_rotamer_output.txt
  #phenix.rotalyze model=/wynton/group/fraser/swankowicz/mtz/191114/pdb${holo}.ent outliers_only=False > ${base_dir}/${holo}_rotamer_output.txt
   phenix.rotalyze model=/wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${apo}/${apo}_qFit.pdb outliers_only=False > ${base_dir}/${apo}_qFit_rotamer_output.txt
   phenix.rotalyze model=/wynton/group/fraser/swankowicz/from_slac/190105_to_transfer/${holo}/${holo}_qFit.pdb outliers_only=False > ${base_dir}/${holo}_qFit_rotamer_output.txt

  ~/anaconda3/envs/qfit3/bin/python /wynton/group/fraser/swankowicz/script/get_sasa.py /wynton/group/fraser/swankowicz/mtz/191114/pdb${holo}.ent ${holo} ${base_dir}
  ~/anaconda3/envs/qfit3/bin/python /wynton/group/fraser/swankowicz/script/get_sasa.py /wynton/group/fraser/swankowicz/mtz/191114/pdb${apo}.ent ${apo} ${base_dir}
  python /wynton/group/fraser/swankowicz/script/subset_output.py ${apo} 5 -qFit=Y
  python /wynton/group/fraser/swankowicz/script/subset_output.py ${holo} 5 -qFit=Y
  #python /wynton/group/fraser/swankowicz/script/subset_output.py ${apo} 5
  #python /wynton/group/fraser/swankowicz/script/subset_output.py ${holo} 5
  
 
done
