#!/bin/bash
#Stephanie Wankowicz 5/13/2019
#determine which PDBs have ensemeble & qfit

#source Phenix
source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh #CHANGE THIS AS NEEDED
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate qfit
which python

base_dir=/wynton/home/fraserlab/swankowicz/190503_Targets/
touch /wynton/home/fraserlab/swankowicz/190503_Targets/phenix_done.txt
touch /wynton/home/fraserlab/swankowicz/190503_Targets/qfit_done.txt
touch /wynton/home/fraserlab/swankowicz/190503_Targets/qfit_phenix_done.txt
touch /wynton/home/fraserlab/swankowicz/190503_Targets/summary_table.csv

#printf $'\n'$PDB > /wynton/home/fraserlab/swankowicz/190503_Targets/qfit_phenix_done.txt
#qfit_phenix_done+=("$PDB")
n=0
PDB_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/apo_test.txt
while read line; do
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
    rm -r A_*
    rm -r B_*
    rm -r C_*
    rm -r D_*
    generate_single_conformer $PDB.pdb> ${PDB}_baseline_summary_output.txt
    get_metrics $PDB.pdb > ${PDB}_baseline_ind_rmsd_output.txt
    get_metrics multiconformer_model2.pdb > ${PDB}_multi_ind_rmsd_output.txt
    generate_single_conformer multiconformer_model2.pdb > ${PDB}_multi_summary.txt
    RMSF ${PDB}-sf.mtz $PDB.pdb --pdb=${PDB}_orig
    RMSF ${PDB}-sf.mtz multiconformer_model2.pdb --pdb=${PDB}_multi
    ((qfit++))
    try
    (
    	ligand=$(cat "ligand.txt")
    )
    catch || {
      ligand='apo'
    }
    echo $ligand
    num_resn ${PDB}.pdb > ${PDB}_num_res.txt
    num_residues=$(cat "${PDB}_num_res.txt")
    echo '________________________________________________________Checking Phenix #1________________________________________________________'
    if [ -e "${PDB}_0.6_5.pdb" ]; then
      echo 'ensemble done!'
      ((phenix++))
      gunzip ${PDB}*.pdb.gz
      echo 'starting analysis 1'
      phenix.python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_rmsf.py ${PDB}.pdb CA csv > ${PDB}_original.csv
      phenix.python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_rmsf.py ${PDB}_0.8_10.pdb CA csv > ${PDB}_ens.csv
      python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_refine_parser_main_log.py ${PDB}_0.6_5/${PDB}_0.6_5.log
      python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/summary_stats_table_creation.py --ligand=$ligand --average_conf_org=${PDB}_baseline_summary_output.txt --average_conf_qfit=${PDB}_multi_summary.txt --pdb_name=$PDB --num_res=$num_residues --pdb_num=$n --refine_log=${PDB}_refine_df.csv --ens_refine_log=${PDB}_ens_refinement_output.csv
    else [ -d "${PDB}_0.6_5" ]
      #cd ${PDB}_0.6_5_
      echo 'folder exists!'
      if [ -e "${PDB}_0.6_5/${PDB}_0.6_5.pdb.gz" ]; then
        echo 'ensemble done!'
        ((phenix++))
        echo $'\n'$PDB> /wynton/home/fraserlab/swankowicz/190503_Targets/qfit_phenix_done.txt #\n
        qfit_phenix_done+=("$PDB")
        mv "${PDB}_0.6_5*/${PDB}_0.6_5.pdb.gz" .
        mv "${PDB}_0.6_2.5*/${PDB}_0.6_2.5.pdb.gz" .
        mv "${PDB}_0.6_10*/${PDB}_0.6_10.pdb.gz" .
        mv "${PDB}_0.8_5*/${PDB}_0.8_5.pdb.gz" .
        mv "${PDB}_0.8_2.5*/${PDB}_0.8_2.5.pdb.gz" .
        mv "${PDB}_0.8_10*/${PDB}_0.8_10.pdb.gz" .
        gunzip ${PDB}*.pdb.gz
        python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_refine_parser_main_log.py ${PDB}_0.6_5/${PDB}_0.6_5.log
        phenix.python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_rmsf.py ${PDB}.pdb CA csv > ${PDB}_original.csv
        phenix.python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_rmsf.py ${PDB}_0.8_10*.pdb CA csv > ${PDB}_ens.csv
      fi
    fi
  else
    if [ -e "${PDB}_0.6_5.pdb*" ]; then
      echo 'ensemble done!'
      echo $'\n'$PDB > /wynton/home/fraserlab/swankowicz/190503_Targets/phenix_done.txt
      ((phenix++))
    else
      if [ -d "${PDB}_0.6_5" ]; then
        #cd ${PDB}_0.6_5_
        echo 'folder exists!'
        if [[ -e "${PDB}_0.6_5*/${PDB}_0.6_5*.pdb.gz" ]]; then
          ((phenix++))
	  echo 'ensemble done!'
          echo $PDB > /wynton/home/fraserlab/swankowicz/190503_Targets/phenix_done.txt
          mv "${PDB}_0.6_5*/${PDB}_0.6_5.pdb.gz" .
          mv "${PDB}_0.6_2.5*/${PDB}_0.6_2.5.pdb.gz" .
          mv "${PDB}_0.6_10*/${PDB}_0.6_10.pdb.gz" .
          mv "${PDB}_0.8_5*/${PDB}_0.8_5.pdb.gz" .
          mv "${PDB}_0.8_2.5*/${PDB}_0.8_2.5.pdb.gz" .
          mv "${PDB}_0.8_10*/${PDB}_0.8_10.pdb.gz" .
          gunzip ${PDB}*.pdb.gz
        fi
      fi
    fi #check if phenix is done
  fi
done <$PDB_file

echo $phenix
echo $qfit

echo 'qfit_phenix_done'
echo $qfit_phenix_done
echo 'starting analysis'
#get qfit_phenix_done.txt

'''
all_done=/wynton/home/fraserlab/swankowicz/190503_Targets/qfit_phenix_done.txt
while read line; do
  echo $line
  PDB=$line
  echo $PDB
  cd $base_dir
  cd $PDB
  #run phenix analysis
  #python /wynton/home/fraserlab/swankowicz/190419_Phenix/ens_refine_parser.py ${PDB}.log
  phenix.python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_rmsf.py ${PDB}.pdb CA csv > ${PDB}_original.csv
  phenix.python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_rmsf.py ${PDB}_0.8_10.pdb CA csv > ${PDB}_ens.csv
  #run qfit analysis
  generate_single_conformer $PDB.pdb> baseline_summary_output.txt
  get_metrics $PDB.pdb > baseline_ind_rmsd_output.txt
  get_metrics multiconformer_model2.pdb > multi_ind_rmsd_output.txt
  #cat baseline_ind_rmsd_output.txt | wc -l > num_residues.txt
  #wc -l baseline_ind_rmsd_output.txt > num_residues.txt
  python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/psi_phi_angles.py --pdb ${PDB}.pdb --pdb_name $PDB
  generate_single_conformer multiconformer_model2.pdb > ${PDB}_multi_summary.txt
  RMSF ${PDB}-sf.mtz $PDB.pdb --pdb=${PDB}_orig
  RMSF ${PDB}-sf.mtz multiconformer_model2.pdb --pdb=${PDB}_multi

  #python script to get pdb name, resolution, size of protein, ligand name, average # of multi conf pre/post qfit
  #make sure all other scripts have pdb names in output column
  #concadenate all of them
done <$all_done
#cd $base_dir
#mkdir scrape_files_5_22_2019
'''
