# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 15:30:58 2021

@author: Sameitos
"""


import numpy as np
from tqdm import tqdm
from sklearn.preprocessing import binarize


class data_cluster():
    
    def __init__(self):
        pass
        
    def basic_obo(self,data,cutoff,function):
        """
        There is no mutable center of cluster to not slow down the cluster
    
        Parameters:
            data: BitVector of Molecules
            cutoff: cutoff: Threshold to cluster the points
            
        Return:
            reps: Representatives of each cluster
        """
        
        cluster = {}
        cluster.update({0:[0]})
        for k,p in enumerate(tqdm(data[1:])):
            
            point = k + 1
            centers = list(cluster.keys())
            sim = function(p,[data[center] for center in centers])
            max_sim = max(sim)
            if max_sim < cutoff:
                cluster.update({point:[point]})
            else:
                center = centers[sim.index(max_sim)]
                cluster[center].append(point)
                
        return cluster
    
    def mid_obo(self,data,cutoff,function):
        """
        Centers of clusters are mutable according to only similarity to get more realistic clustering result 
        
        Parameters:
            data: BitVector of Molecules
            cutoff: cutoff: Threshold to cluster the points
            
        Return:
            reps: Representatives of each cluster
        """
        
        cluster = {}
        cluster.update({0:[[0],[0]]})
        for k,p in enumerate(tqdm(data[1:])):
            
            point = k + 1
            centers = list(cluster.keys())
            sim = function(p,[data[center] for center in centers])
            max_sim = max(sim)
           
            if max_sim < cutoff:
                sim_sum = 0
                cluster.update({point:[[point],[sim_sum]]})
            else:
                center = centers[sim.index(max_sim)]
                sim_sum = function(p,[data[bits] for bits in cluster[center][0]])[0]
                cluster[center][0].append(point)
                cluster[center][1].append(sim_sum)
                max_sim = 0
                
                for count, (idx,sim) in enumerate(zip(cluster[center][0],cluster[center][1])):
                    sims = sim + function(data[idx],[p])[0]
                    cluster[center][1][count] = sims
                    if max_sim<sims:
                        max_sim = sims
                
                if max_sim > cluster[center][1][0]:
                    in_center_idx = cluster[center][1].index(max_sim)
                    new_center = cluster[center][0][in_center_idx]

                    cluster[center][0][0],cluster[center][0][in_center_idx] = cluster[center][0][in_center_idx],cluster[center][0][0]
                    cluster[center][1][0],cluster[center][1][in_center_idx] = cluster[center][1][in_center_idx],cluster[center][1][0]
                    
                    cluster.update({cluster[center][0][0]:cluster[center]})
                    del cluster[center]
                    
        return cluster
    
    def deep_obo(self,data,cutoff,function):
        """
    	Centers of clusters are mutable accroding both neigbor number 
        and similarity to get more realistic clustering result 

        Parameters:
            data: BitVector of Molecules
            cutoff: cutoff: Threshold to cluster the points
            
        Return:
            reps: Representatives of each cluster
        """
        cluster = {}
        cluster.update({0:[[0],[0]]})
        for k,p in enumerate(tqdm(data[1:])):
            
            point = k + 1
            centers = list(cluster.keys())
            sim = function(p,[data[center] for center in centers])
            max_sim = max(sim)
           
            if max_sim < cutoff:
                sim_sum = 0
                cluster.update({point:[[point],[sim_sum]]})
            else:
                center = centers[sim.index(max_sim)]
                sim_sum = function(p,[data[bits] for bits in cluster[center][0]])[0]
                cluster[center][0].append(point)
                cluster[center][1].append(sim_sum)
                
                max_sim = 0
                for count, (idx,sim) in enumerate(zip(cluster[center][0],cluster[center][1])):
                    sims = sim + function(data[idx],[p])[0]
                    cluster[center][1][count] = sims
                    if max_sim<sims:
                        max_sim = sims
                
                if max_sim > cluster[center][1][0]:
                    in_center_idx = cluster[center][1].index(max_sim)
                    new_center = cluster[center][0][in_center_idx]

                    cluster[center][0][0],cluster[center][0][in_center_idx] = cluster[center][0][in_center_idx],cluster[center][0][0]
                    cluster[center][1][0],cluster[center][1][in_center_idx] = cluster[center][1][in_center_idx],cluster[center][1][0]
                    
                    cluster.update({cluster[center][0][0]:cluster[center]})
                    del cluster[center]
                
                    center = new_center
                    cl_length = len(cluster[center][0])

                    #graph_construction
                    if cl_length > 20 and cl_length <= 100000:
                        
                        sorted_sims = np.argsort(np.array(cluster[center][1]))[int(cl_length - cl_length*0.1)-1:]
                        new_centers = np.take(np.array(cluster[center][0]),sorted_sims)
                        new_sims = np.take(np.array(cluster[center][1]),sorted_sims)
                        sum_nn = np.array([])
                        for l,i in enumerate(new_centers):
                            sim = function(data[i],[data[x] for x in new_centers])
                            max_sim = max(sim)
                            adj_matrix_row = binarize(np.array(sim).reshape(1,-1), threshold = max_sim*0.95)
                            sum_nn = np.append(sum_nn, np.sum(adj_matrix_row))

                        high_nn = new_centers[np.argmax(sum_nn)]
                        if high_nn != center:
                            high_nn_sim = sorted_sims[np.argmax(sum_nn)]   
                            cluster[center][0][0],high_nn = high_nn,cluster[center][0][0]
                            cluster[center][1][0],high_nn_sim = high_nn_sim,cluster[center][1][0]
                            
                            cluster.update({high_nn:cluster[center]})
                            del cluster[center]

                    elif cl_length > 100000:

                        sorted_sims = np.argsort(np.array(cluster[center][1]))[int(cl_length - cl_length*0.1)-1:]
                        new_centers = np.take(np.array(cluster[center][0]),sorted_sims)
                        new_sims = np.take(np.array(cluster[center][1]),sorted_sims)
                        sum_nn = np.array([])
                        for l,i in enumerate(new_centers):
                            sim = function(data[i],[data[x] for x in new_centers])
                            max_sim = max(sim)
                            adj_matrix_row = binarize(np.array(sim).reshape(1,-1), threshold = max_sim*0.95)
                            sum_nn = np.append(sum_nn, np.sum(adj_matrix_row))

                        high_nn = new_centers[np.argmax(sum_nn)]
                        if high_nn != center:
                            high_nn_sim = sorted_sims[np.argmax(sum_nn)]   
                            cluster[center][0][0],high_nn = high_nn,cluster[center][0][0]
                            cluster[center][1][0],high_nn_sim = high_nn_sim,cluster[center][1][0]
                            
                            cluster.update({high_nn:cluster[center]})
                            del cluster[center]
        return cluster
