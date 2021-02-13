# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 14:13:36 2021

@author: Sameitos
"""

import numpy as np
from rdkit import DataStructs
from scipy.spatial import distance

class similarity_functions():
    
    def __init__(self,p):
        '''
        Parameters:
            p: p value to calculate Minkowski similarity. 
               (if p = 1: Manhattan, if p = 2: Euclidean similarities)
        '''
        self.p = p
    
    def rdkitTanimoto(self,point,others):
        '''
        Parameters:
            p: point to calculate similarity with others
            others: other points
        Return:
            Tanimoto similarity with rdkit package
        '''
        return DataStructs.BulkTanimotoSimilarity(point,others)
            
    def tanimoto(self,point,others):
        '''
        It is used to find similarity between bitvectors({0,1}).  
        Parameters:
            p: point to calculate similarity with others
            others: other points
        Return:
            sims: list of similarities
        '''
        sims = []
        for i in others:
            counter = 0
            for p,o in zip(point,i):
                if p == o: counter +=1
            joint = counter
            union = len(p) + len(o) - joint
            sims.append(joint/union)
            
        return sims
    
    def euclidean(self,point,others):
        '''
        Parameters:
            p: point to calculate similarity with others
            others: other points
        Return:
            sims: list of similarities
        '''
        sims = []
        for i in others:
            sim = 1/(1+np.linalg.norm(point-i))
            sims.append(sim)
            
        return sims
        
    def manhattan(self,point,others):
        '''
        Parameters:
            p: point to calculate similarity with others
            others: other points
        Return:
            Tanimoto similarity with rdkit package
        '''
        sims = []
        for i in others:
            sim = 1/(1+np.linalg.norm(point-i, ord = 1))
            sims.append(sim)
            
        return sims
        
    def minkowski(self,point,others):
        '''
        Parameters:
            p: point to calculate similarity with others
            others: other points
        Return:
            sims: list of similarities
        '''
        sims = []
        for i in others:
            sim = 1/(1 + distance.minkowski(point,i,self.p))
            sims.append(sim)
            
        return sims
        
    def cosine(self,point,others):
        '''
        Parameters:
            p: point to calculate similarity with others
            others: other points
        Return:
            sims: list of similarities
        '''
        sims = []
        for i in others:
            sims.append(1 - distance.cosine(point,i))
        
        return sims

        