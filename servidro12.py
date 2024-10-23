import socket
import threading
import serial
from cryptography.fernet import Fernet
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class ChatServer:
    def __init__(self, host='0.0.0.0', port=6060):
        print(host, port)
        self.arduino = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"Servidor escuchando en {host}:{port}")
        self.clients = []
        self.pending_confirmations = {}
        self.contrasena = None
        self.correo = None

        self.key = self.load_key()
        self.cipher = Fernet(self.key)

        self.thread = threading.Thread(target=self.accept_connections)
        self.thread.start()
        puertoSerial = "COM5"
        try:
            self.arduino = serial.Serial(puertoSerial, 9600)
            print(f"Conectado a Arduino en el puerto {puertoSerial}")
        except serial.SerialException as e:
            print(f"Error al conectar con Arduino: {e}")
        except Exception as e:
            print(f"Otro error: {e}")

    def load_key(self):
        try:
            with open('clave.key', 'rb') as key_file:
                return key_file.read()
        except FileNotFoundError:
            raise FileNotFoundError("Error: La clave de cifrado no se encuentra.")

    def accept_connections(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f"Conexión de {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8').strip()
                if message:
                    print(f"Cliente dice: {message}")
                    if message.startswith("GET"):
                        self.handle_http_request(message, client_socket)
                        continue

                    message_parts = message.split(",")
                    tipo_mensaje = message_parts[0]
                    response = "tipo de mensaje no válido\n"

                    if tipo_mensaje == "configuracion":
                        self.correo = message_parts[1]
                        self.contrasena = message_parts[2]

                        if self.verificarCorreo(self.correo):
                            confirmation_link = f"http://172.18.173.122:6060/confirm"
                            subject = "Confirmación de Cambios de Contraseña"
                            content = f"Por favor, confirma haciendo clic en: {confirmation_link}"
                            self.send_email(self.correo, subject, content)
                            response = "Enviado\n"
                        else:
                            response = "Fallo\n"
                    elif tipo_mensaje == "publicar":
                        ubicacion = message_parts[1].strip()
                        capacidad = message_parts[2].strip()
                        descripcion = message_parts[3].strip()
                    
                        # Las amenidades van desde la cuarta parte hasta el penúltimo elemento
                        amenidades = ", ".join(part.strip() for part in message_parts[4:-1])
                    
                        # El último elemento es el precio
                        precio = message_parts[-1].strip()

                        # Procesar los datos como sea necesario (ejemplo: guardar en archivo o base de datos)
                        print(f"Publicación recibida: Ubicación={ubicacion}, Capacidad={capacidad}, "
                            f"Descripción={descripcion}, Amenidades={amenidades}, Precio={precio}")

                        response = "Publicación recibida exitosamente\n"

                    elif tipo_mensaje == "leds":
                        self.conexionArduino(message_parts[1])

                    elif tipo_mensaje == "registro":
                        if self.handle_registration(message_parts):
                            response = "false\n"
                        else:
                            self.write_encrypted_message_to_file(message.strip())
                            response = "true\n"

                    elif tipo_mensaje == "login":
                        if self.verificarLogin(message_parts[1], message_parts[2]):
                            response = "true\n"
                        else:
                            response = "false\n"

                    print(f"Respuesta enviada: {response}")
                    client_socket.send(response.encode('utf-8'))
                else:
                    break

            except ConnectionResetError:
                print("El cliente cerró la conexión abruptamente.")
                break
            except Exception as e:
                print(f"Error al manejar el cliente: {e}")
                break

    def verificarCorreo(self, correo):
        try:
            with open('datos.txt', 'rb') as file:
                encrypted_lines = file.readlines()
                for encrypted_line in encrypted_lines:
                    decrypted_message = self.cipher.decrypt(encrypted_line.strip()).decode('utf-8')
                    stored_parts = decrypted_message.split(",")
                    if correo == stored_parts[2]:
                        return True
            return False
        except FileNotFoundError:
            return False

    def verificarLogin(self, dato_cliente, contrasena_cliente):
        try:
            with open('datos.txt', 'rb') as file:
                encrypted_lines = file.readlines()
                for encrypted_line in encrypted_lines:
                    decrypted_message = self.cipher.decrypt(encrypted_line.strip()).decode('utf-8')
                    stored_parts = decrypted_message.split(",")

                    # Verificar contraseña junto con correo, usuario o número de teléfono
                    if (
                        contrasena_cliente == stored_parts[1] and
                        (
                            dato_cliente == stored_parts[2] or  # Correo
                            dato_cliente == stored_parts[3] or  # Usuario
                            dato_cliente == stored_parts[4]     # Número de teléfono
                        )
                    ):
                        return True
            return False
        except FileNotFoundError:
            print("Error: El archivo 'datos.txt' no se encuentra.")
            return False

    def conexionArduino(self, mensaje):
        if self.arduino:
            self.arduino.write(mensaje.encode("utf-8"))

    def send_email(self, to_email, subject, content):
        message = Mail(
            from_email='intellihome060@gmail.com',
            to_emails=to_email,
            subject=subject,
            plain_text_content=content
        )
        try:
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            print(f"Correo enviado: {response.status_code}")
        except Exception as e:
            print(f"Error al enviar correo: {e}")

    def handle_registration(self, message_parts):
        password = message_parts[1]
        email = message_parts[2]
        username = message_parts[3]
        if self.is_message_in_encrypted_file2(email, username):
            return True
        else:
            self.write_encrypted_message_to_file(",".join(message_parts))
            return False

    def write_encrypted_message_to_file(self, message):
        encrypted_message = self.cipher.encrypt(message.encode('utf-8'))
        with open('datos.txt', 'ab') as file:
            file.write(encrypted_message + b'\n')

    def is_message_in_encrypted_file2(self, email, username):
        try:
            with open('datos.txt', 'rb') as file:
                encrypted_lines = file.readlines()
                for encrypted_line in encrypted_lines:
                    decrypted_message = self.cipher.decrypt(encrypted_line.strip()).decode('utf-8')
                    stored_parts = decrypted_message.split(",")
                    if email == stored_parts[2] or username == stored_parts[3]:
                        return True
            return False
        except FileNotFoundError:
            return False

    def close_server(self):
        for client in self.clients:
            client.close()
        self.server_socket.close()
        if self.arduino:
            self.arduino.close()

    def handle_http_request(self, request, client_socket):
        try:
            print("Solicitud HTTP recibida")
            headers = request.splitlines()
            method, path, _ = headers[0].split()
            self.update_password()
            response = "Confirmada\n"
            print(response)
            client_socket.send(response.encode('utf-8'))
        except Exception as e:
            print(f"Error en la solicitud HTTP: {e}")
            client_socket.send(b"HTTP/1.1 404 Not Found\n\nRuta no encontrada.")

    def update_password(self):
        print("Actualiza la contraseña en el archivo de datos.")
        try:
            with open('datos.txt', 'rb') as file:
                encrypted_lines = file.readlines()

            updated_lines = []
            for encrypted_line in encrypted_lines:
                decrypted_message = self.cipher.decrypt(encrypted_line.strip()).decode('utf-8')
                stored_parts = decrypted_message.split(",")
                if self.correo == stored_parts[2]:
                    stored_parts[1] = self.contrasena
                    updated_message = ",".join(stored_parts)
                    updated_lines.append(self.cipher.encrypt(updated_message.encode('utf-8')) + b'\n')
                else:
                    updated_lines.append(encrypted_line)

            with open('datos.txt', 'wb') as file:
                file.writelines(updated_lines)
        except FileNotFoundError:
            print("Error: El archivo de datos no se encuentra.")

if __name__ == "__main__":
    server = ChatServer()