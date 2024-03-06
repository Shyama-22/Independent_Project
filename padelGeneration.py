import padelpy
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

toxinData = pd.read_excel('padelFinds.xlsx')

def generate(arg):
    try:
        feat = padelpy.from_smiles(arg[0], fingerprints=True)
        feat['pubchemid'] = arg[1]
        feat['smile'] = arg[0]
        return feat
    except:
        print('except', arg)
        return None

data = toxinData
feat = padelpy.from_smiles(data['smile'][0], fingerprints=True)
feat['pubchemid'] = data['pubchemid'][0]
feat['smile'] = data['smile'][0]
padelFeature = pd.DataFrame([feat])
with ThreadPoolExecutor(max_workers = 4) as executor:
    results = executor.map(generate, zip(data['smile'][1:], data['pubchem id'][1:]))
    for result in tqdm (results, desc='extracting'):
        if result:
            padelFeature.loc[len(padelFeature)] = result
padelFeature.to_excel('padelfeatures.xlsx', index=False)
