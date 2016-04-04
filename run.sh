#!/usr/bin/env bash
python ./src/clean_tweets.py ./tweet_input/tweets.txt ./tweet_output/cleaned_tweets.txt
python ./src/average_degree.py ./tweet_input/tweets.txt ./tweet_output/output.txt
