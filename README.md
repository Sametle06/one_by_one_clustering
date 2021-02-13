# A new way of Clustering for Large Datasets

This clustering algorithm was designed to cluster very large datesets like sets including 1 million points. To achieve that we used hierarchical clustering logic in our codes. Clustering was started from the single point and processing through the points accroding to similarities among them. As a point is coming, only its index and summation of similarity with other cluster members are recorded. Therefore, while clustering, no extra memory usage is seen. Also, since only one data point is examined in one pass, at the start of the algorithm, symmetric distance matrix is not needed that also results in low memory usage. 

## The Parameters

The main function we use is  'obyone()' to achive clustering. The parameters of the function:

- **data**: A feature dataset
- **cutoff**: A threshold to form clusters
- **function**, {Tanimoto, Manhattan, Euclidean, Cosine, Minkowski}, (default: Euclidean):A similarity function.
- **isBit**: A boolean value to indicate whether data is a rdkit.bitvector or not. If True, rdkit.DataStructs.BulkTanimotoSimilarity function will be used.
- **updateReps**, {‘basic’, ’mid’, ’deep’}, (default: ‘basic’): A parameter that decides to how to adjust centers of clusters.
  - *basic*: No adjustment for center. 1st cluster member is the center.
  - *mid*: Adjustment for center based on similarity sum.
  - *deep*: Both similarity and number neighbors to adjust center.
- **p**: p value to calculate Minkowski similarity. (if p = 1: Manhattan, if p = 2: Euclidean similarities) 

### Expanse Explanation of Parameter 'updateReps':

Since large dataset means large memory consumption, we tried to be selective to lower this consumption as much as possible. To achieve it, we present three methods of calibrating the centers of clusters. These three methods are named as 'basic', 'mid' and 'deep'. 

#### updateReps: 'basic'

In this selection, basic clustering is used. As points are coming, they are clustered according to their similarities between the previous cluster centers. After points are placed, no center recalculation is done to not increase complexity. The following figure gives visual aid:

![basic_figure](https://user-images.githubusercontent.com/37181660/107857952-8a2c7b80-6e42-11eb-80eb-121b2c9670fa.PNG)
*Figure-1 Visual Representation of Clustering while updateReps = 'basic'* 

