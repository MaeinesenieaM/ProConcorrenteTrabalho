from time import sleep

import server
import client

if __name__ == "__main__":
    servidor = server.Server(50)
    cliente = client.Client(servidor)