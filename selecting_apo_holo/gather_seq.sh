file=/wynton/group/fraser/swankowicz/PDB_2A_noligand.txt
for line in $(cat $file); do
   #line=$(echo ${line} | tr '[:upper:]' '[:lower:]')
   mid=$(echo ${line:1:2})
   echo $line
   SEQ1=$(~/anaconda3/envs/qfit3/bin/python /wynton/group/fraser/swankowicz/get_seq.py /wynton/group/fraser/swankowicz/mtz/191114/pdb${line}.ent)
   echo $line $SEQ1 >> /wynton/group/fraser/swankowicz/sequences_all.txt
done
