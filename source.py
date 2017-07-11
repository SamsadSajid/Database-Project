import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import re
pd.set_option('display.expand_frame_repr', False)

def word_in_text(word, text):
    word = word.lower()
    text = unicode(text).lower()
    match = re.search(word, text)

    if match:
        return True
    else:
        return False

def _connect_mongo(host, port, db):
    """ A util for making a connection to mongo

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
    """
    conn = MongoClient(host, port)


    return conn[db]


def read_mongo(db, collection, host, port):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, db=db)

    #create index
    #result = db[collection].createIndex({text: "text"})

    # Make a query to the specific DB and Collection
    # cursor = db[collection].find({'place.country':'Russia'},
    #     no_cursor_timeout=True)

    cursor = db[collection].find({'source':{'$regex': 'web|iphone|android'}}, 
        no_cursor_timeout=True)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    return df


db = 'twitter'
collection='twitterCol'
#query={'lang':'{$exists: true}'}
host='localhost'
port=27017

var = read_mongo(db, collection, host, port)
#print var['place']

#matching language
var['web'] = var['text'].apply(lambda tweet:word_in_text('web', tweet))
var['iphone'] = var['text'].apply(lambda tweet:word_in_text('iphone', tweet))
var['android'] = var['text'].apply(lambda tweet:word_in_text('android', tweet))


src_web = var['web'].value_counts()[True]         
src_iphone = var['iphone'].value_counts()[True]
src_android = var['android'].value_counts()[True]

print src_web
print src_iphone
print src_android 

sources = ['web', 'iphone', 'android']
tweets_by_sources = [var['web'].value_counts()[True], var['iphone'].value_counts()[True],
 var['android'].value_counts()[True]]

x_pos = list(range(len(sources)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_sources, width, alpha=1, color='g')

# Setting axis labels and ticks
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: web vs. iphone vs. android (Raw data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(sources)
plt.grid()
plt.savefig('tweets_by_sources', format='png')
