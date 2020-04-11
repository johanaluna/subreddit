
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_cors import CORS
from decouple import config
import joblib
from model import *
import pandas as pd


app = Flask(__name__,static_url_path="/static/")
CORS(app)
loadcv = joblib.load('models/tf.joblib')
loaddf = joblib.load('models/tfarray.joblib')
loaddf = loaddf.todense()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subreddit')
def search():

    subreddit_input = request.args.get('title') + ' ' + request.args.get('content')
    data = transform_get(subreddit_input, loadcv, loaddf)
    res = get_subreddit_info(data)

    return(render_template('search.html', res=res))

@app.route('/test')
def vals():
    """this route lets us test the model directly in the Flask app"""
    # title, text, link = sorted([request.values['title'],
    #                                 request.values['text'],
    #                                 request.values['link']])
    submission = {"title": 'title', "text": 'text'}
    model_input = jsonConversion(submission)
    model_output = transform_get(model_input, loadcv, loaddf)
    subreddit_list = list_subreddits(model_output)
    return jsonify(subreddit_list)

# run the app.
if __name__ == "__main__":
    "Entry point for the falsk app"
    app.debug = True
    app.run()