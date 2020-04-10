
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_cors import CORS
from decouple import config
from get_data import *
import joblib
from model import *
import pandas as pd


app = Flask(__name__)
CORS(app)

loadcv = joblib.load('models/tf.joblib')
loaddf = joblib.load('models/tfarray.joblib')
loaddf = loaddf.todense()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subreddit')
def search():
    title = request.args.get('title')
    block = request.args.get('block')
    words = title + ' ' + block.strip()
    data = transform_get(words, loadcv, loaddf)
    res = get_subreddit_info(data)

    return(render_template('search.html', res=res))

@app.route('/test')
def vals():
    res = get_subreddit_info([1,6,8,5])
    return(jsonify(res))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()