#
   line=$1
   SEQ1=$(grep ${line} /wynton/group/fraser/swankowicz/sequences_missed_191226.txt | head -n 1 | awk '{print $2}')
   echo $SEQ1
   file3=/wynton/group/fraser/swankowicz/pairs_191202/${line}_potential_pairs.txt
   for line2 in $(cat $file3); do
       echo $line2
       RESO2=$(grep ${line2} /wynton/group/fraser/swankowicz/space_unit_reso_191118.txt | head -n 1 | awk '{print $2}')
       SEQ2=$(grep ${line2} /wynton/group/fraser/swankowicz/sequences_missed_191226.txt | head -n 1 | awk '{print $2}')
       echo $SEQ2
       if [[ -z ${SEQ1} ]]; then
              echo 'no seq1'
              exit 1
       elif [[ -z ${SEQ2} ]]; then
             echo 'no seq2'
             continue
       else
             echo $SEQ2
             if [ "$SEQ1" = "$SEQ2" ]; then
                     echo 'final pair'
                     echo $line
                     echo $SEQ1
                     echo $line2
                     echo $SEQ2
                     echo $line $line2 $RESO1 $RESO2 >> /wynton/group/fraser/swankowicz/PDB_pairs_191202.txt
             else
                     SEQ1_end5=${SEQ1:-5}
                     SEQ2_end5=${SEQ2:-5}
                     SEQ1_begin5=${SEQ1:5}
                     SEQ2_begin5=${SEQ2:5}
                     if [ "$SEQ1" = "$SEQ2_begin5" ] || [ "$SEQ1" = "$SEQ2_end5" ] || [ "$SEQ2" = "$SEQ1_end5" ] || [ "$SEQ2" = "$SEQ1_begin5" ]; then
                       echo 'final pair'
                       echo $line $line2 $RESO1 $RESO2 >> /wynton/group/fraser/swankowicz/PDB_pairs_191202.txt
                     fi
             fi
       fi
   done
