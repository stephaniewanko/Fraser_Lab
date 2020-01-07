#scraping files
#git: 07-12-2019

#________________________________________________INPUTS________________________________________________#
working_dir='/wynton/home/fraserlab/swankowicz/190503_Targets/'  #where the folders are located
apo_PDB_file=/wynton/home/fraserlab/swankowicz/190503_Targets/190503_Apo2.txt  #list of PDB IDs
holo_PDB_file=/wynton/home/fraserlab/swankowicz/190503_Targets/190503_Holo2.txt

#________________________________________________Activate Env________________________________________________#
source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate qfit
which python


#scrape
for i in {1..150}; do
  holo_PDB=$(cat $apo_PDB_file | head -n $i | tail -n 1)
  echo $holo_PDB
  cd $working_dir
  cd $holo_PDB
  echo 'grabbing ligand csv'
  #cp ${holo_PDB}_ligand_verification.csv /wynton/home/fraserlab/swankowicz/190503_Targets/scaping/
  cp ${holo_PDB}_refine_df.csv /wynton/home/fraserlab/swankowicz/190503_Targets/scaping/
  cp ${holo_PDB}_model_v_data.txt /wynton/home/fraserlab/swankowicz/190503_Targets/scaping/
  cp ligand_name.txt /wynton/home/fraserlab/swankowicz/190503_Targets/scaping/
done

cd /wynton/home/fraserlab/swankowicz/190503_Targets/5_9_ligand_data/
files=ls *.csv
#ls grid_search_ens_refine.sh.o* > grid_search_files.txt
output_file=/wynton/home/fraserlab/swankowicz/190503_Targets/ligand_verification.csv
echo $files
for filename in $files; do
  echo $i
  if [[ $i -eq 0 ]] ; then
    # copy csv headers from first file
    echo "first file"
    head -1 $filename > $output_file
  fi
    echo $i "common part"
    # copy csv without headers from other files
    tail -n +2 $filename >> $output_file
    i=$(( $i + 1 ))
done
  #cat /wynton/home/fraserlab/swankowicz/190503_Targets/ligand_verification.csv  $PDB_ligand_verification.csv > /wynton/home/fraserlab/swankowicz/190503_Targets/ligand_verification.csv
