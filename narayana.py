import json
from random import randint
import datetime
from time import strftime
from flask import Flask, render_template, request
from tinydb import TinyDB, where

app = Flask(__name__)
db = TinyDB('nynn.json')
app.config['SECRET_KEY'] = str(randint)


@app.route('/', methods=['GET'])
def index_get():
    return render_template('index.html')


@app.route('/record', methods=['GET'])
def record_get():
    return render_template('record.html')


@app.route('/record', methods=['POST'])
def record_post():
    data = request.form
    thoughts = data['thoughts']
    phone = data['phone']
    level = data['level']
    db.insert(
        {'thoughts': data['thoughts'],
         'phone': data['phone'],
         'level': data['level'],
         'time': strftime("%Y-%m-%d %H:%M:%S")})

    return render_template('confirm.html')


@app.route('/access', methods=['GET'])
def access_get():
    return render_template('access.html')


@app.route('/access', methods=['POST'])
def access_post():
    custsubs = db.search(where('phone') == request.form['phone'])
    return render_template('accessresults.html', thoughts=json.dumps(custsubs))


@app.route('/logs', methods=['GET'])
def logs_get():
    custsubs = db.all()
    return render_template('accessresults.html', thoughts=json.dumps(custsubs))


if __name__ == '__main__':
    app.jinja_env.cache = {}
    app.run()
