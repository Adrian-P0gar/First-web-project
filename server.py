from flask import Flask, render_template, request, redirect, url_for
import data_handler as data

app = Flask(__name__)


@app.route('/')
@app.route('/list', methods=['GET', 'POST'])
def list():
    default_information = data.read_csv()
    if request.args.get('sort') is None:
        information = data.sort_by(default_information)
    else:
        information = data.sort_by(default_information, request.args.get('sort'), request.args.get('sort_direction'))
    return render_template('list.html', information=information, title="Home", data=data)


@app.route('/add', methods=['GET', 'POST'])
def add():
    today_timer = data.get_time_stamp()
    if request.method == "POST":
        question_content = {
            'submission_time': today_timer,
            'title': request.form.get('title'),
            'view_number': 0,
            'vote_number': 0,
            'message': request.form.get('message'),
            'image': "?"
        }
        data.add_on_csv(dict(question_content))
        return redirect('/list')
    return render_template('add.html')


@app.route('/edit/<question_id>', methods=['GET', 'POST'])
def edit(question_id):
    if request.method == 'POST':
        form_id = request.form.get('form_id')
        form_title = request.form.get('title')
        if question_id == form_id:
            question_content = {
                'id': question_id,
                'submission_time': request.form.get('submission_time'),
                'title': request.form.get('title'),
                'view_number': request.form.get('view_number'),
                'vote_number': request.form.get('vote_number'),
                'message': request.form.get('message'),
                'image': request.form.get('image')
            }
            data.update_on_csv(question_content)
            return redirect(url_for('list'))
    question_content = data.get_csv_data(question_id)
    return render_template('edit.html',
                           question_content=question_content,
                           question_id=question_id
                           )


@app.route('/delete/<question_id>', methods=['GET', 'POST'])
def delete_question(question_id):
    form_id = request.form.get('form_id')
    data.delete_question(question_id)
    return redirect('/')


@app.route('/question/<question_ids>', methods=['GET', 'POST'])
def display_question(question_ids):
    if request.method == 'GET':
        if question_ids == request.form.get('id'):
            question = {"id": question_ids,
                        'title': request.form.get('title'),
                        'message': request.form.get('message')
                        }
            answer = {
                'id': request.form.get('id'),
                'submission_time': request.form.get('submission_time'),
                'vote_number': request.form.get('vote_number'),
                'message': request.form.get('message'),
                'image': request.form.get('image'),
                'question_id': request.form.get('question_id')
            }
    question = data.get_csv_data(question_ids)
    answer = data.get_csv_data_answer(question_ids)
    data.count_views_number(question_ids)
    return render_template('display_question.html',
                           question=question, question_ids=question_ids, title='Question',
                           answer=answer)


@app.route('/question/<question_ids>/new_answer', methods=['GET', 'POST'])
def answer(question_ids):
        if request.method == 'POST':
            answer_to_write = {
                'submission_time': data.get_time_stamp(),
                'vote_number': 0,
                'question_id': question_ids,
                'message': request.form.get('message'),
                'image': "?"
                }
            data.add_on_answer(answer_to_write)
            return redirect('/list')
        question = data.get_csv_data(question_ids)
        return render_template('new_answer.html', question=question)


@app.route("/question/<question_id>/vote_up", methods=['GET', 'POST'])
def vote_up(question_id):
    if request.method == 'POST':
        data.count_votes(int(question_id), 1)
        return redirect('/list')


@app.route("/question/<question_id>/vote_down", methods=['GET', 'POST'])
def vote_down(question_id):
    if request.method == 'POST':
        data.count_votes(int(question_id), -1)
        return redirect('/list')

@app.route('/delete/<question_id>', methods=['GET', 'POST'])
def delete_question(question_id):
    form_id = request.form.get('form_id')
    data.delete_question(question_id)
    return redirect('/')

@app.route("/answer/<answer_id>/vote_up", methods=['GET', 'POST'])
def vote_up_answer(answer_id):
    if request.method == "POST":
        data.count_votes_answer(int(answer_id), 1)
        return redirect(request.referrer)


@app.route("/answer/<answer_id>/vote_down", methods=['GET', 'POST'])
def vote_down_answer(answer_id):
    if request.method == "POST":
        data.count_votes_answer(int(answer_id), -1)
        return redirect(request.referrer)


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True
    )
