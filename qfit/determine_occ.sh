#!/bin/bash

input_pdb=$1;

occupancies=$(cut -c 55-60 $input_pdb)
echo $1
echo $occupancies
