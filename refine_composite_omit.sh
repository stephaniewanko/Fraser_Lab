#!/bin/bash

#$ -l h_vmem=80G
#$ -l mem_free=64G
#$ -t 1-1
#$ -l h_rt=100:00:00
#$ -pe smp 1


#this script will run qfit based on the input PDB names you have.

#________________________________________________INPUTS________________________________________________#
working_dir='/wynton/group/fraser/swankowicz/191227_qfit/'  #where the folders are located
PDB_file=/wynton/group/fraser/swankowicz/script/comp_omit4_191229.txt
echo $working_dir
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

#________________________________________________SET PATHS________________________________________________#
source /wynton/home/fraserlab/swankowicz/phenix-installer-dev-3594-intel-linux-2.6-x86_64-centos6/phenix-dev-3594/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate qfit3


which python
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

#________________________________________________RUN QFIT________________________________________________#
PDB_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/composite_omit_191227.txt  #list of PDB IDs
PDB=$1
echo $PDB
dir=$2
cd $dir
#CHANGE X Elements to C
file=$PDB.pdb; while read -r line; do var="$(echo "$line" | cut -c 78-79)"; if [[ "$var" = "X" ]]; then echo "$line" | sed s/"$var"/'C'/g ;else echo "$line";fi; done < $file >> ${PDB}_updated.pdb

remove_duplicates ${PDB}_updated.pdb

#RUN READYSET
phenix.ready_set ${PDB}_updated.pdb.fixed

#RUN REFINEMENT
if [[ -e "${PDB}_updated.pdb.updated_refine_001.pdb" ]]; then
    continue
else
    if [[ -e "${PDB}_updated.pdb.ligands.cif" ]]; then
       echo '________________________________________________________Running refinement with ligand.________________________________________________________'
       if grep -F _refln.F_meas_au $PDB-sf.cif; then
        phenix.refine ${PDB}_updated.pdb.updated.pdb ${PDB}.mtz ${PDB}_updated.pdb.ligands.cif /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize.params #refinement.input.xray_data.labels="FOBS,SIGFOBS"
       else
        echo 'IOBS'   
         phenix.refine ${PDB}_updated.pdb.updated.pdb ${PDB}.mtz ${PDB}_updated.pdb.ligands.cif /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize.params #refinement.input.xray_data.labels="IOBS,SIGIOBS"
       fi

    else
      echo '________________________________________________________Running refinement without ligand.________________________________________________________'
      if grep -F _refln.F_meas_au $PDB-sf.cif; then
        phenix.refine ${PDB}_updated.pdb.updated.pdb ${PDB}.mtz /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize.params #refinement.input.xray_data.labels="FOBS,SIGFOBS" refinement.input.xray_data.r_free_flags.label=R-free-flags
      else
        phenix.refine ${PDB}_updated.pdb.updated.pdb ${PDB}.mtz /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize.params #refinement.input.xray_data.r_free_flags.label=R-free-flags refinement.input.xray_data.labels="IOBS,SIGIOBS"
      fi
    fi      
fi

#RUN COMPOSITE OMIT MAP
    echo 'Starting Composite Omit Map'
    if [[ -e composite_omit_map.mtz ]]; then
        echo 'composite omit map already created'
    else
        if [ ! -f ${PDB}.mtz ]; then
                echo 'No mtz file'
        else
                phenix.mtz.dump ${PDB}.mtz > ${PDB}_mtzdump.out
                if grep -q FREE ${PDB}_mtzdump.out; then
                        phenix.composite_omit_map ${PDB}.mtz ${PDB}_updated.pdb.updated_refine_001.pdb omit-type=refine nproc=1 #input.xray_data.r_free_flags.label=R-free-flags
                else
                        phenix.composite_omit_map ${PDB}.mtz ${PDB}_updated.pdb.updated_refine_001.pdb omit-type=refine nproc=1 r_free_flags.generate=True
                fi
        fi
    fi


    qfit_protein composite_omit_map.mtz -l 2FOFCWT,PH2FOFCWT ${PDB}_updated.pdb.updated_refine_001.pdb --nproc 1


