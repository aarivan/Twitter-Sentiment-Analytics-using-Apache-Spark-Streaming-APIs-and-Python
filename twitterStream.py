from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import operator
import numpy as np
import matplotlib.pyplot as plt


def main():
    conf = SparkConf().setMaster("local[2]").setAppName("Streamer")
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 10)   # Create a streaming context with batch interval of 10 sec
    ssc.checkpoint("checkpoint")

    pwords = load_wordlist("positive.txt")
    nwords = load_wordlist("negative.txt")
   
    counts = stream(ssc, pwords, nwords, 100)
    make_plot(counts)


def make_plot(counts):
    """
    Plot the counts for the positive and negative words for each timestep.
    Use plt.show() so that the plot will popup.
    """
    plt.xlabel('Time Step')
    plt.ylabel('Word Count')
    positive = []
    negative = []
    count = []
    print counts
    for timestep in counts:
        positive.append(int(timestep[0]))
        negative.append(int(timestep[1]))
    for i in range(0,len(positive)):
        count.append(i)
    pos1, = plt.plot(count,positive)
    neg1, = plt.plot(count,negative)
    plt.legend([pos1,neg1],['Positive','Negative'])
    plt.axis([0,10,0,300])
    plt.show()


def load_wordlist(filename):
    """ 
    This function should return a list or set of words from the given filename.
    """    
    file = open(filename,'rU')
    words = set(line.strip() for line in file)

    return words


def orientation(word,pwords,nwords):
    if word in pwords:
        return ('positive',1)
    elif word in nwords:
        return ('negative',1)


def updateFunction(newValues, runningCount):
    if runningCount is None:
        runningCount = 0
    return sum(newValues, runningCount)


def stream(ssc, pwords, nwords, duration):
    
    kstream = KafkaUtils.createDirectStream(
        ssc, topics = ['twitterstream'], kafkaParams = {"metadata.broker.list": 'localhost:9092'})
    tweets = kstream.map(lambda x: x[1].encode("ascii","ignore"))

    # Each element of tweets will be the text of a tweet.
    # You need to find the count of all the positive and negative words in these tweets.
    # Keep track of a running total counts and print this at every time step (use the pprint function).

    words = tweets.flatMap(lambda k: k.split(" "))
    wordsType = words.map(lambda k: orientation(k,pwords,nwords))
    ct = wordsType.reduceByKey(lambda a, b : a + b)

    # Let the counts variable hold the word counts for all time steps
    # You will need to use the foreachRDD function.
    # For our implementation, counts looked like:
    #   [[("positive", 100), ("negative", 50)], [("positive", 80), ("negative", 60)], ...]

    counts = []
    cts = ct.updateStateByKey(updateFunction)
    ct.foreachRDD(lambda t,rdd: counts.append(rdd.collect()))
    cts.pprint()
    # YOURDSTREAMOBJECT.foreachRDD(lambda t,rdd: counts.append(rdd.collect()))

    ssc.start()                         # Start the computation
    ssc.awaitTerminationOrTimeout(duration)
    ssc.stop(stopGraceFully=True)
    
    return counts


if __name__=="__main__":
    main()
