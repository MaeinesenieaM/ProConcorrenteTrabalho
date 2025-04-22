import server
import client
import time

if __name__ == "__main__":
    servidor = server.Server(100)
    time.sleep(1)

    while True:
        cliente = client.Client(servidor)
        cliente.thread.join()

        continuar = input("Deseja cadastrar outro usuário? (s/n): ").strip().lower()
        if continuar != 's':
            print("Encerrando sistema.")
            break
