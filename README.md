# TADA: TAbular Data Annotation

## New ideas (2018, Sept)
1. Use a subset of the entity column and try different set of combinations tto get matches. Once the functions (text manipulationes e.g. Transform them to Camel Case) they are applied to the rest of the values in that column. It will be much faster as exact can be used. We can also look for cell values that results in a smaller number of entities to ease entity disambiguation when performing entity linking (Inspired by zhang2017effective).

## Get the prerequisites
1. [python](https://www.python.org/downloads/)
2. [pip](https://pip.pypa.io/en/stable/installing/)
3. [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)


## Installing the prerequisite python libraries:
1. You can run the below command to install the libraries.
```
pip install -r requirements.txt
```

Note: to run the `explore\explore.py` (that show the diagrams, you would need to install the latest matplotlib from github (not in pip yet) [here](https://github.com/matplotlib/matplotlib).

## Running the application:
1. Go to the folder tadacode 

```
cd tadacode
```
2. If it is your first time, run the below command:

```
python manage.py makemigrations tadaa
```
3. If it is your first time, run the below command:

```
python manage.py migrate tadaa
```
4. Run the server using the below command:

```
python manage.py runserver
```
5. Go to `http://127.0.0.1:8000`

Note: Running the application locally, after creating the model or the prediction when the status reaches 100 (even before showing that on the screen) it stop and you would need to restart the server using the below command:

```
python manage.py runserver
```

## Data for entity column semantic labeling
[Olympic Data](https://github.com/ahmad88me/tada/tree/master/tadacode/explore/updated_input_new_for_tada)

## Project Components:

#### Fuzzy c-means:
This includes the FCM class which is an implementation of fuzzy c-means. The implementation is inspired by the code of k-means in scikit-learn. 
Folder: `clustering`

#### Web app and workflow:
It contains the workflow of the application (e.g. creating the model and perform the prediction using FCM) and the web related code (e.g. WUI and the server code). 
Folder: `tadaa`
Files:`learning.py`

#### data extraction
This model is responsible for extracting the data for a collection of classes from the endpoint using SPARQL query.
File: `data_extraction.py` and `easysparql.py`

## Step by Step guide
[step by step guide](https://github.com/ahmad88me/tada/tree/master/step_by_step/README.md)

## Data
[Olympic Data](https://github.com/ahmad88me/tada/tree/master/tadacode/explore/updated_input_new_for_tada)


## Report
[report](https://github.com/ahmad88me/tada/blob/master/report.pdf)

