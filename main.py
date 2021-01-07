from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from utils.socket_utils.SocketUtils import SocketUtils
from textblob import TextBlob

def preprocessing(lines):
    lines.printSchema()
    words = lines.select(explode(split(lines.value, "t_end")).alias('word'))
    words.dropna()
    words.printSchema()
    words = words.withColumn('word', regexp_replace('word', r'http\S+', ''))
    words = words.withColumn('word', regexp_replace('word', '@\w+', ''))
    words = words.withColumn('word', regexp_replace('word', '#', ''))
    words = words.withColumn('word', regexp_replace('word', 'RT', ''))
    words = words.withColumn('word', regexp_replace('word', ':', ''))
    return words

def polarity_detection(text):
    return TextBlob(text).sentiment.polarity

def subjectivity_detection(text):
    return TextBlob(text).sentiment.subjectivity

def text_classification(words):
    # polarity detection
    polarity_detection_udf = udf(polarity_detection, StringType())
    words = words.withColumn("polarity", polarity_detection_udf("word"))
    # subjectivity detection
    subjectivity_detection_udf = udf(subjectivity_detection, StringType())
    words = words.withColumn("subjectivity", subjectivity_detection_udf("word"))
    return words

if __name__ == "__main__":
    # create Spark session
    spark = SparkSession.builder.appName("TwitterSentimentAnalysisSpark").master("local[*]")\
      .enableHiveSupport().getOrCreate()
    # read the tweet data from socket
    lines = spark.readStream.format("socket").option("host",SocketUtils.HOST).option("port",SocketUtils.PORT).load()
    # Preprocess the data
    words = preprocessing(lines)
    # text classification to define polarity and subjectivity
    words = text_classification(words)
    query = words.writeStream.queryName("all_tweets")\
        .outputMode("append").format("parquet")\
        .option("path", "hdfs://localhost:9000/user/ankur/datasets/twitter/")\
        .option("checkpointLocation", "./check")\
        .trigger(processingTime='60 seconds').start()
    query.awaitTermination()