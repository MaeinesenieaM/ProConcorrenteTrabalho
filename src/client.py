from time import sleep
import threading

import server

class Client:
    def __init__(self, servidor: server.Server):
        self.servidor = servidor
        self.messages = {}
        threading.Thread(target = run, args = [self]).start()

    def print(self, text):
        self.servidor.add_request("print", text)

def run(cliente: Client):
    print("Cliente iniciado!")
    servidor = cliente.servidor
    while True:
        sleep(1)
        cliente.print("um!")
        cliente.print("dois!")
        sleep(1)
        cliente.print("tres!")

if __name__ == "__main__":
    print("W.I.P")