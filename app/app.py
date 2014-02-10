from flask import Flask, render_template, g, request, redirect
import requests
import json
from collections import OrderedDict
import datetime
import pymongo
from statsd import StatsClient

statsd = StatsClient(host='127.0.0.1',
                     port=8125)

statsd.incr('start')


app = Flask(__name__)

conn = pymongo.MongoClient()
db = conn.blog

@app.route("/")
@statsd.timer('index')
def index():
    statsd.incr('index_pageview')
    articles = db.articles.find().sort('created_at', pymongo.DESCENDING).limit(10)
    ret = []
    for article in articles:
        user = db.users.find_one({'user_id': article['user_id']})
        article['user'] = user
        ret.append(article)
    latest_users = db.users.find().sort('created_at', pymongo.DESCENDING).limit(10)
    return render_template('index.html', articles=ret, latest_users=latest_users)


@app.route("/show/<permalink>")
@statsd.timer('article')
def show(permalink):
    article = db.articles.find_one({'permalink':permalink})
    article['user'] = db.users.find_one({'user_id': article['user_id']})
    latest_users = db.users.find().sort('created_at', pymongo.DESCENDING).limit(10)
    return render_template('article.html', article=article, latest_users=latest_users)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9001)
