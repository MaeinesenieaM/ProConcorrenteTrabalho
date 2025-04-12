import threading

def run(server):
    print("Server iniciado!")
    while True:
        server.check_requests()

class Server:
    def __init__(self, assentos_quant):
        self.requests = {}
        self.assentos = {f"{numero + 1}": False for numero in range(assentos_quant)}
        threading.Thread(target = run, args = [self]).start()

    def check_requests(self):
        for tipo, param in self.requests.items():
            if tipo == "print":
                print(param)

        self.requests.clear()

if __name__ == "__main__":
    servidor = Server(10)
