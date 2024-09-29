import socket
import threading

class ChatServer:
    print("clase")
    def __init__(self, host='0.0.0.0', port=2020):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((host, port))
            self.server_socket.listen(5)
            print(f"Servidor escuchando en {host}:{port}")
            self.clients = []

            self.thread = threading.Thread(target=self.accept_connections)
            self.thread.start()
        except:
            print("error2")
    def accept_connections(self):
        
        while True:
            print("Se ejecuta connections")
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f"Conexión de {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            
    def handle_client(self, client_socket):
        print("Handle")
        while True:
            try:
                # Recibir mensaje del cliente
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    # Imprimir mensaje recibido en la consola del servidor
                    print(f"Cliente dice: {message}")
                    
                    # Enviar "Hola" de vuelta al cliente
                    response = "Hola"
                    client_socket.send(response.encode('utf-8'))
                else:
                    break  # Salir del bucle si el mensaje está vacío o la conexión se cierra
            except:
                print("error")
        client_socket.close()
        self.clients.remove(client_socket)

    def close_server(self):
        for client in self.clients:
            client.close()
        self.server_socket.close()

if __name__ == "__main__":
    print("main")
    server = ChatServer()
    """while True:
        command = input(">> ")
        if command == "exit":
            server.close_server()
            break  # Salir del bucle principal
    """
