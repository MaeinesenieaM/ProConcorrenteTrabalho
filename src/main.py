import cinema
import time

if __name__ == "__main__":
    assentos = input("quantos assentos?")
    #O servidor é iniciado assim que é criado, com sua propria thread e loop.
    servidor = cinema.Servidor(int(assentos))

    while True:
        nome = str(input("Digite seu nome: "))
        #Diferente do servidor, é necessário acordar o cliente para usar pelo prompt de comando.
        cliente = cinema.Cliente(nome, servidor)
        #Acorda o cliente e recebe sua Thread. (Fortemente recomendado acordar um cliente por vez.)
        cliente_thread = cliente.start()

        cliente_thread.join() #Espera que o cliente termine sua função.

        #Aki abaixo é mais exclusivo para esta demonstração, é possível criar múltiplos clientes e
        # usa-los um por vez. Não é o melhor sistema de todos, mas foi o que encontramos.
        continuar = input("Deseja cadastrar outro usuário? (s/n): ").strip().lower()
        if continuar != 's':
            print("Encerrando sistema.")
            break