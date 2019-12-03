#$ -l mem_free=60G
#$ -t 1-1
#$ -l h_rt=100:00:00
#$ -R yes
#$ -V


#this script will run qfit based on the input PDB names you have.

#________________________________________________INPUTS________________________________________________#
PDB_file=/wynton/group/fraser/swankowicz/PDB_2A_res_w_lig_191123.txt #PDB_2A_res_w_lig_111719.txt
export OMP_NUM_THREADS=1

#________________________________________________SET PATHS________________________________________________#
source /wynton/home/fraserlab/swankowicz/phenix-installer-dev-3594-intel-linux-2.6-x86_64-centos6/phenix-dev-3594/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate qfit3
which python

#________________________________________________RUN SCRIPT________________________________________________#
PDB=$(cat $PDB_file | head -n $SGE_TASK_ID | tail -n 1)


#cp -R /wynton/group/fraser/swankowicz/mtz/ $TMPDIR/
#cp -R /wynton/group/fraser/swankowicz/mtz/191114/ $TMPDIR/

#cp /wynton/group/fraser/swankowicz/mtz/191114/pdb${line}.ent $TMPDIR/${PDB}
#cp /wynton/group/fraser/swankowicz/mtz/191114/${line}.dump $TMPDIR/${PDB}

sh /wynton/group/fraser/swankowicz/gather_seq.sh
#sh /wynton/group/fraser/swankowicz/run_qfit_ligand.sh
#sh /wynton/group/fraser/swankowicz/run_nucleotide_remove.sh
#sh /wynton/group/fraser/swankowicz/find_str_with_Hetatom.sh $PDB
sh /wynton/group/fraser/swankowicz/find_apo_holo2.sh $PDB
#sh /wynton/group/fraser/swankowicz/space_unit_text.sh $PDB
#sh /wynton/group/fraser/swankowicz/run_mtz_dump.sh $PDB

#cp -R ${TMPDIR}/${PDB}/ $base_dir/
