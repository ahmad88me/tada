

## About the web app
* Add a page to list Predictions
* Test the prediction function
* Test update_func for train_with_data_and_meta and test_with_data_and_meta
* There was an error (below), I actually applied the solution, but I need to check if it is solved
```
in explore_and_train
    else:
AttributeError: 'QuerySet' object has no attribute 'save'
```
* Add update_func to the rest of the function calls in `core.py`
* Implement the prediction interface
* Top k candidates
* Implement the testing mode (to verify the score of the classifications with a given k (top k candidates))
* Add stats and diagrams.
* Accept multiple csv files.
* Filter out non-numerical columns from the csv files
* Generate R2RML.
* Check Safety of the functionns in core.py e.g. if data is None then update the status and stop.


## progress
* Building the web app
* Looking for data sources, will use the the one from Karma (Smithsonian American Art Museum)
* Also explore http://smartcity.linkeddata.es/sparql as provided by Maria
* **New FCM** algorithm that takes into account the average memebership for each cluster.
* Extract the ontology schema as in the paper "Extraction and Visualization of TBox Information from SPARQL Endpoints"

## finished [ordered in desc]
* now preparing to do the testing with the files after learning from the sparql queries, implementing the cleaner
version of learning.py and main.py
* on main compute center of clusters as average and by the fuzzy way provides exact match, now I wanna test it on
the function main_manual_sparql
* working on the function merge_clusters_from_meta in learning.py


## Questions to answer/ Ideas to consider
* is using rdfs:RANGE for a concept is enough to get numerical data?
* explore the idea of cluster radius; instead of storing only cluster centers, maybe we can use the quarentile for this.
* how to merge close clusters (if the membership is less than a given threshold) (what I'm doing now is merge them if
 the membership of one of them has higherscore for being in the other).
* Problem with the merging or clusters: what is there is a circular merging thing that arise, e.g. if cluster a is
closer to cluster b and cluster b is closer to cluster c. For now, if a is closer to b and b is closer to another
cluster, then don't merge a and b (maybe I can also examine should I ignore merge a and b while allowing b and c? or
would it be better to merge a and b while not merging b and c. maybe I can examine the membership of both and then pick
[right now, I'm doing in a naive way depending on the order (which comes first)]). Also I'm not checking what is the
impact of multiple clusters is getting merged (and what if all of them merged into one big cluster?).
* I need to further study the theory see if having data points that initially belong to a cluster (from the initial data
) actually belong more (higher membership) to another cluster is possible to occur from a theoretical point of view.
* I should compute the centers of the clusters in the fuzzy way, not like k-means.
* Introducing a new FCM algorithm that supports merging clusters and we call it MerFCM.
* **New FCM** algorithm that takes into account the average memebership for each cluster (because now even with manually
computed membership, it does not provide the best membership for the whole cluster, giving that we are averaging
the membership).



Will only use average because all the points matters, and all the data points are actually weighted equally.



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


## Other use cases
* Cleaning up synonym properties in knowledge bases like DBpedia


# Hypotheses:
* Can classify any bag of numbers if their values is distinguishable enough in the given domain.
* Without computing any features, only the numerical data them selves

# Debug
* SPARQLWrapper returns 10000 by max (it turns out that this limitation is from DBpedia)