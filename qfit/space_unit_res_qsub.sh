#!/bin/bash

source /home/wankowicz/phenix-installer-1.16-3546-intel-linux-2.6-x86_64-centos6/phenix-1.16-3546/phenix_env.sh
#export PATH="/home/wankowicz/anaconda3/bin:$PATH"
source activate qfit2.1
which python


line=$1
mid=$(echo ${line:1:2})
SPACE1=$(grep "^Space group number from file:" /data/wankowicz/PDB_092019/fit/mtz/${mid}/${line}.dump | awk '{print $6,$7}')
UNIT1=$(grep "Unit cell:" /data/wankowicz/PDB_092019/fit/mtz/${mid}/${line}.dump | tail -n 1 | sed "s/[(),]//g" | awk '{print $3,$4,$5,$6,$7,$8}')
RESO1=$(grep "^Resolution" /data/wankowicz/PDB_092019/fit/mtz/${mid}/${line}.dump | head -n 1 | awk '{print $4}')

line2=$2
mid2=$(echo ${line2:1:2})
SPACE2=$(grep "^Space group number from file:" /data/wankowicz/PDB_092019/fit/mtz/${mid2}/${line2}.dump | awk '{print $6}')
UNIT2=$(grep "Unit cell:" /data/wankowicz/PDB_092019/fit/mtz/${mid2}/${line2}.dump | tail -n 1 | sed "s/[(),]//g" | awk '{print $3,$4,$5,$6,$7,$8}')
RESO2=$(grep "^Resolution" /data/wankowicz/PDB_092019/fit/mtz/${mid2}/${line2}.dump | head -n 1 | awk '{print $4}')

RESO1_lower=$(echo ${RESO1}-0.1 | bc -l)
RESO1_upper=$(echo ${RESO1}+0.1 | bc -l)

#echo $RESO1_upper
#echo $RESO1_lower
echo $RESO1
echo $RESO2
echo $UNIT1
echo $UNIT2
echo $SPACE1
echo $SPACE2

UNIT1_out=$UNIT1
UNIT2_out=$UNIT2
UNIT1=( $UNIT1 )
UNIT2=( $UNIT2 )

UNIT1_0_lower=$(echo ${UNIT1[0]}-1 | bc -l)
UNIT1_0_upper=$(echo ${UNIT1[0]}+1 | bc -l)

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


echo $UNIT1_2_upper
echo $UNIT1_2_lower

if (( `echo ${RESO2}'<='${RESO1_upper} | bc` )) && (( `echo ${RESO2}'>='${RESO1_lower} | bc` )); then
   echo 'pair'
   if [ $SPACE1 == $SPACE2 ]; then
      echo 'pair2'
      if (( `echo ${UNIT2[3]}'<='${UNIT1_3_upper} | bc` )) && (( `echo ${UNIT2[3]}'>='${UNIT1_3_lower} | bc` )) && (( `echo ${UNIT2[4]}'<='${UNIT1_4_upper} | bc` )) && (( `echo ${UNIT2[4]}'>='${UNIT1_4_lower} | bc` )) && (( `echo ${UNIT2[5]}'<='${UNIT1_5_upper} | bc` )) && (( `echo ${UNIT2[5]}'>='${UNIT1_5_lower} | bc` )); then
         echo 'pair3'
         if (( `echo ${UNIT2[0]}'<='${UNIT1_0_upper} | bc` )) && (( `echo ${UNIT2[0]}'>='${UNIT1_0_lower} | bc` )) && (( `echo ${UNIT2[1]}'<='${UNIT1_1_upper} | bc` )) && (( `echo ${UNIT2[1]}'>='${UNIT1_1_lower} | bc` )) && (( `echo ${UNIT2[2]}'<='${UNIT1_2_upper} | bc` )) && (( `echo ${UNIT2[2]}'>='${UNIT1_2_lower} | bc` )); then
            echo 'pair4'
            echo $line $line2 $RESO1 $RESO2 $SPACE1 $SPACE2 $UNIT1_out $UNIT2_out >> /home/wankowicz/scripts/PDB_pairs_191022_qsub.txt
            #echo $SPACE1 $SPACE2 $UNIT1_out $UNIT2_out >> /home/wankowicz/scripts/PDB_pairs_191022_qsub.txt  
         fi
      fi
   fi
   #echo $line $line2 $RESO1 $RESO2 >> /data/wankowicz/PDB_092019/PDB_pairs_191015_qsub.txt
   #echo $line $line2 $RESO1 $RESO2 >> /data/wankowicz/PDB_092019/PDB_pairs_191015_qsub.txt

fi
