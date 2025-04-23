import threading
import time

class Servidor:
    def __init__(self, quantidade_assentos: int):
        self.requests = {}
        self.clients = {}
        self.assentos = {f"{numero + 1}": None for numero in range(quantidade_assentos)}
        self.lock = threading.Lock()
        threading.Thread(target=self.run, daemon=True).start()
        print("[SERVER] Servidor iniciado!")

    def get_client(self, nome: str) -> "Cliente":
        return self.clients[nome]

    def run(self):
        while True:
            with self.lock:
                #Sim, o servidor é apenas isso.
                self.check_requests()

    #Aki é a lógica inteira para checar os comandos enviados pelos clientes
    #a cada comando completo, o comando e retirado da lista self.requests
    #para evitar repetição.
    def check_requests(self):
        remove_queue = []
        current_requests = self.requests.copy()
        for tipo, valores in current_requests.items():
            for valor in valores:
                match tipo:
                    case "reservar":
                        nome, assento = valor
                        if assento in self.assentos:
                            print(f"[SERVER] Verificando Assento {assento} para {nome}.")
                            if self.assentos[assento] is None:
                                self.assentos[assento] = nome
                                resposta = f"Assento {assento} reservado com sucesso por {nome}."
                            else:
                                resposta = f"Assento {assento} já está reservado por {self.assentos[assento]}."
                            self.get_client(nome).add_response("reservado", resposta)
                        else:
                            print(f"[SERVER] Assento {assento} inválido.")
                            self.get_client(nome).add_response("reservado", None)
                        remove_queue.append((tipo, valor))
                    case "listar":
                        nome = valor
                        self.get_client(nome).add_response("assentos", self.assentos)
                        print(f"[SERVER] Enviado assentos para: {nome}")
                        remove_queue.append((tipo, valor))
                    case "sair":
                        nome = valor
                        self.clients.pop(nome, None)
                        print(f"[SERVER] Cliente {nome} saiu.")
                        remove_queue.append((tipo, nome))
                    case _:
                        print(f"[SERVER] Recebido pedido invalido!: {tipo}")
                        remove_queue.append((tipo, valor))

        #Remove as requests de clientes ja concluídos da lista.
        for tipo, valor in remove_queue:
            if tipo in self.requests and valor in self.requests[tipo]:
                self.requests[tipo].remove(valor)

    def add_request(self, request_type, param):
        if request_type not in self.requests:
            self.requests[request_type] = []
        self.requests[request_type].append(param)

    def add_client(self, name: str, cliente: "Cliente"):
        if name in self.clients:
            print("TODO!")
        self.clients[name] = cliente

class Cliente:
    def __init__(self, nome: str, servidor: "Servidor"):
        self.server = servidor
        self.response = {}
        self.nome = nome
        servidor.add_client(self.nome, self) #Adiciona o cliente para a lista do servidor.
        print(f"[Cliente: {self.nome}] Criado!")

    def start(self):
        print(f"[Cliente: {self.nome}] Iniciado!")
        thread = threading.Thread(target=self._menu)
        thread.start()
        return thread

    def _menu(self):
        while True:
            print("\nOpções:")
            print("1. Ver assentos disponíveis")
            print("2. Reservar assento")
            print("3. Sair")
            escolha = input("Digite sua opção: ")

            if escolha == "1":
                self._listar_assentos()
            elif escolha == "2":
                assento = input("Digite o número do assento que deseja reservar: ")
                self._reservar(assento)
            elif escolha == "3":
                self.server.add_request("sair", self.nome)
                print(f"Encerrando cliente {self.nome}...")
                break
            else:
                print("Opção inválida.")
                time.sleep(0.5)

    def _reservar(self, assento):
        self.server.add_request("reservar", (self.nome, assento))
        resposta = self._listen_type("reservado")
        if resposta is None:
            print(f"[Cliente: {self.nome}] RESERVA COM ASSENTO INVALIDO!")
        else:
            print(resposta)

    def _listar_assentos(self):
        self.server.add_request("listar", self.nome)
        assentos = self._listen_type("assentos")
        if assentos is None:
            print(f"[Cliente: {self.nome}] Lista de assentos recebida Invalida!")
        else:
            self._imprimir_assentos(assentos)

    def add_response(self, tipo: str, valor):
        self.response[tipo] = valor

    def _listen_type(self, tipo: str):
        espera = time.time()
        while True:
            segundos = 5
            if time.time() - espera > segundos:
                print(f"[Cliente: {self.nome}] Servidor não esta respondendo!")
                return None
            if not self.response: continue
            resposta = self.response[tipo]
            self.response.pop(tipo, None)
            return resposta

    def _imprimir_assentos(self, assentos):
        print(f"\nAssentos disponíveis para {self.nome}:\n")
        print("-" * 22, "TELA", "-" * 22)
        print("\n")

        colunas = 10  # 10 assentos por linha
        linha = ""
        for i, (numero, reservado_por) in enumerate(assentos.items(), start=1):
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