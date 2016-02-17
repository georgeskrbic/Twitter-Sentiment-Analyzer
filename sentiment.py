import twitter
import json
from urllib import unquote

CONSUMER_KEY = 'xxxxxxxxxxxxxxx'
CONSUMER_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
OAUTH_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
OAUTH_TOKEN_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

q = raw_input('Enter a search term: ')
k = raw_input('Enter a second term: ')

count = 1000

search_results = twitter_api.search.tweets(q=q, count=count)

statuses = search_results['statuses']


print q+": "
for _ in range(5):
    print "Length of statuses", len(statuses)
    try:
        next_results = search_results['search_metadata']['next_results']
    except KeyError, e: # No more results when next_results doesn't exist
        break
        
    # Create a dictionary from next_results, which has the following form:
    # ?max_id=313519052523986943&q=NCAA&include_entities=1
    kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
    
    search_results = twitter_api.search.tweets(**kwargs)
    statuses += search_results['statuses']

status_texts = [ status['text'] 
                 for status in statuses ]
words = [ w 
          for t in status_texts 
              for w in t.split() ]


sent_file = open('AFINN-111.txt')

scores = {} # initialize an empty dictionary
for line in sent_file:
    term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
    scores[term] = int(score)  # Convert the score to an integer.

score1 = 0
for word in words:
    uword = word.encode('utf-8')
    if uword in scores.keys():
        score1 = score1 + scores[word]


search_results = twitter_api.search.tweets(q=k, count=count)

statuses = search_results['statuses']
print ("")
print k + ": "
for _ in range(5):
    print "Length of statuses", len(statuses)
    try:
        next_results = search_results['search_metadata']['next_results']
    except KeyError, e: # No more results when next_results doesn't exist
        break
        
    # Create a dictionary from next_results, which has the following form:
    # ?max_id=313519052523986943&q=NCAA&include_entities=1
    kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
    
    search_results = twitter_api.search.tweets(**kwargs)
    statuses += search_results['statuses']

status_texts = [ status['text'] 
                 for status in statuses ]
words = [ w 
          for t in status_texts 
              for w in t.split() ]

sent_file = open('AFINN-111.txt')

scores = {} # initialize an empty dictionary
for line in sent_file:
    term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
    scores[term] = int(score)  # Convert the score to an integer.

score2 = 0
for word in words:
    uword = word.encode('utf-8')
    if uword in scores.keys():
        score2 = score2 + scores[word]


# Depending on the score the print statement will match the appropriate statement for the corresponding difference in score
print ""
if float(score1)>float(score2):
	if float(score1) > 0:
		print "It appears that " + q + " has a more positive sentiment value of " + str(float(score1)) + " while " + k + " has a value of " + str(float(score2)) 
	else:
		print "It appears that " + q + " has less negative sentiment value of " + str(float(score1)) + " while " + k + " has a value of " + str(float(score2)) 
elif float(score1)<float(score2):
	if float(score2) > 0:
		print "It appears that " + k + " has a more positive sentiment value of " + str(float(score2)) + " while " + q + " has a value of " + str(float(score1))
	else:
		print "It appears that " + k + " has less negative sentiment value of " + str(float(score1)) + " while " + q + " has a value of " + str(float(score1)) 
else:
	print "It appears that both" + q + " and " + k + " have equal sentiment values of " + str(float(score1))


# Produces a graph for the sentiments of both terms.
import matplotlib.pyplot as plt
import numpy as np

n = 2
ind = np.arange(n)
width = .65
sentimentScore1 = [float(score1), float(score2)]
searchTerms = [q,k]

bar1 = plt.bar(ind,sentimentScore1 ,width, edgecolor='black',align='center')
bar2 = plt.bar(ind,sentimentScore1,width,edgecolor='black',align='center')

bar2[0].set_color('g')
bar2[1].set_color('b')
bar2[0].set_edgecolor('b')
bar2[1].set_edgecolor('b')

plt.ylabel('Scores')
plt.title('Sentiment Comparison')
plt.xticks(ind, searchTerms)
plt.show()






