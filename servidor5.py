import socket
import threading
from cryptography.fernet import Fernet

class ChatServer:
    def __init__(self, host='0.0.0.0', port=2020):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((host, port))
            self.server_socket.listen(5)
            print(f"Servidor escuchando en {host}:{port}")
            self.clients = []

            # Cargar clave de cifrado existente
            self.key = self.load_key()  # Cargar clave existente
            self.cipher = Fernet(self.key)

            self.thread = threading.Thread(target=self.accept_connections)
            self.thread.start()
        except Exception as e:
            print(f"Error al iniciar el servidor: {e}")

    def load_key(self):
        # Cargar la clave si existe, lanzar error si no se encuentra
        try:
            with open('clave.key', 'rb') as key_file:
                return key_file.read()
        except FileNotFoundError:
            raise FileNotFoundError("Error: La clave de cifrado no se encuentra. Asegúrate de que el archivo 'clave.key' existe.")

    def accept_connections(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f"Conexión de {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                # Recibir mensaje del cliente
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Cliente dice: {message}")

                    if self.is_message_in_encrypted_file(message.strip()):
                        response = "true\n"

                    else:
                        # Escribir mensaje cifrado en el archivo
                        #self.write_encrypted_message_to_file(message + "\n")
                        response = "false\n"

                    # Enviar respuesta de vuelta al cliente
                    print(f"Respuesta enviada: {response}")
                    client_socket.send(response.encode('utf-8'))
                else:
                    break  # Salir si el mensaje está vacío o la conexión se cierra
            except Exception as e:
                print(f"Error al manejar el cliente: {e}")
                break

        client_socket.close()
        self.clients.remove(client_socket)

    # Función para escribir un mensaje cifrado en el archivo
    def write_encrypted_message_to_file(self, message):
        encrypted_message = self.cipher.encrypt(message.encode('utf-8'))
        with open('datos.txt', 'ab') as file:  # 'ab' para append en modo binario
            file.write(encrypted_message + b'\n')

    # Función para verificar si un mensaje ya está en el archivo cifrado
    def is_message_in_encrypted_file(self, message):
        try:
            with open('datos.txt', 'rb') as file:
                encrypted_lines = file.readlines()
                for encrypted_line in encrypted_lines:
                    try:
                        decrypted_message = self.cipher.decrypt(encrypted_line.strip()).decode('utf-8')
                        if decrypted_message == message:
                            return True
                    except Exception as e:
                        print(f"Error al desencriptar una línea: {e}")
            return False
        except FileNotFoundError:
            return False  # Si el archivo no existe, el mensaje no está

    def close_server(self):
        for client in self.clients:
            client.close()
        self.server_socket.close()

if __name__ == "__main__":
    server = ChatServer()
