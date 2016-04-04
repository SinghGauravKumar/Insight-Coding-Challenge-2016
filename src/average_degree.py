# Insight Data Engineering Coding Challenge
# Submission by Gaurav Kumar Singh
# Module for computing the average degree of the vertices of the graph structure made of hashtags

# Importing necessary modules
import json
import datetime as dt
import itertools
import sys

# function for modifying tweets: basically removal of spaces, newlines, tabs, etc
def modify_string(str):
    str.strip()
    str.replace("\/", "/")
    str.replace("\\", "\ ")
    str.replace("\'", "'")
    str.replace('\"', '"')
    str.replace("\n", " ")
    str.replace("\t", " ")
    str = " ".join(str.split())
    return str
	
# function for converting timestamp to obtain year, month, day, time data
def timestamp_converter(timestamp):
    yy = int(timestamp.split(' ')[5])
    mm = enumerate_month(timestamp.split(' ')[1])
    dd = int(timestamp.split(' ')[2])
    time = timestamp.split(' ')[3]
    hr = int(time.split(':')[0])
    mi = int(time.split(':')[1])
    sec = int(time.split(':')[2])
    datetime_object = dt.datetime(yy,mm,dd,hr,mi,sec)
    return datetime_object

# function for enumerating months starting from 1
def enumerate_month(months_abbr):
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    month=0
    for iter in months:
        month+=1
        if months_abbr.lower() == iter:
            return month

# function for extracting hashtags and date from the tweet in the form of tuples
def extract_hashtags_and_date_from_tweet(lines):

    lines_dict = json.loads(lines)
    try:
        text_unicode = lines_dict['text']
        text_ascii = text_unicode.encode('ascii','ignore')
        text_ascii = modify_string(text_ascii)
        text_ascii = text_ascii.lower()
        #get timestamp
        timestamp = lines_dict['created_at']
        timestamp = timestamp.encode('ascii')
        date = timestamp_converter(timestamp)

        #get the hashtags out
        hashtags = map(lambda x: x.split(' ')[0], text_ascii.split('#'))
        hashtags = hashtags[1:]
        return (hashtags, date)
    except KeyError:
        no_text = 1
        return no_text


class hashtag_graph:
    def __init__(self):
        self.degree_dict = {}
        self.connection_dict = {}

    def add_tweet(self, tuple_hashtags_and_date):
        new_connections = itertools.combinations(tuple_hashtags_and_date[0],2)
        for edge in new_connections:
			#if edge does not exist
            if tuple(edge) not in self.connection_dict.keys():
				# increment degree counter
                for vertex in edge:
                    if vertex in self.degree_dict.keys():
                        self.degree_dict[vertex] +=1
                    else:                         
                        self.degree_dict[vertex] = 1
            # update the time for the edge:
            self.connection_dict[tuple(edge)] = tuple_hashtags_and_date[1]

    def remove_old_tweets(self, date, time_period):
        #if the time is older than the intended time_period window, it will not be a part of the dictionary
        rolling_dict = { k:v for k,v in self.connection_dict.items() if date - v < dt.timedelta(0,time_period)}
        #deleted keys:
        diff = list(set(self.connection_dict.keys()) - set(rolling_dict.keys()))
        for edge in diff:
            for vertex in edge:
                if vertex in self.degree_dict.keys(): #alone hashtags can not be a part of degree_dict
                    self.degree_dict[vertex] -=1
                    if self.degree_dict[vertex] <= 0:
                        del self.degree_dict[vertex]
        self.connection_dict = rolling_dict

    def get_degree_list(self):
        return self.degree_dict.values()

def average_degree_60_sec_window(inputfile, outputfile):
    empty_tweets = 0
    num_tweet = 0
    graph_hashtags = hashtag_graph()
    with open(inputfile,'r') as tweets_handle:
        for lines in tweets_handle:
            num_tweet +=1 
            #get hashtags and date
            tuple_hashtags_and_date = extract_hashtags_and_date_from_tweet(lines)
            #skip empty tweet
            if tuple_hashtags_and_date == 1:
                empty_tweets +=1
                continue
            tuple_hashtags_and_date[0].sort()
            graph_hashtags.add_tweet(tuple_hashtags_and_date)
            graph_hashtags.remove_old_tweets(tuple_hashtags_and_date[1],60)
            degree_list = graph_hashtags.get_degree_list()

            #calculate average degree and write to outputfile.
            if len(degree_list) >0:
				# average_degree computation
                average_degree = float(sum(degree_list))/len(degree_list)
                with open(outputfile, 'a') as output:
                    result = '%.2f' %average_degree
                    output.write(result)
                    output.write('\n')
            else:
                with open(outputfile, 'a') as output:
                    result = '0'
                    output.write(result)
                    output.write('\n')


if __name__ == '__main__':
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    average_degree_60_sec_window(inputfile, outputfile)
