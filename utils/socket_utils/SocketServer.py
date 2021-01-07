from utils.socket_utils.SocketUtils import SocketUtils

class SocketServer:

  def __init__(self):
    self.socket = SocketUtils.get_connection()
    self.socket.bind((SocketUtils.HOST, SocketUtils.PORT))
    self.socket.listen(5)
    self.connected_client = None

  def start_server(self):
    self.socket_client, addr = self.socket.accept()
    print("Received request from: " + str(addr))
    return self.socket_client

  def send_data(self, data):
    if self.connected_client == None:
      self.connected_client = self.start_server()
    self.connected_client.send(data)

  def close_connection(self):
    self.socket_client.close()

if __name__ == "__main__":
  SocketServer().send_data("hell".encode("utf-8"))