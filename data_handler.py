import csv

def read_csv():
    all_information = []
    with open("/home/pogar/Web Module/TW I/ask-mate-python/sample_data/question.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            all_information.append(dict(row))
    return all_information












