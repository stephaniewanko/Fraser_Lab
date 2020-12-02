#Figure Functions
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

#reference files
os.chdir('/Users/stephaniewankowicz/Downloads/qfit/pair_docs/')
pairs = pd.read_csv('ligand_supplementary_table1.txt', sep=' ', header=None)
pairs = pairs.rename(columns={0: "Apo", 1: "Apo_Res", 2: "Holo", 3: "Holo_Res", 5:"Ligand"})
AH_pairs = pairs.drop_duplicates()

os.chdir('/Users/stephaniewankowicz/Downloads/qfit/pair_docs/')
AH_key=pd.read_csv('qfit_AH_key_191218.csv')

def paired_ttest(holo_col, apo_col):
	print(stats.wilcoxon(holo_col, apo_col))

	print('Holo Mean:')
	print(holo_col.mean())

	print('Apo Mean:')
	print(apo_col.mean())

	print('Holo Median:')
	print(holo_col.median())

	print('Apo Median:')
	print(apo_col.median())



def ind_MannWhit(col_1, col_2):
	print(stats.mannwhitneyu(col_1, col_2))

	print('Column 1 Mean:')
	print(col_1.mean())

	print('Column 2 Mean:')
	print(col_2.mean())

	print('Column 1 Median:')
	print(col_1.median())

	print('Column 2 Median:')
	print(col_2.median())



def merge_apo_holo_df(df):
	df = df.merge(AH_key, on=['PDB'])
	df_holo = df[df['Apo_Holo'] == 'Holo']
	df_apo = df[df['Apo_Holo'] == 'Apo']
	test = df_holo.merge(AH_pairs, left_on='PDB', right_on='Holo')
	df_merged = test.merge(df_apo, left_on=['Apo', 'chain', 'resi'], right_on=['PDB', 'chain', 'resi'])  
	df_merged = df_merged.drop_duplicates()
	return df_merged



def make_dist_plot_AH(holo_col, apo_col, x_label, y_label, title, out_name):
    fig = plt.figure()
    sns.distplot(holo_col, kde=False, label='Bound')
    #sns.kdeplot(holo_col, label='Bound', bw=0.02)
    #sns.kdeplot(apo_col, label='Unbound', bw=0.02)
    sns.distplot(apo_col, kde=False, label='Unbound')
    plt.xlabel(x_label)
    plt.legend()
    plt.ylabel(y_label)
    plt.title(title)
    fig.savefig(out_name + '.png')

def make_boxenplot_AH(holo_col, apo_col, xlabel, ylabel, title, out_name):
	fig = plt.figure()
	x = range(2)
	f, axes = plt.subplots(1, 2, sharey=True, sharex=True)
	p1 = sns.boxenplot(holo_col, orient='v', ax=axes[0]).set(xlabel = 'Bound', ylabel = ylabel)
	p2 = sns.boxenplot(apo_col, orient='v', ax=axes[1]).set(xlabel = 'Unbound', ylabel = '')
	plt.savefig(out_name + '.png')


def make_boxenplot_chem(low_col, high_col, xlabel_low, xlabel_high, ylabel, out_name):
	fig = plt.figure()
	x = range(2)
	f, axes = plt.subplots(1, 2, sharey=True, sharex=True)
	p1 = sns.boxenplot(low_col, orient='v', ax=axes[0]).set(xlabel = xlabel_low, ylabel = ylabel)
	p2 = sns.boxenplot(high_col, orient='v', ax=axes[1]).set(xlabel = xlabel_high, ylabel = '')
	plt.savefig(out_name + '.png')
	#plt.show()


def rotamer_compare(subset_rotamer):
	AH_rotamer = pd.DataFrame()
	n=1
	for i in AH_pairs['Holo']:
		#print(i)
		apo_list = AH_pairs[AH_pairs['Holo'] == i]['Apo'].unique()
		tmp = subset_rotamer[subset_rotamer['PDB'] == i]
		if tmp.empty == True:
			continue
		else:
			for a in apo_list:
				apo = subset_rotamer[subset_rotamer['PDB'] == a]
				if apo.empty == True:
					continue
				else:
					for r in apo['chain_resi'].unique():
						num_alt_loc_a= len(apo[apo['chain_resi'] == r].index)
						if r in tmp['chain_resi'].unique():
							num_alt_loc_h= len(tmp[tmp['chain_resi'] == r].index)
							if num_alt_loc_h > 1 or num_alt_loc_a > 1:
								for alt in tmp[tmp['chain_resi'] == r]['altloc'].unique():
									for alt2 in apo[apo['chain_resi'] == r]['altloc'].unique():
										AH_rotamer.loc[n, 'Holo'] = i
										AH_rotamer.loc[n, 'Apo'] = a
										AH_rotamer.loc[n, 'chain_resi'] = r
										AH_rotamer.loc[n, 'Apo_alt_loc'] = num_alt_loc_a
										AH_rotamer.loc[n, 'Holo_alt_loc'] = num_alt_loc_h
										AH_rotamer.loc[n, 'Holo_alt_loc_name'] = alt
										AH_rotamer.loc[n, 'Apo_alt_loc_name'] = alt2
										tmp_alt = tmp[(tmp['chain_resi'] == r) & (tmp['altloc'] == alt)]
										apo_alt = apo[(apo['chain_resi'] == r) & (apo['altloc'] == alt2)]
										AH_rotamer.loc[n, 'Apo_Rotamer'] = apo_alt[apo_alt['chain_resi'] == r]['rotamer'].unique()
										AH_rotamer.loc[n, 'Holo_Rotamer'] = tmp_alt[tmp_alt['chain_resi'] == r]['rotamer'].unique()
										if (apo_alt['rotamer'].unique() == tmp_alt['rotamer'].unique()).all() == True:
											AH_rotamer.loc[n, 'rotamer'] = 'Same'
										else:                                              
											AH_rotamer.loc[n, 'rotamer'] = 'Different'
										n+=1
							else:
								AH_rotamer.loc[n, 'Holo'] = i
								AH_rotamer.loc[n, 'Apo'] = a
								AH_rotamer.loc[n, 'chain_resi'] = r
								AH_rotamer.loc[n, 'Apo_alt_loc'] = num_alt_loc_a
								AH_rotamer.loc[n, 'Holo_alt_loc'] = num_alt_loc_h
								AH_rotamer.loc[n, 'Apo_Rotamer'] = apo[apo['chain_resi'] == r]['rotamer'].unique()
								AH_rotamer.loc[n, 'Holo_Rotamer'] = tmp[tmp['chain_resi'] == r]['rotamer'].unique()
								if (apo[apo['chain_resi'] == r]['rotamer'].unique() == tmp[tmp['chain_resi'] == r]['rotamer'].unique()).all() == True:
									AH_rotamer.loc[n, 'rotamer'] = 'Same'
								else:
									AH_rotamer.loc[n, 'rotamer'] = 'Different'
								n += 1
	return AH_rotamer

