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

#### updateReps: 'mid'

When 'mid' is selected as center updating option, summation of similarities of each point to each point is held as in python dictionary. As new point is added to cluster, similarity sum is recalculated and the point with maximum similarity is seleceted as center.

![mid_figure](https://user-images.githubusercontent.com/37181660/107858174-e512a280-6e43-11eb-902b-3ceaea5a57a2.PNG)

#### updateReps: 'deep'

'deep' selection is the most expansieve method in this clustering methods. Since it uses both similarity and number of nearest neighbors are used to calibrate the center of each cluster. To decrease the space consumption, counting neighbors algortihm is applied on the points that have the highest similarity. The number of points is change as the number of cluster members. 

![deep_figure](https://user-images.githubusercontent.com/37181660/107858387-f7411080-6e44-11eb-919e-b0941540c839.PNG)

With this method, clustering the large dataset can be applicable without considering symmetric distance matrices or large graph constructions to find centers. Also, since it provide different distance functions it can be applied any kind of data. 
