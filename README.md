# A new way of Clsutering for Large Datasets

This clustering algorithm was designed to cluster very large datesets like sets including 1 million points. To achieve that we used hierarchical clustering logic in our codes. Clustering was started from the single point and processing through the points accroding to similarities among them. As a point is coming, only its index and summation of similarity with other cluster members are recorded. Therefore, while clustering, no extra memory usage is seen. Also, since only one data point is examined in one pass, at the start of the algorithm, symmetric distance matrix is not needed that also results in low memory usage. 

