import socket
import sys

class SocketUtils:
  HOST = "127.0.0.1"
  PORT = 9936
  socket_client = None

  def __init__(self):
    if SocketUtils.socket_client != None:
      raise Exception("Cannot create object directly, use get_connection instead.")
    else:
      try:
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      except socket.error as err:
        print("Error occured while socket_utils initialization: {}".format(err))
        sys.exit()
      SocketUtils.socket_client = socket_client

  @staticmethod
  def get_connection():
    if SocketUtils.socket_client == None:
      SocketUtils()
    return SocketUtils.socket_client