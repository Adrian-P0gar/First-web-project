import csv
import time

DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_FILE_PATH = "/Users/alexandruoriean/codecool/web/1_tw_week/ask_mate/sample_data/question.csv"
ANSWER_PATH = '/Users/alexandruoriean/codecool/web/1_tw_week/ask_mate/sample_data/answer.csv'


def read_csv():
    all_information = []
    with open(DATA_FILE_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            all_information.append(dict(row))
    return all_information


def update_on_csv(story):
    list_of_all = read_csv()
    with open(DATA_FILE_PATH, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        writer.writeheader()

        for row in list_of_all:
            # if row['id'] != story['id']:
            #     writer.writerow(row)
            if row['id'] == story['id']:
                row = story
                # writer.writeheader()

            writer.writerow(row)


def answer_read():
    all_information = []
    with open(ANSWER_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            all_information.append(dict(row))
    return all_information


def get_csv_data_answer(one_user_story_id=None):
    """
    :param one_user_story_id:
        If given, it will act as a filter and return the dictionary of one specific User Story
        If not given, it will return a list of dictionaries with all the details
    :return:
    """
    #  create a temporary list to read each line
    user_stories = []
    final_answer = []
    #  open csv file to read
    with open(ANSWER_PATH, encoding='utf-8') as csvfile:
        #  use DictReader to directly create dictionaries from each lines in the csv file
        reader = csv.DictReader(csvfile)

        #  read all lines in csv file
        for row in reader:
            #  make a copy of the read row, since we can't modify it
            user_story = dict(row)

            # if filtered, then just return this _found_ user story
            if one_user_story_id is not None and one_user_story_id == user_story['question_id']:
                final_answer.append(user_story)

            #  store modified data in temporary list
            user_stories.append(user_story)
        return final_answer


def get_csv_data(one_user_story_id=None):
    """
    :param one_user_story_id:
        If given, it will act as a filter and return the dictionary of one specific User Story
        If not given, it will return a list of dictionaries with all the details
    :return:
    """
    #  create a temporary list to read each line
    user_stories = []

    #  open csv file to read
    with open(DATA_FILE_PATH, encoding='utf-8') as csvfile:
        #  use DictReader to directly create dictionaries from each lines in the csv file
        reader = csv.DictReader(csvfile)

        #  read all lines in csv file
        for row in reader:
            #  make a copy of the read row, since we can't modify it
            user_story = dict(row)

            # if filtered, then just return this _found_ user story
            if one_user_story_id is not None and one_user_story_id == user_story['id']:
                return user_story

            #  store modified data in temporary list
            user_stories.append(user_story)


def next_id():
    existing_data = read_csv()
    if len(existing_data) == 0:
        return 1
    else:
        id = len(existing_data) + 1
        return id


def add_on_csv(story):
    with open(DATA_FILE_PATH, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        # writer.writeheader()
        story["id"] = next_id()
        writer.writerow(story)


def get_time_stamp():
    return str(int(time.time()))


def get_date_time(time_stamp):
    return time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(int(time_stamp)))


def sort_by(data, label='submission_time', order='descending'):
    for element in data:
        element['id'] = int(element['id'])
        element['submission_time'] = int(element['submission_time'])
        element['view_number'] = int(element['view_number'])
        element['vote_number'] = int(element['vote_number'])
    if order == 'descending':
        return [element for element in sorted(data, key=lambda x: x[label], reverse=True)]
    return [element for element in sorted(data, key=lambda x: x[label])]


def count_views_number(id_question):
    questions = read_csv()
    for question in questions:
        if question['id'] == str(id_question):
            question['view_number'] = str(int(question['view_number']) + 1)
            update_on_csv(question)


def count_votes(question_id, number):
    all_csv_info= read_csv()
    for row in all_csv_info:
        if int(row['id']) == question_id:
            row_to_edit = row
            number_of_votes = int(row_to_edit['vote_number']) + int(number)
            row_to_edit['vote_number'] = number_of_votes
            update_on_csv(row_to_edit)
