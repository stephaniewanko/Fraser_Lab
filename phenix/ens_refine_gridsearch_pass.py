#!/usr/bin/env python
#last edited: 2019-04-16
#last edited by: Stephanie Wankowicz

import pandas as pd
import os
import datetime
import argparse
import sys


def grid_search_pass(log_file1, log_file2): #put in 2 log files
    base_file=open(log_file1, 'r')
    Rfree_new=''
    Rfree_baseline=''
    for line in base_file:
        if line.startswith('FINAL'):
            #print(line)
            Rfree_baseline=line.split('=')[2][1:7]
            print('Original Rfree:')
            print(Rfree_baseline)
    new_file=open(log_file2, 'r')
    for line in new_file:
        if line.startswith('FINAL'):
            #print(line)
            Rfree_new=line.split('=')[2][1:7]
            print('New Rfree:')
            print(Rfree_new)
    with open('ensemble_refinement_grid_search_tracker.txt', 'w') as file_tracker:
        file_tracker.write('Rfree_old: {1}, Rfree_new: {2}\n'.format(Rfree_old, Rfree_new))
        file_tracker.write('{0}\n {1} {2}\n {3} {4}\n {5} {6}\n {7} {8}\n'.format('Failed', 'Rfree Thresold:',
    if Rfree_baseline>=Rfree_new: #if the Rfree is lower in the new ensemble_refinement, we want to replace it
        with open('ensemble_grid_search.txt', 'w') as file:
            file.write("Passed")

def main(log_file1, log_file2):
    grid_search_pass(log_file1, log_file2)
    sys.exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('Baseline', help='The original/baseline Ensemble Refinement File.')
    parser.add_argument('New', help='The Ensemble Refinement File that you want to compare to see if it is superior')
    args = parser.parse_args()
    main(args.Baseline, args.New)
