import padelpy
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# toxinData = pd.read_excel('padelFinds.xlsx')
nontoxinData = pd.read_excel('allnontoxicsmiles.xlsx')
# nontoxinData.rename(columns={'pubchemCID':'pubchemid'}, inplace=True)

def generate(arg):
    try:
        feat = padelpy.from_smiles(arg[0], fingerprints=True)
        feat['pcid'] = arg[1]
        feat['smile'] = arg[0]
        return feat
    except:
        print('except', arg)
        return None

data = nontoxinData
feat = padelpy.from_smiles(data['smile'][0], fingerprints=True)
feat['pcid'] = data['pcid'][0]
feat['smile'] = data['smile'][0]
padelFeature = pd.DataFrame([feat])
with ThreadPoolExecutor(max_workers = 4) as executor:
    results = executor.map(generate, zip(data['smile'][1:], data['pcid'][1:]))
    for result in tqdm (results, desc='extracting'):
        if result:
            padelFeature.loc[len(padelFeature)] = result
padelFeature.to_excel('nontoxicpadelfeatures.xlsx', index=False)
