#!/bin/bash
#git: 01-05-2021
#Stephanie Wankowicz

'''
This script will allow you to determine which ensemble from the grid search has the best Rfree. This can come from the output file from the qsub command or from the log file.
'''

base_dir='/wynton/home/fraserlab/swankowicz/' #where the log files are located
cd ${base_di}
ls grid_search_ens_refine.sh.o* > grid_search_files.txt #first grab all the files in the base directory that are grid search

files=grid_search_files.txt
while read -r line; do
  cd $base_dir
  _file=$line
  python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_refine_parser.py $_file
  output_location=$(cat "output_location.txt")
  echo $_file
  echo $output_location
  echo "$_file" | tr sh.o sh.e
done < $files
