# TAbular DAta classification of soft clusters

###Detailed Plan
* learning different statistical tests.
* Implement statistical tests.
* Use them as features in K-means and visualize them.
* Use softclustering and mixed guassian mode.
* Compare our algorithm with gold standard.

###Highlevel Plan
1. *Work first with numerical data*: So first, for each column I'll create n-features, each feature will some kind of statistical test e.g. t-test, Kolmogorov–Smirnov, ...etc.
2. *Include Categorical data, (see the papers __"Approximation Algorithms for k-models clustering"__ and __"Extensions to the k-Means Algorithm for Clustering Large Data Sets with Categorical Values"__)*

###Assumptions
* There are no similar columns in the training set, e.g. city_name_english, city_name_french


###Ideas
* Add further (dummy) data to the training set if the user classified one column in the data set to be the same as one column in the training set that is not very similar.


###Open Questions
* What about sources that are neither RDF not CSV e.g. (databases)

