import pandas as pd
import pubchempy as pcp

nonToxicCompound = pd.read_excel('non-toxicCompounds.xlsx', index_col=0)

nonToxicCompound = nonToxicCompound[['Substance']]
nonToxicCompound['smiles'] = None
nonToxicCompound['compName'] = None
nonToxicCompound['pubchemCID'] = None

total = nonToxicCompound

for i, row in total.iterrows():
    if total.at[i, 'smiles'] == None:
        try:
            res = pcp.get_compounds(row['Substance'], 'name')
            if res != []:
                total.at[i, 'pubchemCID'] = res[0].cid
                total.at[i, 'compName'] = res[0].iupac_name
                total.at[i, 'smiles'] = res[0].canonical_smiles
        except:
            print(total.at[i, 'Substance'])
    if total.at[i, 'smiles'] == None:
        try:
            res = pcp.get_substances(row['Substance'], 'name')
            if res != []:
                total.at[i, 'pubchemCID'] = res[0].standardized_compound.cid
                total.at[i, 'compName'] = res[0].standardized_compound.iupac_name
                total.at[i, 'smiles'] = res[0].standardized_compound.canonical_smiles
        except:
            print(total.at[i, 'Substance'])

total.to_excel('non-toxic-smiles.xlsx')
total.to_csv('non-toxic-smiles.csv')

