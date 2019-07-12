#!/bin/bash
#Stephanie Wankowicz 5/13/2019
#determine which PDBs have ensemeble & qfit

#source Phenix
source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh #CHANGE THIS AS NEEDED
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate qfit
which python

base_dir=/wynton/home/fraserlab/swankowicz/190503_Targets/
options_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/phenix_ens_grid_search_options.txt
#touch /wynton/home/fraserlab/swankowicz/190503_Targets/phenix_done.txt
#touch /wynton/home/fraserlab/swankowicz/190503_Targets/qfit_done.txt
#touch /wynton/home/fraserlab/swankowicz/190503_Targets/qfit_phenix_done.txt
#touch /wynton/home/fraserlab/swankowicz/190503_Targets/summary_table.csv

#printf $'\n'$PDB > /wynton/home/fraserlab/swankowicz/190503_Targets/qfit_phenix_done.txt
#qfit_phenix_done+=("$PDB")
n=0
PDB_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/apo_test.txt
#while read line; do
  ((n++))
  echo $n
  PDB=$line
  echo $PDB
  cd $base_dir
  cd $PDB
  #echo $qfit_phenix_done
  qfit=0
  phenix=0
  echo '________________________________________________________Checking Qfit #1________________________________________________________'
  if [[ -e "multiconformer_model2.pdb" ]]; then
    echo 'qfit done!'
    #rm -r A_*
    #rm -r B_*
    #rm -r C_*
    #rm -r D_*
    generate_single_conformer $PDB.pdb> ${PDB}_baseline_summary_output.txt
    get_metrics $PDB.pdb > ${PDB}_baseline_ind_rmsd_output.txt
    get_metrics multiconformer_model2.pdb > ${PDB}_multi_ind_rmsd_output.txt
    generate_single_conformer multiconformer_model2.pdb > ${PDB}_multi_summary.txt
    RMSF ${PDB}-sf.mtz $PDB.pdb --pdb=${PDB}_orig
    RMSF ${PDB}-sf.mtz multiconformer_model2.pdb --pdb=${PDB}_multi
    ~/anaconda3/envs/qfit/bin/python3 /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/b_factors.py --pdb=multiconformer_model2.pdb --pdb_name=${PDB}_qfit
    ~/anaconda3/envs/qfit/bin/python3 /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/psi_phi_angles.py --pdb=multiconformer_model2.pdb --pdb_name=${PDB}_qfit
    ((qfit++))
    ligand=$(cat "ligand.txt") || ligand='apo'
    echo $ligand
    num_resn ${PDB}.pdb
    num_residues=$(cat "${PDB}_num_residues.txt")
    
    echo '________________________________________________________Checking Phenix #1________________________________________________________'
    phenix.python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_rmsf.py ${PDB}.updated_refine_001.pdb CA csv > ${PDB}_original.csv
    ~/anaconda3/envs/qfit/bin/python3 /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/b_factors.py --pdb=${PDB}.updated_refine_001.pdb --pdb_name=${PDB}_original
    ~/anaconda3/envs/qfit/bin/python3 /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/psi_phi_angles.py --pdb=${PDB}.updated_refine_001.pdb --pdb_name=${PDB}_original
    for i in {1..9}; do
      echo $i
      pTLS=$(cat $options_file | awk '{ print $1 }' |head -n $i | tail -n 1)
      weights=$(cat $options_file | awk '{ print $2 }'|head -n $i | tail -n 1)
      if [ -e "${PDB}_${pTLS}_${weights}.pdb" ]; then
        echo 'PDB exists'
        python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_refine_parser_main_log.py ${PDB}_${pTLS}_${weights}/${PDB}_${pTLS}_${weights}.log
      elif [ -e "${PDB}_${pTLS}_${weights}.pdb.gz" ]; then
        echo 'Gunzip exists'
        gunzip ${PDB}_${pTLS}_${weights}.pdb.gz
        python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_refine_parser_main_log.py ${PDB}_${pTLS}_${weights}/${PDB}_${pTLS}_${weights}.log
      elif [ -d "${PDB}_${pTLS}_${weights}" ]; then
        echo 'directory exists'
        mv "${PDB}_${pTLS}_${weights}/${PDB}_${pTLS}_${weights}.pdb.gz" .
        gunzip ${PDB}_${pTLS}_${weights}.pdb.gz
        python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_refine_parser_main_log.py ${PDB}_${pTLS}_${weights}/${PDB}_${pTLS}_${weights}.log
      else
	echo 'None'
      fi
      ((n++))
      echo 'running analysis scripts'
      phenix.python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_rmsf.py ${PDB}_${pTLS}_${weights}.pdb CA csv > ${PDB}_${pTLS}_${weights}_ens.csv
      ~/anaconda3/envs/qfit/bin/python3 /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/b_factors.py --pdb=${PDB}_${pTLS}_${weights}.pdb --pdb_name=${PDB}_${pTLS}_${weights}_ensemble
      ~/anaconda3/envs/qfit/bin/python3 /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/psi_phi_angles.py --pdb=${PDB}_0.6_5.pdb --pdb_name=${PDB}_${pTLS}_${weights}_ensemble
      phenix.python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/multiconformity.py ${PDB}.updated_refine_001.pdb ${PDB}_${pTLS}_${weights}.pdb > ${PDB}_${pTLS}_${weights}_rotamer.csv
      echo $ligand
      echo $n
      python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/summary_stats_table_creation.py --ligand=$ligand --average_conf_org=${PDB}_baseline_summary_output.txt --average_conf_qfit=${PDB}_mul$
    done
   else
    echo 'Qfit not done!'
   fi
#done <$PDB_file

#echo $phenix
#echo $qfit

#echo 'qfit_phenix_done'
#echo $qfit_phenix_done
#echo 'starting analysis'
#get qfit_phenix_done.txt
