import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import re

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
    cursor = db[collection].find({'text':{'$regex': 'python|java|javascript'}}, 
        no_cursor_timeout=True)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    '''
     Delete the _id
    if no_id:
        del df['_id']
	'''
    return df    


#tweet mining

def extract_link(text):
    link = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(link, text)
    if match:
        return match.group()
    return ''



db = 'twitter'
collection='twitterCol'
#query={'lang':'{$exists: true}'}
host='localhost'
port=27017

var = read_mongo(db, collection, host, port)
print var['text']

#matching language
var['Cpython'] = var['text'].apply(lambda tweet:word_in_text('python', tweet))
var['Cjavascript'] = var['text'].apply(lambda tweet:word_in_text('javascript', tweet))
var['Cjava'] = var['text'].apply(lambda tweet:word_in_text('java', tweet))


py_tweets_by_lang = var['Cpython'].value_counts()[True]			
js_tweets_by_lang = var['Cjavascript'].value_counts()[True]
j_tweets_by_lang = var['Cjava'].value_counts()[True]

print py_tweets_by_lang
print js_tweets_by_lang
print j_tweets_by_lang

prg_langs = ['python', 'javascript', 'java']
tweets_by_prg_lang = [var['Cpython'].value_counts()[True], var['Cjavascript'].value_counts()[True],
 var['Cjava'].value_counts()[True]]

x_pos = list(range(len(prg_langs)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')

# Setting axis labels and ticks
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: python vs. javascript vs. java (Raw data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(prg_langs)
plt.grid()
plt.savefig('tweets_by_prg_language_1', format='png')


#Targeting relevant tweets
print 'Targeting relevant tweets\n'
var['programming'] = var['text'].apply(lambda tweet: word_in_text('programming', tweet))
var['tutorial'] = var['text'].apply(lambda tweet: word_in_text('tutorial', tweet))
var['relevant'] = var['text'].apply(lambda tweet: word_in_text('programming', tweet) 
    or word_in_text('tutorial', tweet))
"""
#Analyzing Tweets by programming language: Second attempt
print 'Analyzing tweets by programming language: Second attempt\n'
tweets_by_prg_lang = [var[var['relevant'] == True]['python'].value_counts()[True], 
                  var[var['relevant'] == True]['javascript'].value_counts()[True], 
                  var[var['relevant'] == True]['java'].value_counts()[True]]
x_pos = list(range(len(prg_langs)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_prg_lang, width,alpha=1,color='g')
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: python vs. javascript vs. ruby (Relevant data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(prg_langs)
plt.grid()
plt.savefig('tweets_by_prg_language_2', format='png')    
"""
#extracted link
var['link'] = var['text'].apply(lambda tweet: extract_link(tweet))

#This DataFrame is a subset of tweets DataFrame and contains all relevant tweets that have a link.
tweets_relevant = var[var['relevant'] == True]
tweets_relevant_with_link = tweets_relevant[tweets_relevant['link'] != '']

#displaying links
print tweets_relevant_with_link[tweets_relevant_with_link['Cpython'] == True]['link']
print tweets_relevant_with_link[tweets_relevant_with_link['Cjavascript'] == True]['link']
print tweets_relevant_with_link[tweets_relevant_with_link['Cjava'] == True]['link']