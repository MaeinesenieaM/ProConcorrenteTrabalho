import threading
from client import Client

class Server:
    def __init__(self, assentos_quant):
        self.requests = {}
        self.clients = {}
        self.assentos = {f"{numero + 1}": None for numero in range(assentos_quant)}
        #self.lock = threading.Lock()
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        print("Servidor iniciado!")
        while True:
            self.check_requests()
    #Aki é a lógica inteira para checar os comandos enviados pelos clientes
    #a cada comando completo, o comando e retirado da lista self.requests
    #para evitar repetição.
    def check_requests(self):
        #with self.lock:
        remove_queue = []
        current_requests = self.requests.copy()
        for tipo, valores in current_requests.items():
            for valor in valores:
                match tipo:
                    case "reservar":
                        nome, assento = valor
                        if assento in self.assentos:
                            if self.assentos[assento] is None:
                                self.assentos[assento] = nome
                                print(f"[SERVER] Assento {assento} reservado com sucesso por {nome}.")
                            else:
                                print(f"[SERVER] Assento {assento} já está reservado por {self.assentos[assento]}.")
                        else:
                            print(f"[SERVER] Assento {assento} inválido.")
                        remove_queue.append((tipo, valor))
                    case "listar":
                        nome = valor
                        self.listar_assentos(nome)
                        remove_queue.append((tipo, valor))
                    case "sair":
                        print(f"[SERVER] Cliente {valor} saiu.")
                        remove_queue.append((tipo, valor))

        #Remove as requests de clientes da lista.
        for tipo, valor in remove_queue:
            if tipo in self.requests and valor in self.requests[tipo]:
                self.requests[tipo].remove(valor)

    def listar_assentos(self, nome):
        print(f"\n[SERVER] Assentos disponíveis para {nome}:\n")
        print("-" * 22, "TELA", "-" * 22)
        print("\n")

        colunas = 10  # 10 assentos por linha
        linha = ""
        for i, (numero, reservado_por) in enumerate(self.assentos.items(), start=1):
            if reservado_por:
                linha += f"[{reservado_por[0].upper():^3}] "

            else:
                linha += f"[{numero:>2}] "  # alinhamento com 2 dígitos

            if i % colunas == 0:
                print(linha)
                linha = ""
        if linha:
            print(linha)
        print()

    def add_request(self, request_type, param):
        if request_type not in self.requests:
            self.requests[request_type] = []
        self.requests[request_type].append(param)

    def add_client(self, name: str, client: Client):
        if name in self.clients:
            print("TODO!")
        self.clients[name] = client
