#!/bin/bash

#PBS -t 1-5
#PBS -l walltime=100:00:00
#PBS -l nodes=12
#PBS -l mppnppn=1


#this script will run qfit based on the input PDB names you have.

#________________________________________________INPUTS________________________________________________#
working_dir='/home/wankowicz/high_res_test/'  #where the folders are located
PDB_file=/mnt/home1/wankowicz/scripts/high_res.txt
echo $working_dir
export OMP_NUM_THREADS=1

#________________________________________________SET PATHS________________________________________________#
source /home/wankowicz/phenix-installer-1.16-3546-intel-linux-2.6-x86_64-centos6/phenix-1.16-3546/phenix_env.sh
export PATH="/home/wankowicz/anaconda3/bin:$PATH"
source activate qfit2.1
which python

#________________________________________________CHECK VARIABLES________________________________________________#
echo 'which job:'
echo $PBS_JOBID
echo $PBS_ARRAYID

echo "I ran on:"
#cat $PBS_NODEFILE


#________________________________________________RUN QFIT________________________________________________#
#PDB=$(cat $PDB_file | head -n $LSB_JOBINDEX | tail -n 1)
PDB=$(cat $PDB_file | head -n $PBS_ARRAYID | tail -n 1)
echo $PDB
cd $working_dir
cd $PDB

cd /tmp
#ls
mkdir wankowicz
cd wankowicz

cp -R ${working_dir}/${PDB}/ /tmp/wankowicz/
cd $PDB

#CHANGE X Elements to C
file=$PDB.pdb; while read -r line; do var="$(echo "$line" | cut -c 78-79)"; if [[ "$var" = "X" ]]; then echo "$line" | sed s/"$var"/'C'/g ;else echo "$line";fi; done < $file >> ${PDB}_updated.pdb

remove_duplicates ${PDB}_updated.pdb

#RUN READYSET
if [[ -e ${PDB}-sf.cif ]]; then
        phenix.ready_set ${PDB}_updated.pdb.fixed #cif_file_name=${PDB}-sf.cif
else
        phenix.ready_set ${PDB}_updated.pdb.fixed
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
                        phenix.composite_omit_map ${PDB}.mtz ${PDB}_updated.pdb.updated.pdb omit-type=refine nproc=24 input.xray_data.r_free_flags.label=R-free-flags
                else
                        phenix.composite_omit_map ${PDB}.mtz ${PDB}_updated.pdb.updated.pdb omit-type=refine nproc=24 r_free_flags.generate=True
                fi
        fi
fi



qfit_protein composite_omit_map.mtz -l 2FOFCWT,PH2FOFCWT ${PDB}_updated.pdb.updated.pdb --nproc 24
#RUN QFIT
echo 'starting qfit run'
#if [[ -e multiconformer_model2.pdb ]]; then
#       echo 'qfit done!'
#else
#       qfit_protein composite_omit_map.mtz -l 2FOFCWT,PH2FOFCWT ${PDB}_updated.pdb.updated.pdb --nproc 24
#fi

cp -R /tmp/wankowicz/$PDB/ $working_dir/
