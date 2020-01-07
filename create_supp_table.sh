file=/wynton/group/fraser/swankowicz/script/qfit_pairs_191218.txt
while read p; do
   #echo "$p"
   arr=($p)
   Holo=$(echo ${arr[0]})
   Apo=$(echo ${arr[1]})
   Holo_Res=$(echo ${arr[2]})
   Apo_Res=$(echo ${arr[3]})
   lig_name=$(grep -A 1 ${Holo} /wynton/group/fraser/swankowicz/PDB_2A_lig_name_111419.txt)
   echo $Apo $Apo_Res $Holo $Holo_Res $lig_name >> ligand_supplementary_table1.txt
done </wynton/group/fraser/swankowicz/script/qfit_pairs_191218.txt


