import threading
import socket
import pickle
from threading import Thread


class SockServer(object):
    def __init__(self, host, port):
        self.clients = set()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):  # Функция, ожидающая новых подключений
        self.sock.listen(500)
        while True:
            client, address = self.sock.accept()  # При подключении клиента
            print(address)
            self.clients.add(client)  # Он добавляется в множество clients
            threading.Thread(target=self.listenToClient, args=(client, address)).start()
            # И в отдельном потоке запускается

    def listenToClient(self, client, address):  # Функция прослушивания сообщений
        size = 4096
        all_data = bytearray()
        while True:
            try:
                data = client.recv(size)  # Получаем сообщение
                if data:
                    for other in self.clients:  # Рассылаем его всем остальным клиентам
                        if other != client:
                            print('Recv: {}: {}'.format(len(data), data))
                            all_data += data
                            print('All data: {}'.format(all_data))
                            obj = pickle.loads(all_data)
                            print(obj)
                            other.send(data)
                else:
                    self.clients.remove(client)  # Если клиент отключился, вычеркиваем его из множества

            except:
                client.close()
                try:
                    self.clients.remove(client)
                except:
                    pass


SockServer(socket.gethostbyname('0.0.0.0'), 5000).listen()
