
import sets
import json


def get_tables_types(file_dir):
    f = open(file_dir)
    s = f.read()
    table_type_set = sets.Set()
    for line in s.split('\n'):
        try:
            j = json.loads(line)

            # if j["hasKeyColumn"]:
            #     print j
            #     return ""
            # for k in j.keys():
            #     table_type_set.add(k)
            #table_type_set.add(j['tableType'])
        except Exception as e:
            pass

    print table_type_set


get_tables_types('/Users/aalobaid/Downloads/1438042981921.1/warc/CC-MAIN-20150728002301-00000-ip-10-236-191-2.ec2.internal.json')
get_tables_types('/Users/aalobaid/Downloads/1438042981921.1/warc/CC-MAIN-20150728002301-00001-ip-10-236-191-2.ec2.internal.json')
