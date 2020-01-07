#!/bin/bash


#________________________________________________INPUTS________________________________________________#
working_dir='/wynton/home/fraserlab/swankowicz/190503_Targets'  #where the folders are located
apo_PDB_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/apo_examine.txt  #list of PDB IDs
holo_PDB_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/holo_examine.txt

#________________________________________________Activate Env________________________________________________#
source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate qfit

#________________________________________________Qfit Analysis________________________________________________#
for i in {14..18}; do
  apo_PDB=$(cat $apo_PDB_file | head -n $i | tail -n 1)
  echo $apo_PDB
  cd $working_dir
  #cd $apo_PDB
  #echo 'qfit scripts'
  holo_PDB=$(cat $holo_PDB_file | head -n $i | tail -n 1)
  echo $holo_PDB
  #cd $working_dir
  cd $holo_PDB
  echo 'Holo PDB!'
  lig_name=$(cat "ligand_name.txt")
  cd $working_dir
  mkdir ${apo_PDB}_${holo_PDB}
  cd ${apo_PDB}_${holo_PDB}
  distance=5
  subset_structure -apo_structure $working_dir/$apo_PDB/$apo_PDB.updated_refine_001.pdb -holo_structure $working_dir/$holo_PDB/${holo_PDB}.updated_refine_001.pdb -lig $lig_name -dis $distance --PDB_name ${apo_PDB}_${holo_PDB}_refined
  subset_structure -apo_structure $working_dir/$apo_PDB/multiconformer_model2.pdb -holo_structure $working_dir/$holo_PDB/multiconformer_model2.pdb -lig $lig_name -dis  $distance --PDB_name ${apo_PDB}_${holo_PDB}_qfit
  #subset_structure -apo_structure $working_dir/$apo_PDB/$apo_PDB_0.6_5.pdb -holo_structure $working_dir/$holo_PDB/${holo_PDB}_0.6_5.pdb -lig $lig_name -dis	5 --PDB_name ${apo_PDB}_${holo_PDB}_ensemble

  echo 'analysis'
  python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/b_factors.py --pdb=${apo_PDB}_${holo_PDB}_refined_holo_substructure.pdb --pdb_name=${holo_PDB}_refined
  python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/b_factors.py --pdb=${apo_PDB}_${holo_PDB}_refined_apo_substructure.pdb --pdb_name=${apo_PDB}_refined
  #python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/phi_psi_angles.py --pdb=${PDB}.updated_refine_001.pdb --pdb_name=${PDB}_original
  generate_single_conformer ${apo_PDB}_${holo_PDB}_refined_holo_substructure.pdb> ${holo_PDB}_${distance}_refined_baseline_summary_output.txt
  generate_single_conformer ${apo_PDB}_${holo_PDB}_refined_apo_substructure.pdb> ${apo_PDB}_${distance}_refined_baseline_summary_output.txt
  RMSF $working_dir/$apo_PDB/${apo_PDB}-sf.mtz ${apo_PDB}_${holo_PDB}_refined_apo_substructure.pdb --pdb=${apo_PDB}_orig_${distance}
  RMSF $working_dir/$holo_PDB/${holo_PDB}-sf.mtz ${apo_PDB}_${holo_PDB}_refined_holo_substructure.pdb --pdb=${holo_PDB}_orig_${distance}

  python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/b_factors.py --pdb=${apo_PDB}_${holo_PDB}_qfit_holo_substructure.pdb --pdb_name=${holo_PDB}_qfit
  python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/b_factors.py --pdb=${apo_PDB}_${holo_PDB}_qfit_apo_substructure.pdb --pdb_name=${apo_PDB}_qfit
  #python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/phi_psi_angles.py --pdb=${PDB}.updated_refine_001.pdb --pdb_name=${PDB}_original
  generate_single_conformer ${apo_PDB}_${holo_PDB}_qfit_holo_substructure.pdb> ${holo_PDB}_${distance}_qfit_baseline_summary_output.txt
  generate_single_conformer ${apo_PDB}_${holo_PDB}_qfit_apo_substructure.pdb> ${apo_PDB}_${distance}_qfit_baseline_summary_output.txt
  RMSF $working_dir/$apo_PDB/${apo_PDB}-sf.mtz ${apo_PDB}_${holo_PDB}_qfit_apo_substructure.pdb --pdb=${apo_PDB}_qfit_${distance}
  RMSF $working_dir/$holo_PDB/${holo_PDB}-sf.mtz ${apo_PDB}_${holo_PDB}_qfit_holo_substructure.pdb --pdb=${holo_PDB}_qfit_${distance}

  #python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/analysis.py -PDB=$apo_PDB -sum=qfit_summary_output.txt -ind=qfit_ind_rmsd_output.txt -h_a=apo -qfit=Yes -dis=0
done
