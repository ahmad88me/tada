import requests
import csv
from PPool.Pool import Pool

ENDPOINT = "http://tadaa.linkeddata.es/api/webcommons_get_col_type"


def check_single_file(file_name, concept, fast=True):
    alphas = [0.1, 0.05, 0.01, 0.005, 0.001]
    url = "%s?k=5&file_name=%s&alpha=" % (ENDPOINT, file_name)
    k_list = [10, 5, 3, 1]
    k_a = {}
    if not fast:
        alphas = []
        for aa in range(100):
            alphas.append(aa*0.001)
    for a in alphas:
        r = requests.get(url+str(a))
        result = r.json()
        for k in k_list:
            if k in k_a:
                continue
            if result["results"] == []:
                k_a[k]="no results"
                # print "%30s, %20s, %s, %s" % (file_name, concept, str(k), "no results")
                # return
            else:
                # print "res: <%s> and concept <%s>" % (result["results"][0], concept)
                if concept in result["results"][:k]:
                #if result["results"][0] == concept:
                    # print "%30s, %20s, %s, %s" % (file_name, concept, str(k), str(a))
                    # return
                    k_a[k] = str(a)
        if result["results"] == []:
            for k in k_list:
                k_a[k] = "no results"
            break
        if len(k_list) == len(k_a.keys()):  # all required info are gathered, no need to continue
            break
    if len(k_list) == len(k_a.keys()):
        for k in k_list:
            print "%30s, %20s, %s, %s" % (file_name, concept, str(k), k_a[k])
    elif not fast:
        for k in k_list:
            if k not in k_a:
                k_a[k] = "alpha outside the scope"
                print "%30s, %20s, %s, %s" % (file_name, concept, str(k), "alpha outside the scope")
            else:
                print "%30s, %20s, %s, %s" % (file_name, concept, str(k), k_a[k])
    else:
        check_single_file(file_name, concept, fast=False)


#check_single_file("1438042986423_95_20150728002306-00125-ip-10-236-191-2_88435628_5", "http://dbpedia.org/ontology/PoliticalParty")

def validate():
    params_list = []
    f = open("local_data/web_commons_classes.csv")
    reader = csv.reader(f)
    for line in reader:
        file_name = line[0][:-7]
        concept = line[2]
        params_list.append((file_name, concept))
        #print file_name, concept
        # output_file = "local_uploads/web_commons_%s_%s.csv" % (concept, file_name)
        # input_file = "local_data/web_commons_tables/%s.json" % file_name
        # web_commons_json_table_to_csv(input_file, output_file)
    pool = Pool(max_num_of_processes=10, func=check_single_file, params_list=params_list)
    pool.run()

validate()