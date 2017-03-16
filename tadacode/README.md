



## Questions to answer
* is using rdfs:RANGE for a concept is enough to get numerical data?



## To Do

- [x] compute the centers for each cluster
- [x] use Fuzzy clustering fit and get the membership (it works fine)
- [x] predict the new resources and see how the membership is performing
- [x] Produce the average membership of each cluster
- [ ] computer the error in each predicted cluster


## Contributions:
* A way to cleanup data (e.g. height with cm, in, foot,..).
* Measure how representative a given bag of numbers in a given domain (by classifying the training data after computing
the cluster centers).
* Merge measurements that are more likely the same (e.g. height and heightIn).
* Mapping with convention. extends the current R2RML with units conversion.
* Automatic classification of numerical data using fuzzy clustering


# Hypotheses:
* Can classify any bag of numbers if their values is distinguishable enough in the given domain.
*

# Debug
* SPARQLWrapper returns 10000 by max (it turns out that this limitation is from DBpedia)