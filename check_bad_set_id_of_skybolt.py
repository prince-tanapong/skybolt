import csv
from pprint import pprint
from itertools import groupby


FILE_NAME = 'Skybolt.csv'


with open(FILE_NAME) as csvfile:
    reader = csv.DictReader(csvfile)
    set_of_set_id = {}
    result = []
    for row in reader:
        if row['SETSID'] not in set_of_set_id:
            set_of_set_id[row['SETSID']] = [row['RSTAT']]
        else:
            set_of_set_id[row['SETSID']].append(row['RSTAT'])

    for key, value in set_of_set_id.items():
        is_bad = False
        for text, group in groupby(value):
            if text == 'T' and sum(1 for _ in group) >= 3:
                is_bad = True
                break
        result.append({
            'SETSID': key,
            'RSTAT_GROUP': value,
            'IS_BAD': is_bad
        })

write_file_name = FILE_NAME.split('.')[0] + '_summary.csv'
with open(write_file_name, 'w') as csvfile:
    fieldnames = ['SETSID', 'RSTAT_GROUP', 'IS_BAD']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for each in result:
        writer.writerow(each)
