import cinema
import time

if __name__ == "__main__":
    assentos = input("quantos assentos?")
    servidor = cinema.Servidor(int(assentos))
    time.sleep(1)

    while True:
        cliente = cinema.Cliente(servidor)
        cliente.thread.join()

        continuar = input("Deseja cadastrar outro usuário? (s/n): ").strip().lower()
        if continuar != 's':
            print("Encerrando sistema.")
            break