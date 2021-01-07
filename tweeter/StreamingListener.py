import tweepy
import json
from utils.socket_utils.SocketServer import SocketServer

class StreamingListener(tweepy.StreamListener):

  def __init__(self):
    self.socket_client = SocketServer()

  def on_status(self, status):
      print(status.text)

  def on_disconnect(self, notice):
    super().on_disconnect(notice)
    self.socket_client.close_connection()

  def on_error(self, status_code):
      if status_code == 420:
          return False

  def on_data(self, raw_data):
    json_data = json.loads(raw_data)
    # If tweeet is more than 140 characters
    if "extended_tweet" in json_data:
      self.socket_client.send_data(str(json_data['extended_tweet']['full_text']+"t_end")
            .encode('utf-8'))
      print(json_data['extended_tweet']['full_text'])
    else:
      self.socket_client.send_data(str(json_data['text'] + "t_end")
              .encode('utf-8'))
      print(json_data['text'])