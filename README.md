# Twitter-Sentiment-Analytics-using-Apache-Spark-Streaming-APIs-and-Python
About processing live data streams using Spark’s streaming APIs and Python. We will be performing a basic sentiment analysis of real-time tweets. In addition, a basic introduction to Apache Kafka.

# Background
In this project, we will be processing streaming data in real time. One of the first requirements is to get access to the streaming data; in this case, realtime
tweets. Twitter provides a very convenient API to fetch tweets in a streaming manner. 

In addition, we will also be using Kafka to buffer the tweets before processing. Kafka provides a distributed queuing service which can be used to store the data when the data creation rate is more than processing rate. 

In order to download the tweets from twitter streaming API and push them to kafka queue, we have have the python script twitter_to_kafka.py. The script will need twitter authentication tokens (keys). Once we have the authentication tokens, create or update the twitter.txt file with these credentials. 

After updating the text file with twitter keys, we can start downloading tweets from the twitter stream API and push them to the twitterstream topic in Kafka.

The twitterStream.py writes the running total count of the number of positive and negative words that have been tweeted. In addition, we will have to plot the total positive and negative word counts for each timestep. 

See the example outputs below.
The word lists for positive words and negative words are given in the positive.txt and negative.txt files respectively.

load_wordlist(filename)
This function is used to load the positive words from positive.txt and the negative words from negative.txt . This function returns the words as a list or set.

stream(ssc, pwords, nwords, duration)
This is the main streaming function consisting of several steps like starting the stream, getting the tweets from kafka, and stopping the stream. We take the streamed tweets and find the number of positive and negative words. The tweets variable is a DStream object on which we can perform similar transformations that we could to an RDD. Currently, tweets consists of rows of strings, with each row representing one tweet. We can view this structure by using the pprint function : tweets.pprint()

We want to combine the positive word counts together and to combine the negative word counts together. Therefore, rather than mapping each word to (word, 1), we can map each word to (“positive”, 1) or (“negative”, 1) depending on which class that word belongs. Then, the counts can be aggregated using the reduceByKey function to get the total counts for “positive” and the total counts for “negative”. The DStream would store the counts at each time step, not the running total. To get the running total, we must use the updateStateByKey function. For more details, read the section about this operation. It is this DStream (the one with the running totals) that we should output using the pprint function. 

The other DStream (the one that doesn’t store the running total) can be used to make the plot that shows the total counts at each time step. However, we first must convert the DStream into something useable. To do this, use the foreachRDD function. With this function, we can loop over the sequence of RDDs of that DStream object and get the actual values.

make_plot(counts)
In this function, we use matplotlib to plot the total word counts at each time step. This information should be stored in the output of our stream function (counts) . 

