import socket
import threading
from cryptography.fernet import Fernet

class ChatServer:
    print(1)
    def __init__(self, host='0.0.0.0', port=6060):
        print(host,port)
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
                message = client_socket.recv(1024).decode('utf-8').strip()
                if message:
                    print(f"Cliente dice: {message}")

                    # Dividir el mensaje recibido en tipo y datos
                    message_parts = message.split(",")
                    print(message_parts)
                    if len(message_parts) < 1:
                        response = "false\n"
                    else:
                        tipo_mensaje = message_parts[0]  # "login" o "registro"
                        dato1_cliente = message_parts[1]  # Dato1 siempre debe coincidir
                        segundo_dato_cliente = message_parts[2]  # Dato2 o Dato3
                        print(dato1_cliente,segundo_dato_cliente)
                        if tipo_mensaje == "registro":
                            if self.handle_registration(message_parts):
                                print("false")
                                response ="false\n"
                            # Si es un registro, almacenar el mensaje
                            else:
                                print("true")
                                self.write_encrypted_message_to_file(message.strip())
                                response = "true\n"
                                
                        elif tipo_mensaje == "login":
                            # Verificar el mensaje en el archivo para login
                            if self.is_message_in_encrypted_file(dato1_cliente, segundo_dato_cliente):
                                response = "true\n"
                            else:
                                print("no encontrado")
                                response = "false\n"
                        else:
                            response = "tipo de mensaje no válido\n"

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

    def handle_registration(self, message_parts):
        password = message_parts[1]  # Contraseña
        email = message_parts[2]     # Email
        username = message_parts[3]  # Username
        print(f"Registro - Contraseña: {password}, Email: {email}, Username: {username}")

        # Verificar si ya existe el username, email o contraseña
        if self.is_message_in_encrypted_file2(email, username):
            print("Registro fallido - Datos ya en uso")
            return True # Ya existe un registro
        else:
            self.write_encrypted_message_to_file(",".join(message_parts))
            print("Registro exitoso")
            return False
    # Función para escribir un mensaje cifrado en el archivo
    def write_encrypted_message_to_file(self, message):
        encrypted_message = self.cipher.encrypt(message.encode('utf-8'))
        with open('datos.txt', 'ab') as file:  # 'ab' para append en modo binario
            file.write(encrypted_message + b'\n')

    # Función para verificar si un mensaje ya está en el archivo cifrado
    def is_message_in_encrypted_file(self, dato1_cliente, segundo_dato_cliente):
        print("verificación")
        try:
            with open('datos.txt', 'rb') as file:
                encrypted_lines = file.readlines()
                for encrypted_line in encrypted_lines:
                    try:
                        print("verificación 2")
                        # Desencriptar la línea almacenada
                        decrypted_message = self.cipher.decrypt(encrypted_line.strip()).decode('utf-8')
                        
                        # Dividir la línea desencriptada
                        stored_parts = decrypted_message.split(",")
                        
                          
                        dato1_archivo = stored_parts[1]
                        segundo_dato_archivo = stored_parts[2]  
                        tercer_dato_archivo = stored_parts[3] 
                            
                        if (segundo_dato_cliente == dato1_archivo and (dato1_cliente == segundo_dato_archivo or dato1_cliente == tercer_dato_archivo)):
                            return True
                    except Exception as e:
                        print(f"Error al desencriptar una línea: {e}")
            return False
        except FileNotFoundError:
            return False 
    def is_message_in_encrypted_file2(self, dato1_cliente, segundo_dato_cliente):
        print("verificación")
        try:
            with open('datos.txt', 'rb') as file:
                encrypted_lines = file.readlines()
                for encrypted_line in encrypted_lines:
                    try:
                        print("verificación 2")
                        # Desencriptar la línea almacenada
                        decrypted_message = self.cipher.decrypt(encrypted_line.strip()).decode('utf-8')
                        
                        # Dividir la línea desencriptada
                        stored_parts = decrypted_message.split(",")
                        
                          

                        segundo_dato_archivo = stored_parts[2]  
                        tercer_dato_archivo = stored_parts[3] 
                        print(segundo_dato_archivo,dato1_cliente,tercer_dato_archivo,segundo_dato_cliente)   
                        if segundo_dato_cliente==tercer_dato_archivo or dato1_cliente==segundo_dato_archivo:
                            return True
                    except Exception as e:
                        print(f"Error al desencriptar una línea: {e}")
            return False
        except FileNotFoundError:
            return False 
    def close_server(self):
        for client in self.clients:
            client.close()
        self.server_socket.close()

if __name__ == "__main__":
    server = ChatServer()
