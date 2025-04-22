import threading
import server
import time

class Client:
    def __init__(self, servidor: server.Server):
        self.servidor = servidor
        self.nome = input("Digite seu nome: ")
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def reservar(self, assento):
        self.servidor.add_request("reservar", (self.nome, assento))

    def listar_assentos(self):
        self.servidor.add_request("listar", self.nome)

    def sair(self):
        self.servidor.add_request("sair", self.nome)

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
                print(f"Encerrando cliente {self.nome}...")
                break
            else:
                print("Opção inválida.")

                time.sleep(0.2)
