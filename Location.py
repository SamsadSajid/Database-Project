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
    cursor = db[collection].find({'place.country':'Russia'},
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

var['city1'] = var['place'].apply(lambda tweet:word_in_text('Moscow', tweet))
var['city2'] = var['place'].apply(lambda tweet:word_in_text('Saint Petersburg', tweet))
var['city3'] = var['place'].apply(lambda tweet:word_in_text('Rjazan', tweet))
var['city4'] = var['place'].apply(lambda tweet:word_in_text('Tver', tweet))
var['city5'] = var['place'].apply(lambda tweet:word_in_text('Novosibirsk', tweet))

city_num1 = var['city1'].value_counts()[True]
city_num2 = var['city2'].value_counts()[True]
city_num3 = var['city3'].value_counts()[True]
city_num4 = var['city4'].value_counts()[True]
city_num5 = var['city5'].value_counts()[True]

print city_num1
print city_num2
print city_num3
print city_num4
print city_num5

places = ['Moscow', 'Saint Petersburg', 'Rjazan', 'Tver', 'Novosibirsk']

tweets_by_places = [city_num1, 
city_num2, city_num3,
city_num4, city_num5]

x_pos = list(range(len(places)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_places, width, alpha=1, color='g')

# Setting axis labels and ticks
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: Moscow vs. Saint Petersburg vs. Rjazan vs. Tver vs. Novosibirsk (Raw data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(places)
plt.grid()
plt.savefig('tweets_by_places_1', format='png')
