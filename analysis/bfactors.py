args = parse_args()
B_factor = pd.DataFrame()
atom_name = []
chain_ser = []
residue_name = []
b_factor = []
residue_num = []
model_number = []

for model in Bio.PDB.PDBParser().get_structure(args.pdb_name, args.pdb):
    for chain in model.get_list():
        for residue in chain.get_list():
            for atom in residue.get_list():
                model_number.append(model)
                atom_name.append(atom.get_name())
                chain_ser.append(chain.get_id())
                residue_name.append(str(residue)[9:13])
                #print(str(residue)[9:13])
                residue_num.append(residue.get_full_id()[3][1])
                b_factor.append(atom.get_bfactor())
                n=+1

B_factor['Atom'] = atom_name
B_factor['Chain'] = chain_ser
B_factor['residue'] = residue_name
B_factor['residue_num'] = residue_num
B_factor['B_factor'] = b_factor
B_factor['model'] = model_number
B_factor['PDB_name'] = args.pdb_name
B_factor.to_csv(args.pdb_name+'_B_factors.csv', index=False)
