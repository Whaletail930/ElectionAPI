import csv
import json


csv_file = '../DATA/hungarian_election2018.csv'

headers = ['name', 'number_votes', 'share_votes', 'district', 'affiliation']

with open(r'C:\Users\belle\PycharmProjects\GDEIntAlk\DATA\districts_2018-2018-04-16T08-43-24.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    for item in data:
        location = item.get('location')
        candidate_results = item.get('candidate_results', [])
        for candidate in candidate_results:
            name = candidate.get('candidate_name')
            number_votes = candidate.get('num_of_valid_votes')
            share_votes = candidate.get('rate_of_valid_votes')
            district = location
            affiliation = candidate.get('candidate_party')
            writer.writerow([name, number_votes, share_votes, district, affiliation])
