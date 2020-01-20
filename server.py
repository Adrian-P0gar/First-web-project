from flask import Flask, render_template, request,redirect, url_for
import data_handler as data

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def list():
    information = data.read_csv()
    return render_template('list.html', information=information , title="asdfghj")



if __name__ == '__main__':
    app.run(
        port= 5000,
        debug=True
    )