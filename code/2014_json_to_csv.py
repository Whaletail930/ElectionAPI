import json
import csv

with open(r'C:\Users\belle\PycharmProjects\GDEIntAlk\DATA\districts_2014-2018-04-17T09-57-34.json', encoding='utf-8') as f:
    data = json.load(f)

csv_file = '../DATA/hungarian_election2014.csv'

csv_columns = ['name', 'number_votes', 'share_votes', 'district', 'affiliation']

with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()

    for item in data:
        for candidate in item['candidate_results']:
            name = candidate['candidate_name']
            number_votes = candidate['num_of_valid_votes']
            share_votes = candidate['rate_of_valid_votes']
            district = item['location']
            affiliation = candidate['candidate_party']

            writer.writerow({'name': name, 'number_votes': number_votes, 'share_votes': share_votes, 'district': district,
                             'affiliation': affiliation})
