import csv
import time

def read_csv():
    all_information = []
    with open("sample_data/question.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            all_information.append(dict(row))
    return all_information


def sort_by(data, label='id', order='descending'):
    for element in data:
        element['id'] = int(element['id'])
        element['submission_time'] = int(element['submission_time'])
        element['view_number'] = int(element['view_number'])
        element['vote_number'] = int(element['vote_number'])
    if order == 'descending':
        return [element for element in sorted(data, key=lambda x: x[label], reverse=True)]
    return [element for element in sorted(data, key=lambda x: x[label])]


def get_time_stamp():
    return str(int(time.time()))


def get_date_time(time_stamp):
    return time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(int(time_stamp)))
