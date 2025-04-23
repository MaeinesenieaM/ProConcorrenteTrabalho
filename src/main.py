import cinema
import time

if __name__ == "__main__":
    assentos = input("quantos assentos?")
    servidor = cinema.Servidor(int(assentos))

    while True:
        nome = str(input("Digite seu nome: "))
        cliente = cinema.Cliente(nome, servidor)
        cliente_thread = cliente.start()

        cliente_thread.join()

        continuar = input("Deseja cadastrar outro usuário? (s/n): ").strip().lower()
        if continuar != 's':
            print("Encerrando sistema.")
            break