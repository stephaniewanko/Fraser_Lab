#!/usr/bin/env python
#last edited: 2019-04-12
#last edited by: Stephanie Wankowicz

import pandas as pd
import os
import datetime
import argparse
import sys


#parse refinement output .log
def parse_refine_log(file):
    file=open(file, 'r') #take this in as an arguement
    global refine_df
    refine_df=pd.DataFrame(columns=['PDB','Date', 'Starting_Rfree', 'Ending_Rfree', 'Starting_Rwork', 'Ending_Rwork', 'Number of Refinement', 'delta_Rwork', 'delta_Rfree'])
    now = datetime.datetime.now()
    for line in file:
        if line.startswith('Command line arguments'):
            #print(line)
            pdb_name=line.split('.')[0][-4:]
            #print(pdb_name)
        elif line.startswith('Start R-work'):
            start_rwork=float(line.split('=')[1][1:7])
            start_rfree=float(line.split('=')[2][1:7])
            #print(start_rfree)
        elif line.startswith('Final R-work'):
            final_rwork=float(line.split('=')[1][1:7])
            final_rfree=float(line.split('=')[2][1:7])
    refine_df.loc[1,'PDB']=pdb_name
    refine_df.loc[1,'Starting_Rfree']=start_rfree
    refine_df.loc[1,'Ending_Rfree']=final_rfree
    refine_df.loc[1,'Starting_Rwork']=start_rwork
    refine_df.loc[1,'Ending_Rwork']=final_rwork
    refine_df.loc[1,'Number of Refinement']=2
    refine_df.loc[1,'delta_Rwork'] = refine_df.loc[1,'Starting_Rwork']-refine_df.loc[1,'Ending_Rwork']
    refine_df.loc[1, 'R_Rfree_start']=refine_df.loc[1,'Starting_Rwork']-refine_df.loc[1,'Starting_Rfree']
    refine_df.loc[1, 'R_Rfree_end']=refine_df.loc[1,'Ending_Rwork']-refine_df.loc[1,'Ending_Rfree']
    refine_df.loc[1,'delta_Rfree'] = refine_df.loc[1,'Starting_Rfree']-refine_df.loc[1,'Ending_Rfree']
    #refine_df.loc[1, 'Rfree_thres']=((float(refine_df.loc[1,'Starting_Rfree'])*0.02)+float(refine_df.loc[1,'Starting_Rfree']))
    #refine_df.loc[1,'Rdiff_thres']=((float(refine_df.loc[1,'R_Rfree_start'])*0.02)+float(refine_df.loc[1,'R_Rfree_start']))
    refine_df.loc[1,'Date']=now.strftime("%Y-%m-%d")
    print(pdb_name)
    return pdb_name

def heuristics_pass(refine_df):
    #Rfree cannot be 2% worse then input Rfree
    Rfree_thres=((float(refine_df.loc[1,'Starting_Rfree'])*0.02)+float(refine_df.loc[1,'Starting_Rfree']))
    #R-Rfree cannot 2% be worse then input
    print(Rfree_thres)
    Rdiff_thres=((float(refine_df.loc[1,'R_Rfree_start'])*0.02)+float(refine_df.loc[1,'R_Rfree_start']))
    print(Rdiff_thres)
    print('Division:')
    #print()
    if ((float(refine_df.loc[1,'Starting_Rfree']))/(float(refine_df.loc[1,'Ending_Rfree'])))<2:
        if ((float(refine_df.loc[1,'R_Rfree_start']))/(float(refine_df.loc[1,'R_Rfree_end']))) < 2:
            print('Passed')
            with open('threshold.txt', 'w') as file:
                file.write('Passed')
        else:
            print('Failed')
            with open('threshold.txt', 'w') as file:
                file.write("Failed")#. \n Rfree_Threshold: {}, Ending_Rfree: {}\n Rdiff_Threshold: {}, Ending R Diff:{}".format(Rfree_thres, (float(refine_df.loc[1,'Ending_Rfree'])),(float(refine_df.loc[1,'Ending_Rfree'])), Rdiff_thres,(float(refine_df.loc[1,'R_Rfree_end']))))
    else:
        print('Failed')
        #print ('Failed', 'Rfree Thresold:', Rfree_thres, 'Ending Rfree:', (float(refine_df.loc[1,'Ending_Rfree'])), 'Rdiff Threshold:', Rdiff_thres, 'Ending R Diff:', (float(refine_df.loc[1,'R_Rfree_end']), file=outfile.txt)
        with open('threshold.txt', 'w') as file:
            file.write("Failed")#. \n Rfree_Threshold: {}, Ending_Rfree: {}\n Rdiff_Threshold: {}, Ending R Diff:{}".format(Rfree_thres, (float(refine_df.loc[1,'Ending_Rfree'])),(float(refine_df.loc[1,'Ending_Rfree'])), Rdiff_thres,(float(refine_df.loc[1,'R_Rfree_end']))))
            #file.write('{0}\n {1} {2}\n {3} {4}\n {5} {6}\n {7} {8}\n'.format('Failed', 'Rfree Thresold:', Rfree_thres, 'Ending Rfree:', (float(refine_df.loc[1,'Ending_Rfree'])), 'Rdiff Threshold:', Rdiff_thres, 'Ending R Diff:', (float(refine_df.loc[1,'R_Rfree_end']))))
            #file.write('Failed')
            #file.write(Rfree_thres)
            #file.write(float(refine_df.loc[1,'Ending_Rfree']))
            #file.write(Rdiff_thres)
            #file.write(float(refine_df.loc[1,'R_Rfree_end']))


def main(file):
    PDB=parse_refine_log(file)
    heuristics_pass(refine_df)
    refine_df.to_csv(PDB + '_refine_df.csv')
    print(float(refine_df.loc[1,'R_Rfree_start']))
    print(float(refine_df.loc[1,'R_Rfree_end']))
    #return('Continue')
    sys.exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    main(args.filename)
