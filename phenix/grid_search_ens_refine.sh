#!/bin/bash
#grid search for ensemble_refinement
#Stephanie Wankowicz 4/15/2019


# we are going to do a grid search of a bunch of different
#perform grid search: pTLS: 1.0, 0.8, 0.6; weights: wxray_coupled_tbath_offset=2.5;5.0;10.0; timestep always 1.0
#put in job_title and output_dir based on grid search
#we are then going to determine which output is better and remove the files related to the poorer output.


##TO ADD: Some log file with Rfree of all ensemble_refinements

echo'________________________________________________________Running the Original Ensemble Refinement (pTLS=1.0; Weights=2.5)________________________________________________________'

phenix.ensemble_refinement ${PDB}.updated_refine_001.pdb ${PDB}-sf.mtz elbow.${PDB}_pdb.001.cif pTLS=1.0 wxray_coupled_tbath_offset=2.5 ts=1.0 output_file_prefix=${PDB}_pTLS1_weights2.5
#establishing the Baseline
Baseline=${PDB}_pTLS1_weights2.5.${PDB}.updated_ensemble.log
Baseline_name=_pTLS1_weights2.5

echo'________________________________________________________Running Ensemble Refinement (pTLS=1.0; Weights=5.0)________________________________________________________'
phenix.ensemble_refinement ${PDB}.updated_refine_001.pdb ${PDB}-sf.mtz elbow.${PDB}_pdb.001.cif pTLS=1.0 wxray_coupled_tbath_offset=5.0 ts=1.0 output_file_prefix=${PDB}_pTLS1_weights5

echo'________________________________________________________Determining which Ensemble Refinement is SUPERIOR!________________________________________________________'
#determine which one is better
python /Users/fraserlab/Documents/Stephanie/ens_refine_gridsearch.py $Baseline ${PDB}_pTLS1_weithts5.${PDB}.updated_ensemble.log

grid_var=$(cat "ensemble_grid_search.txt") #delete the outputs and save the next one as the Baseline
echo $grid_var

if [ "$grid_var" = "Passed" ]; then #if passed then we need to set a new baseline
  Baseline=${PDB}_pTLS1_weights5.${PDB}.updated_ensemble.log
  Baseline_name=_pTLS1_weights5
  rm *$Baseline_name*
else
  echo "Keeping the same baseline"
  rm ${PDB}_pTLS1_weights5*
fi



echo'________________________________________________________Running Ensemble Refinement (pTLS=1.0; Weights=10.0)________________________________________________________'
phenix.ensemble_refinement ${PDB}.updated_refine_001.pdb ${PDB}-sf.mtz elbow.${PDB}_pdb.001.cif pTLS=1.0 wxray_coupled_tbath_offset=10.0 ts=1.0 output_file_prefix=${PDB}_pTLS1_weights10

echo'________________________________________________________Determining which Ensemble Refinement is SUPERIOR!________________________________________________________'
python /Users/fraserlab/Documents/Stephanie/ens_refine_gridsearch.py $Baseline ${PDB}_pTLS1_weithts10.${PDB}.updated_ensemble.log
grid_var=$(cat "ensemble_grid_search.txt")
echo $grid_var

if [ "$grid_var" = "Passed" ]; then #if passed then we need to set a new baseline
  Baseline=${PDB}_pTLS1_weights5.${PDB}.updated_ensemble.log
  Baseline_name=_pTLS1_weights5
  rm *$Baseline_name*
else
  echo "Keeping the same baseline"
  rm ${PDB}_pTLS1_weights10*
fi


echo'________________________________________________________Running Ensemble Refinement (pTLS=1.0; Weights=5.0)________________________________________________________'
phenix.ensemble_refinement ${PDB}.updated_refine_001.pdb ${PDB}-sf.mtz elbow.${PDB}_pdb.001.cif pTLS=0.8 wxray_coupled_tbath_offset=2.5 ts=1.0 output_file_prefix=${PDB}_pTLS0.8_weights2.5

echo'________________________________________________________Determining which Ensemble Refinement is SUPERIOR!________________________________________________________'
python /Users/fraserlab/Documents/Stephanie/ens_refine_gridsearch.py $Baseline ${PDB}_pTLS0.8_weights2.5.${PDB}.updated_ensemble.log
grid_var=$(cat "ensemble_grid_search.txt")
echo $grid_var

if [ "$grid_var" = "Passed" ]; then #if passed then we need to set a new baseline
  Baseline=${PDB}_pTLS0.8_weights2.5.${PDB}.updated_ensemble.log
  rm *$Baseline_name*
else
  echo "Keeping the same baseline"
  rm ${PDB}_pTLS0.8_weights2.5*
fi



echo'________________________________________________________Determining which Ensemble Refinement is SUPERIOR!________________________________________________________'
python /Users/fraserlab/Documents/Stephanie/ens_refine_gridsearch.py $Baseline ${PDB}_pTLS1_weithts10.${PDB}.updated_ensemble.log
grid_var=$(cat "ensemble_grid_search.txt")
echo $grid_var

if [ "$grid_var" = "Passed" ]; then #if passed then we need to set a new baseline
  Baseline=${PDB}_pTLS1_weithts5.${PDB}.updated_ensemble.log
  rm ${PDB}_pTLS1_weights2.5*
else
  echo "Keeping the same baseline"
  rm ${PDB}_pTLS1_weights5*
fi


echo'________________________________________________________Running Ensemble Refinement (pTLS=1.0; Weights=5.0)________________________________________________________'
phenix.ensemble_refinement ${PDB}.updated_refine_001.pdb ${PDB}-sf.mtz elbow.${PDB}_pdb.001.cif pTLS=0.8 wxray_coupled_tbath_offset=5.0 ts=1.0 output_file_prefix=${PDB}_pTLS0.8_weights5
echo'________________________________________________________Running Ensemble Refinement (pTLS=1.0; Weights=5.0)________________________________________________________'
phenix.ensemble_refinement ${PDB}.updated_refine_001.pdb ${PDB}-sf.mtz elbow.${PDB}_pdb.001.cif pTLS=0.8 wxray_coupled_tbath_offset=10.0 ts=1.0 output_file_prefix=${PDB}_pTLS0.8_weights10
echo'________________________________________________________Running Ensemble Refinement (pTLS=1.0; Weights=5.0)________________________________________________________'
phenix.ensemble_refinement ${PDB}.updated_refine_001.pdb ${PDB}-sf.mtz elbow.${PDB}_pdb.001.cif pTLS=0.6 wxray_coupled_tbath_offset=2.5 ts=1.0 output_file_prefix=${PDB}_pTLS0.6_weights2.5
echo'________________________________________________________Running Ensemble Refinement (pTLS=1.0; Weights=5.0)________________________________________________________'
phenix.ensemble_refinement ${PDB}.updated_refine_001.pdb ${PDB}-sf.mtz elbow.${PDB}_pdb.001.cif pTLS=0.6 wxray_coupled_tbath_offset=5.0 ts=1.0 output_file_prefix=${PDB}_pTLS0.6_weights5
echo'________________________________________________________Running Ensemble Refinement (pTLS=1.0; Weights=5.0)________________________________________________________'
phenix.ensemble_refinement ${PDB}.updated_refine_001.pdb ${PDB}-sf.mtz elbow.${PDB}_pdb.001.cif pTLS=0.6 wxray_coupled_tbath_offset=10.0 ts=1.0 output_file_prefix=${PDB}_pTLS0.6_weights10
