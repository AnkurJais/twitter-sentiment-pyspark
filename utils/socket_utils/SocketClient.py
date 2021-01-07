from utils.socket_utils.SocketUtils import SocketUtils
import socket

class SocketClient:

  def __init__(self):
    self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket_client.connect((SocketUtils.HOST, SocketUtils.PORT))

  def read_data(self):
    while True:
      data = self.socket_client.recv(1024)
      print(data)

if __name__ == "__main__":
  client = SocketClient()
  client.read_data()