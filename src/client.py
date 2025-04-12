from time import sleep
import threading

import server

def run(cliente):
    print("Cliente iniciado!")
    while True:
        sleep(1)
        cliente.send_print("FUNCIONA!")

class Client:
    def __init__(self, servidor: server.Server):
        self.servidor = servidor
        self.messages = {}
        threading.Thread(target = run, args = [self]).start()

    def send_print(self, text):
        self.servidor.requests[f'print'] = text

if __name__ == "__main__":
    print("W.I.P")