def rotamer_AH_summary(multi, AH_rotamer_singlealt):
	AH_rotamer_summary_multi = pd.DataFrame()
	n=0
	for i in multi['Holo'].unique():
		tmp = multi[multi['Holo']==i]
		for a in tmp['Apo'].unique():
			tmp2 = tmp[tmp['Apo']== a]
			for res in tmp2['chain_resi'].unique():
				AH_rotamer_summary_multi.loc[n, 'chain_resi'] = res
				AH_rotamer_summary_multi.loc[n, 'Holo'] = i
				AH_rotamer_summary_multi.loc[n, 'Apo'] = a
				if len(tmp2[tmp2['chain_resi']==res]['rotamer'].unique())==1:
					#print(type(tmp2[tmp2['chain_resi']==res]['rotamer'].unique()))
					AH_rotamer_summary_multi.loc[n, 'Rotamer'] = str(tmp2[tmp2['chain_resi']==res]['rotamer'].unique())
				else:
					AH_rotamer_summary_multi.loc[n, 'Rotamer'] = 'Same and Different'
				n += 1
	
	AH_rotamer_summary_single = pd.DataFrame()
	n = 1
	for i in AH_rotamer_singlealt['Holo'].unique():
		tmp = AH_rotamer_singlealt[AH_rotamer_singlealt['Holo'] == i]
		for a in tmp['Apo'].unique():
			tmp2 = tmp[tmp['Apo'] == a]
			for res in tmp2['chain_resi'].unique():
				AH_rotamer_summary_single.loc[n, 'Holo'] = i
				AH_rotamer_summary_single.loc[n, 'Apo'] = a
				AH_rotamer_summary_single.loc[n, 'chain_resi'] = res
				AH_rotamer_summary_single.loc[n, 'Rotamer'] = str(tmp2[tmp2['chain_resi']==res]['rotamer'].unique())
				n += 1

	AH_rotamer_summary_single['Rotamer'] = AH_rotamer_summary_single.Rotamer.str.replace('[','')
	AH_rotamer_summary_single['Rotamer'] = AH_rotamer_summary_single.Rotamer.str.replace(']','')
	AH_rotamer_summary_single['Rotamer'] = AH_rotamer_summary_single.Rotamer.str.replace("\'", '')
	
	AH_rotamer_summary_multi['Rotamer'] = AH_rotamer_summary_multi.Rotamer.str.replace('[','')
	AH_rotamer_summary_multi['Rotamer'] = AH_rotamer_summary_multi.Rotamer.str.replace("\'", '')
	AH_rotamer_summary_multi['Rotamer'] = AH_rotamer_summary_multi.Rotamer.str.replace(']','')

	return AH_rotamer_summary_multi, AH_rotamer_summary_single

def rotamer_summary_AH(subset_rotamer_holo):
	summary = pd.DataFrame()
	n = 1 
	for i in subset_rotamer_holo['PDB'].unique():
		for res in subset_rotamer_holo[subset_rotamer_holo['PDB'] == i]['chain_resi'].unique():
			summary.loc[n,'PDB'] = i
			summary.loc[n,'Residue'] = res
			tmp = subset_rotamer_holo[(subset_rotamer_holo['chain_resi'] == res) & (subset_rotamer_holo['PDB'] == i)]
			summary.loc[n,'num_altloc'] = len(tmp.index)
			if len(tmp[tmp['chain_resi'] == res]['rotamer'].unique()) == 1:
				summary.loc[n,'Rotamer_Status'] = 'same'
			else:
				summary.loc[n,'Rotamer_Status'] = 'different'
			n += 1
	return summary
