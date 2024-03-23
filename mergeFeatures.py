import pandas as pd
import numpy as np

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

