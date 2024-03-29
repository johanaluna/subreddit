
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_cors import CORS
from decouple import config
import joblib
from model import *
import pandas as pd


application = Flask(__name__,static_url_path="/static/")
CORS(application)
loadcv = joblib.load('models/tf.joblib')
loaddf = joblib.load('models/tfarray.joblib')
loaddf = loaddf.todense()


@application.route('/')
def index():
    return render_template('index.html')

@application.route('/subreddit')
def search():

    subreddit_input = request.args.get('title') + ' ' + request.args.get('content')
    data = transform_get(subreddit_input, loadcv, loaddf)
    # print(data)
    res = get_subreddit_info(data)
    # print(res)

    return(render_template('result.html', res=res))

@application.route('/test')

def vals():
    res = get_subreddit_info([1,6,8,5])
    print(res)
    return(jsonify({'data':res}))


# def vals():
#     """this route lets us test the model directly in the Flask app"""
#     # title, text, link = sorted([request.values['title'],
#     #                                 request.values['text'],
#     #                                 request.values['link']])
#     submission = {"title": 'title', "text": 'text'}
#     model_input = jsonConversion(submission)
#     model_output = transform_get(model_input, loadcv, loaddf)
#     subreddit_list = list_subreddits(model_output)
#     return jsonify(subreddit_list)


# run the application.
if __name__ == "__main__":
    "Entry point for the falsk app"
    application.debug = True
    application.run(host='0.0.0.0')