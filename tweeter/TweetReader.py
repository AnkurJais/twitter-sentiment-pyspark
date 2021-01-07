import tweepy
import os
from tweeter.StreamingListener import StreamingListener
from config.ConfigReader import ConfigReader
from constants import DirectoryConstants
from constants import FileConstants

class TweetReader:

  def __init__(self):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "../", DirectoryConstants.CONFIG, FileConstants.TWEETER_CONFIG)
    config = ConfigReader(config_file).get_config()
    api_credentials = config['api']
    self.auth = tweepy.OAuthHandler(api_credentials['consumer_key'], api_credentials['consumer_secret'])
    self.auth.set_access_token(api_credentials['api_key'], api_credentials['api_secret'])
    self.api = tweepy.API(self.auth)

  def get_public_tweets(self):
    public_tweets = self.api.home_timeline()
    for tweet in public_tweets:
      print(tweet.text)

  def get_streaming_tweets(self, *keyword):
    myStream = tweepy.Stream(auth=self.auth, listener=StreamingListener())
    myStream.filter(track=keyword, languages=["en"])

if __name__ == "__main__":
  TweetReader().get_streaming_tweets("covid")