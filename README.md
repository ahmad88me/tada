# TAbular DAta soft clustering

## new plan January, 2017

### Assumptions
* We are dealing with numerical numbers only


### Algorithm
1. From the training data, set the center of clusters using the hard k-means way (with membership being 0 or 1). As in the beginning the training set belongs to a single type
2. Classify the column of interest using its data via FCM.
3. Compute the average of the membership matrix to each cluster. and consider it the membership of this column.

### Things to consider
* think about the use of statistical tests.
* check if the average is a good measure.
* Use a test bed for comparison.
* Why it should performs better.
* What about the relation between columns.
* What about the subclasses.
* learning from new data sources e.g. (is the error is too high, or it is far from any of the clusters, we add this new cluster)
* allow human intervension to correct the classification.

##### The below are not part of the new idea
================================
### Detailed Plan
* learning different statistical tests.
* Check out this paper [14.3 Are Two Distributions Different?](http://www.aip.de/groups/soe/local/numres/bookcpdf/c14-3.pdf). Which seems to be really relavant.
* Implement statistical tests.
* Use them as features in K-means and visualize them.
* Use softclustering and mixed guassian mode to define the clusers.
* Label the cluseters.
* Compare our algorithm with the gold standard.


### Highlevel Plan
1. *Work first with numerical data*: So first, for each column I'll create n-features, each feature will some kind of statistical test e.g. t-test, Kolmogorov–Smirnov, ...etc.
2. *Include Categorical data, (see the papers __"Approximation Algorithms for k-models clustering"__ and __"Extensions to the k-Means Algorithm for Clustering Large Data Sets with Categorical Values"__)*


### Assumptions
* There are no similar columns in the training set, e.g. city_name_english, city_name_french


### Ideas
* Run K means multiple times and obtain the probabilites (Juan manuel's idea)
* Use PCA from the collection of tests to reduce the dimensionality.
* Add further (dummy) data to the training set if the user classified one column in the data set to be the same as one column in the training set that is not very similar.
* Maybe use the central limit theorem for the training samples incase we are using Standard Error of the Mean.
* Use Cohen's d, the distance between the population mean and the sample mean in terms of the sample standard deviation S. as a feature. The problem is that it is significantly affected by the outliers, and hence, we can eleminate them (or the max 10% and min 10%).
* Use t-values to computer the standard deviation instead of the z, so we cas save time. It is also possible to take something like 10 samples each of size 100.
* Maybe try to use R^2 (how correleted is the data) as a feature.
* For the probability, we can use the corresponding porbability in the z/t score. but I'm not sure if the distribution should be normal for that.
* [Enhancing Cluster Labeling Using Wikipedia](http://140.122.184.128/presentation/09-11-09/Enhancing%20Cluster%20Labeling%20Using%20Wikipedia.pdf).
* It would be nice to include something from this paper to justfy the use of statistical tests [On the Appropriateness of Statistical Tests in Machine Learning](http://www.site.uottawa.ca/ICML08WS/papers/J_Demsar.pdf).
* Use Continuous Reinforcement Learning to learn the types corrected manually by the domain expert. I have to idea how this would be done, but it is an interesting approach.

### Open Questions
* What about sources that are neither RDF not CSV e.g. (databases)
* Should we distinguish between temperature of cities and temperatures in the cosmos domain? (I will for now). 

### Tests to be checked
* [Kolmogorov–Smirnov test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test)
* [Anderson–Darling test](https://en.wikipedia.org/wiki/Anderson%E2%80%93Darling_test)
* [Jarque–Bera test](https://en.wikipedia.org/wiki/Jarque%E2%80%93Bera_test)
* [Goodness of fit](https://en.wikipedia.org/wiki/Goodness_of_fit)
* [Cramér–von Mises criterion](https://en.wikipedia.org/wiki/Cram%C3%A9r%E2%80%93von_Mises_criterion)
* [Akaike information criterion](https://en.wikipedia.org/wiki/Akaike_information_criterion)
* [Hosmer–Lemeshow test](https://en.wikipedia.org/wiki/Hosmer%E2%80%93Lemeshow_test)
* [Shapiro–Wilk test](https://en.wikipedia.org/wiki/Shapiro%E2%80%93Wilk_test)
* [Kuiper's test](https://en.wikipedia.org/wiki/Kuiper%27s_test)
* [Coefficient of determination R^2](https://en.wikipedia.org/wiki/Coefficient_of_determination)
* [Mann–Whitney U test](https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test)
* [Wilcoxon signed-rank test](https://en.wikipedia.org/wiki/Wilcoxon_signed-rank_test)
* [Sign test](https://en.wikipedia.org/wiki/Sign_test)
* [Kruskal–Wallis one-way analysis of variance](https://en.wikipedia.org/wiki/Kruskal%E2%80%93Wallis_one-way_analysis_of_variance)
* [One-way analysis of variance](https://en.wikipedia.org/wiki/One-way_analysis_of_variance)
* [Friedman test](https://en.wikipedia.org/wiki/Friedman_test)
* [Kendall's W](https://en.wikipedia.org/wiki/Kendall%27s_W)
* [Jonckheere's trend test](https://en.wikipedia.org/wiki/Jonckheere%27s_trend_test)
* 
