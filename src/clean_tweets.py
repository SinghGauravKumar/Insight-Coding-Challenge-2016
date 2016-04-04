# Insight Data Engineering Coding Challenge
# Submission by Gaurav Kumar Singh
# Module for cleaning and formatting the string to obtain data in the proper format to compute average degree

# Importing necessary modules
import json
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


# function for formatting tweets and writing them to an output file
def format_tweets(inputfile, outputfile):
    #counting unicode tweets
    num_unicode = 0
    #counting tweets having no useful info.
    num_not_useful = 0
    with open(inputfile ,'r') as tweets_handle:
        for lines in tweets_handle:
            #turn lines into a disctionary
            lines_dict = json.loads(lines)
            try:
                #check if 'str' key exists as it contains the tweet;
                str_unicode = lines_dict['text']
                #check if tweets are ascii/unicode
                try:
                    #check if ascii can be enocded
                    str_ascii = str_unicode.encode('ascii')
                except UnicodeEncodeError:
                    #encode as ascii
                    str_ascii = str_unicode.encode('ascii','ignore')
                    #count tweet with unicode
                    num_unicode += 1
                #get timestamp
                timestamp = lines_dict['created_at']
                timestamp = timestamp.encode('ascii')
                #modify str string
                modified_str = modify_string(str_ascii)
                #merge output
                output = modified_str + ' (timestamp: ' + timestamp + ')'
                #write output to a file
                with open(outputfile, 'a') as tweet_output:
                    tweet_output.write(output)
                    tweet_output.write('\n')
            except KeyError:
                num_not_useful += 1
				
	print str(num_not_useful) + ' tweets left out!!!'
	#attach number of unicode tweets to output
    with open(outputfile, 'a') as tweet_output:
        tweet_output.write('\n')
        tweet_output.write(str(num_unicode) + ' tweets contained unicode.')

if __name__ == '__main__':
	inputfile = sys.argv[1]
	outputfile = sys.argv[2]
	format_tweets(inputfile, outputfile)
	print '\n'
	print 'tweets extracted from ' + str(inputfile) + ' and saved in ' + str(outputfile)

