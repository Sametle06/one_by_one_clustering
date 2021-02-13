# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 21:29:45 2021

@author: Sameitos
"""

from similarity_functions import similarity_functions
from cluster_function import data_cluster

def cluster_function(data,cutoff,updateReps,function,p):

    sf = similarity_functions(p)
    similarities = {'rdkitTanimoto': sf.rdkitTanimoto, 
                    'Tanimoto':sf.tanimoto,'Euclidean':sf.euclidean,
                    'Manhattan':sf.manhattan,'Minkowski':sf.minkowski,
                    'Cosine':sf.cosine}

    cf = data_cluster()

    if updateReps == 'basic':
        cluster = cf.basic_obo(data,cutoff,similarities[function])
        css = []
        for value in cluster.values():
            css.append(value)
        return css
    elif updateReps == 'mid':
        cluster = cf.mid_obo(data,cutoff,similarities[function])
    elif updateReps == 'deep':
        cluster = cf.deep_obo(data,cutoff,similarities[function])

    css = []
    for value in cluster.values():
        css.append(value[0])
    return css


def obyone(data, 
         cutoff,
         function = 'Euclidean',
         isBit = False,
         updateReps = 'basic',
         p = None):
    """
    Paramters:
        data: A feature dataset
        cutoff: A threshold to form clusters
        function: A similarity function. (default: Euclidean),
                  {Tanimoto, Manhattan, Euclidean, Cosine, Minkowski}
        isBit: A boolean value to indicate whether data is a rdkit.bitvector or not. If True,
               rdkit.DataStructs.BulkTanimotoSimilarity function will be used.
        updateReps: A parameter that decides to how to adjust centers of clusters. (default: ‘basic’), 
                    {‘basic’, ’mid’, ’deep’}.
        	        ‘basic’: No adjustment for center. 1st cluster member is the center
        	        ‘mid’: Adjustment for center based on similarity sum
        	        ‘deep’: Both similarity and number neighbors to adjust center
       	p: p value to calculate Minkowski similarity. (if p = 1: Manhattan, if p = 2: Euclidean similarities)     
    Return:
        results: Indices of dataset points in a cluster. The first element of cluster is the 
                 center of that cluster.
    """
    
    if isBit:
        function = 'rdkitTanimoto'
        results = cluster_function(data,cutoff,updateReps,function,p)
    else:
        results = cluster_function(data,cutoff,updateReps,function,p)
    return results

