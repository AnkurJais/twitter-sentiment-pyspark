import configparser
import sys

class ConfigReader:

  def __init__(self, file):
    self.config = configparser.ConfigParser()
    try:
      self.config.read(file)
    except FileNotFoundError as ex:
      sys.exit("Config file does not exist")

  def get_config(self):
    return self.config
