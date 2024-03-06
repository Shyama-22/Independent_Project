from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.ML.Descriptors import MoleculeDescriptors
import pandas as pd

tosmile = pd.read_excel('toxinSmile.xlsx')
def RDkit_descriptors(datas):
    calc = MoleculeDescriptors.MolecularDescriptorCalculator(map(lambda x : x[0], Descriptors._descList))
    desc_names = list(calc.GetDescriptorNames())
    Mol_descriptors = []
    for data in datas.iterrows():
        data = data[1]
        mol = Chem.MolFromSmiles(data['smile'])
        if mol is not None:
            descriptors = calc.CalcDescriptors(mol)
            descriptors = list(descriptors)
            descriptors.append(data['pubchem id'])
            Mol_descriptors.append(descriptors)
    desc_names.append('pubchemid')
    return Mol_descriptors, desc_names

Mol_descriptors, desc_names = RDkit_descriptors(tosmile)
descriptordf = pd.DataFrame(Mol_descriptors,columns=desc_names)
descriptordf.to_excel('rdkitfeatures.xlsx', index=False)

padelfeatures = pd.read_excel('padelfeatures.xlsx')
rdkitfeatures = pd.read_excel('rdkitfeatures.xlsx')

commonfeatures = set(padelfeatures.columns).intersection(set(rdkitfeatures))
mergedfeatures = padelfeatures.merge(rdkitfeatures, how='outer', on='pubchemid')
commonfeatures = set(padelfeatures.columns).intersection(set(rdkitfeatures))
commonfeatures.remove('pubchemid')

for feat in commonfeatures:
    mergedfeatures[feat] = mergedfeatures[feat + '_x'].combine_first(mergedfeatures[feat + '_y'])
    mergedfeatures = mergedfeatures.drop(feat + '_x', axis=1)
    mergedfeatures = mergedfeatures.drop(feat + '_y', axis=1)

mergedfeatures.to_excel('allfeatures.xlsx', index=False)

