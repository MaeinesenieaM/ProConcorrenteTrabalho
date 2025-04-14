import threading

class Server:
    def __init__(self, assentos_quant):
        self.requests = {}
        self.assentos = {f"{numero + 1}": False for numero in range(assentos_quant)}
        threading.Thread(target = run, args = [self]).start()

    #Aki é a lógica inteira para checar os comandos enviados pelos clientes
    #a cada comando completo, o comando e retirado da lista self.requests.
    def check_requests(self):
        remove_queue = []
        for tipo, valor in self.requests.items():
            if tipo == "print":
                for texto in valor:
                    print(texto)
                    remove_queue.append((tipo, texto))
            else:
                print("COMANDO INVALIDO!")
                remove_queue.append((tipo, valor)) #Isso talvez quebre.


        for tipo, valor in remove_queue:
            self.requests[tipo].remove(valor)
            print(f"removido chamada: {tipo} {valor}")

    def add_request(self, request_type, param):
        if request_type not in self.requests:
            self.requests[request_type] = []
        self.requests[request_type].append(param)

def run(server):
    print("Server iniciado!")
    while True:
        server.check_requests()

if __name__ == "__main__":
    servidor = Server(10)
