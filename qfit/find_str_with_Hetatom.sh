#!/bin/bash

#________________________________________________SET PATHS________________________________________________#
source /home/wankowicz/phenix-installer-1.16-3546-intel-linux-2.6-x86_64-centos6/phenix-1.16-3546/phenix_env.sh
export PATH="/home/wankowicz/anaconda3/bin:$PATH"
source activate qfit2.1
which python

file=/home/wankowicz/scripts/PDBs_end_101419.txt
while read -r line; do
   mid=$(echo ${line:1:2} | tr '[:upper:]' '[:lower:]')
   line=$(echo ${line} | tr '[:upper:]' '[:lower:]')
   #echo $mid
   echo $line
   if [[ ! -e /data/wankowicz/PDB_092019/fit/mtz/${mid}/${line}.dump  ]]; then
      echo 'no mtz'
      echo $line >> /data/wankowicz/PDB_092019/nomtz_101419.txt
      #mkdir /data/wankowicz/PDB_092019/$line
      #cd /data/wankowicz/PDB_092019/$line
      #phenix.fetch_pdb --mtz $line || wget https://files.rcsb.org/download/${line}-sf.cif
      #phenix.cif_as_mtz ${line}-sf.cif
   else
      if [[  -e /data/wankowicz/PDB_092019/fit/pdb/${mid}/pdb${line}.ent.gz ]]; then
         #echo 'pdb found'
         find_largest_lig /data/wankowicz/PDB_092019/fit/pdb/${mid}/pdb${line}.ent.gz $line
         lig_name=$(cat ${line}_ligand_name.txt)
         #echo $lig_name
         if [ ! -z "$lig_name" ]; then
            #echo 'has ligand!'
            echo $line >> /data/wankowicz/PDB_092019/PDB_2A_res_w_lig_101419.txt
            echo $lig_name >> /data/wankowicz/PDB_092019/PDB_2A_res_w_lig_101419.txt
         fi
      #elif [[ -e /data/wankowicz/PDB_092019/$line/$line.pdb ]]; then
      #   largest_lig=$(find_largest_lig /data/wankowicz/PDB_092019/$line/$line.pdb $line)
            else
         echo 'pdb not found'
         echo $line >> /data/wankowicz/PDB_092019/no_pdb_101319.txt
         #mkdir /data/wankowicz/PDB_092019/$line
         #cd /data/wankowicz/PDB_092019/$line
         #try { 
         #    phenix.fetch_pdb $line }
         #catch {
         #    wget https://files.rcsb.org/download/${line}.cif
         #    phenix.cif_as_pdb ${line}.cif }
         #largest_lig=$(find_largest_lig /data/wankowicz/PDB_092019/$line/$line.pdb $line)
      fi
   fi
done < $file
