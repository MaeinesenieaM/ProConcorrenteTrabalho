import threading
import time
from server import Server

class Client:
    def __init__(self, servidor: Server):
        self.server = servidor
        self.server_response = {}
        self.nome = str(input("Digite seu nome: "))

        servidor.add_client(self.nome, self)

        threading.Thread(target=self.run).start()

    def reservar(self, assento):
        self.server.add_request("reservar", (self.nome, assento))
        resposta = self.listen_type("reservado")
        print(resposta)

    def listar_assentos(self):
        self.server.add_request("listar", self.nome)
        assentos = self.listen_type("assentos")
        if assentos is None:
            print("TODO!")
        print(assentos)

    def sair(self):
        self.server.add_request("sair", self.nome)
        print(f"Encerrando cliente {self.nome}...")
        exit(0)

    def run(self):
        print(f"Cliente {self.nome} iniciado!")
        while True:
            time.sleep(0.2)
            print("\nOpções:")
            print("1. Ver assentos disponíveis")
            print("2. Reservar assento")
            print("3. Sair")
            escolha = input("Digite sua opção: ")

            if escolha == "1":
                self.listar_assentos()
            elif escolha == "2":
                assento = input("Digite o número do assento que deseja reservar: ")
                self.reservar(assento)
            elif escolha == "3":
                self.sair()
            else:
                print("Opção inválida.")
                time.sleep(0.5)

    def listen_type(self, tipo: str):
        espera = time.time()
        while True:
            segundos = 5
            if time.time() - espera > segundos:
                print("Servidor não esta respondendo!")
                return ""
            if not self.server_response: continue
            if not self.server_response[tipo]:
                print("ERRO CRITICO! TIPO DE RESPOSTA ESPERADA NÃO FOI ATENDIDA!")
                return ""
            return self.server_response[tipo].items()