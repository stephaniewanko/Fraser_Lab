#!/bin/bash
#git: 07-12-2019
#Stephanie Wankowicz
#19-05-05

#first grab all the files in the base directory that are grid_search

base_dir='/wynton/home/fraserlab/swankowicz/'
cd $base_dir
ls grid_search_ens_refine.sh.o* > grid_search_files.txt

files=grid_search_files.txt
while read -r line; do
  cd $base_dir
  _file=$line
  python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_refine_parser.py $_file
  output_location=$(cat "output_location.txt")
  echo $_file
  echo $output_location
  #mv $_file $output_location
  #replace $file with e
  echo "$_file" | tr sh.o sh.e
  #err_file="$_file" | tr sh.o sh.e
  #mv $err_file $output_location
done < $files

#now do the same for regular phenix output
  #grab ligand info
  #grab rfree info

#if $1=yes:
  #go to folder and rbind the ligand info
  #go to folder and rbind the ens_output_info
