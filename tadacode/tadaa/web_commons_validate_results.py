import requests
import csv
from PPool.Pool import Pool

ENDPOINT = "http://tadaa.linkeddata.es/api/webcommons_get_col_type"


def check_single_file(file_name, concept):
    alphas = [0.1, 0.05, 0.01, 0.005, 0.001]
    url = "%s?k=1&file_name=%s&alpha=" % (ENDPOINT, file_name)
    for a in alphas:
        r = requests.get(url+str(a))
        result = r.json()
        # print "results: "
        # print result
        if result["results"] == []:
            print "%30s, %20s, %s" % (file_name, concept, "no results")
            return
        else:
            # print "res: <%s> and concept <%s>" % (result["results"][0], concept)
            if result["results"][0] == concept:
                print "%30s, %20s, %s" % (file_name, concept, str(a))
                return
    print "%30s, %20s, %s" % (file_name, concept, "alpha outside the scope")


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