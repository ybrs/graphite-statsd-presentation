import pymongo
import datetime

conn = pymongo.MongoClient()
db = conn.blog

for i in xrange(1,100000):
    print ">>>", i
    doc = {
        'title': 'foo %s' % i,
        'permalink': 'foo_%s' % i,
        'created_at': datetime.datetime.utcnow(),
        'excerpt': 'foo %s _ ' % i * 10,
        'article': 'foo %s _ ' %i * 100,
        'user_id': 'user_%s' % ((i % 10) + 1)
    }
    db.articles.insert(doc)

for i in xrange(1,100000):
    doc = {
        'user_id': 'user_%s' % i,
        'name': 'user - %s' % i,
        'created_at': datetime.datetime.utcnow(),
        'profile': 'foo %s _ ' %i * 100,
    }
    db.users.insert(doc)
    print i