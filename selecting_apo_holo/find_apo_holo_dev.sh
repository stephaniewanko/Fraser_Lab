#!/bin/bash

#source /wynton/home/fraserlab/swankowicz/phenix-installer-dev-3594-intel-linux-2.6-x86_64-centos6/phenix-dev-3594/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate qfit3
#which python

   line=$1
   echo $line
   UNIT1=$(grep ${line} /wynton/group/fraser/swankowicz/space_unit_reso_191118.txt | tail -n 1 | sed "s/[(),]//g" | awk '{print $4,$5,$6,$7,$8,$9}')
   UNIT1_out=$UNIT1
   UNIT1=( $UNIT1 )
   UNIT1_0_lower=$(echo "${UNIT1[0]}"-1 | bc -l)
   UNIT1_0_upper=$(echo "${UNIT1[0]}"+1 | bc -l)

   UNIT1_1_lower=$(echo ${UNIT1[1]}-1 | bc -l)
   UNIT1_1_upper=$(echo ${UNIT1[1]}+1 | bc -l)

   UNIT1_2_lower=$(echo ${UNIT1[2]}-1 | bc -l)
   UNIT1_2_upper=$(echo ${UNIT1[2]}+1 | bc -l)

   UNIT1_3_lower=$(echo ${UNIT1[3]}-1 | bc -l)
   UNIT1_3_upper=$(echo ${UNIT1[3]}+1 | bc -l)

   UNIT1_4_lower=$(echo ${UNIT1[4]}-1 | bc -l)
   UNIT1_4_upper=$(echo ${UNIT1[4]}+1 | bc -l)

   UNIT1_5_lower=$(echo ${UNIT1[5]}-1 | bc -l)
   UNIT1_5_upper=$(echo ${UNIT1[5]}+1 | bc -l)
   echo $UNIT1_out
   echo $UNIT1_0_lower
   SEQ1=$(~/anaconda3/envs/qfit3/bin/python /wynton/group/fraser/swankowicz/get_seq.py /wynton/group/fraser/swankowicz/mtz/191114/pdb${line}.ent)
   echo $SEQ1
   file3=/wynton/group/fraser/swankowicz/potential_paris/5d9j_potential_pairs.txt
   for line2 in $(cat $file3); do
       echo $line2
       UNIT2=$(grep ${line2} /wynton/group/fraser/swankowicz/space_unit_reso_191118.txt | tail -n 1 | sed "s/[(),]//g" | awk '{print $4,$5,$6,$7,$8,$9}')
       echo $UNIT2
       UNIT2=( $UNIT2 )
       #echo 'unit2[0]'
       #echo ${UNIT2[0]}
       #echo 'unit1 upper'
       #echo ${UNIT1_0_upper}
       #UNIT2_0=$(echo ${UNIT2[0]}+0 | bc -l)
       #UNIT2_0=$(echo ${UNIT2[0]})
       #echo 'check it out:'
       #echo ${UNIT1_0_upper}
       if (( $(echo "${UNIT2[0]} <= ${UNIT1_0_upper}" |bc -l) )); then
           echo 'FUCKING WORK'
       fi 
       if (( $(echo "${UNIT2[0]} <= ${UNIT1_0_upper}" |bc -l) )) && (( $(echo "${UNIT2[0]} >= ${UNIT1_0_lower}" |bc -l) )) && (( $(echo "${UNIT2[1]} <= ${UNIT1_1_upper}" |bc -l) )) && (( $(echo "${UNIT2[1]} >= ${UNIT1_1_lower}" |bc -l) )) && (( $(echo "${UNIT2[2]} <= ${UNIT1_2_upper}" |bc -l) )) && (( $(echo "${UNIT2[2]} >= ${UNIT1_2_lower}" |bc -l) )); then
              echo 'pair1'
              if (( $(echo "${UNIT2[3]} <= ${UNIT1_3_upper}"|bc -l) )) && (( $(echo "${UNIT2[3]} >= ${UNIT1_3_lower}" |bc -l) )) && (( $(echo "${UNIT2[4]} <= ${UNIT1_4_upper}" |bc -l) )) && (( $(echo "${UNIT2[4]} >= ${UNIT1_4_lower}" |bc -l) )) &&  (( $(echo "${UNIT2[5]} <= ${UNIT1_5_upper}" |bc -l) )) && (( $(echo "${UNIT2[5]} >= ${UNIT1_5_lower}" |bc -l) )); then
                echo 'pair2'
                SEQ2=$(~/anaconda3/envs/qfit3/bin/python /wynton/group/fraser/swankowicz/get_seq.py /wynton/group/fraser/swankowicz/mtz/191114/pdb${line2}.ent)
                echo $SEQ1
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
                     echo 'pair'
                     echo $line
                     echo $SEQ1
                     echo $line2
                     echo $SEQ2
                     echo $line $line2 $RESO1 $RESO2 >> /wynton/group/fraser/swankowicz/PDB_pairs_191119.txt
                   else
                     SEQ1_end5=${SEQ1:-5}
                     SEQ2_end5=${SEQ2:-5}
                     SEQ1_begin5=${SEQ1:5}
                     SEQ2_begin5=${SEQ2:5}
                     if [ "$SEQ1" = "$SEQ2_begin5" ] || [ "$SEQ1" = "$SEQ2_end5" ] || [ "$SEQ2" = "$SEQ1_end5" ] || [ "$SEQ2" = "$SEQ1_begin5" ]; then
                       echo 'pair'
                       echo $line $line2 $RESO1 $RESO2 >> /wynton/group/fraser/swankowicz/PDB_pairs_191119.txt
                     fi
                   fi
              fi
          fi
      fi
   done
  fi
