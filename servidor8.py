import socket
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cryptography.fernet import Fernet
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class ChatServer:
    def __init__(self, host='0.0.0.0', port=6060):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((host, port))
            self.server_socket.listen(5)
            print(f"Servidor escuchando en {host}:{port}")
            self.clients = []
            self.messageParts=""
            self.key = self.load_key()  # Cargar clave existente
            self.cipher = Fernet(self.key)

            self.thread = threading.Thread(target=self.accept_connections)
            self.thread.start()

            # Iniciar el servidor HTTP para manejar confirmaciones
            self.http_server = HTTPServer(('localhost', 6060), ConfirmationHandler)
            threading.Thread(target=self.http_server.serve_forever).start()

        except Exception as e:
            print(f"Error al iniciar el servidor: {e}")

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
                    message_parts = message.split(",")
                    if len(message_parts) < 1:
                        response = "false\n"
                    else:
                        tipo_mensaje = message_parts[0]  # "login" o "registro"
                        dato1_cliente = message_parts[1]  # Dato1 siempre debe coincidir
                        segundo_dato_cliente = message_parts[2]  # Dato2 o Dato3
                        
                        if tipo_mensaje == "registro":
                            if self.handle_registration(message_parts):
                                response = "false\n"
                            else:
                                response = "true\n"
                        if tipo_mensaje == "login":
                            if self.is_message_in_encrypted_file(dato1_cliente, segundo_dato_cliente):
                                response = "true\n"
                            else:
                                response = "false\n"
                        elif tipo_mensaje=="confirmación":
                            if self.send_email(dato1_cliente,"",segundo_dato_cliente):
                                response= "true\n"
                        else:
                            response = "tipo de mensaje no válido\n"

                    client_socket.send(response.encode('utf-8'))
                else:
                    break
            except Exception as e:
                break

        client_socket.close()
        self.clients.remove(client_socket)

    def handle_registration(self, message_parts):
        email = message_parts[1]  # Contraseña
        contrasena = message_parts[2]     # Email
        username = message_parts[3]  # Username

        # Verificar si ya existe el username, email o contraseña
        if self.is_message_in_encrypted_file2(email, username):
            return True  # Ya existe un registro
        else:
            self.write_encrypted_message_to_file(",".join(message_parts))
            # Enviar correo de confirmación
            subject = "Registro Exitoso"
            body = f"Hola {username},\n\nTu registro fue exitoso."
            self.send_email(email, subject, body, username)

            return False

    # Función para enviar correos electrónicos
    def send_email(self, to_email, subject, body, username):
        confirmation_link = f'http://localhost:6060/confirm?user={username}'  # Crea el enlace de confirmación
        body += f"\n\nPor favor, confirma tu registro haciendo clic en el siguiente enlace:\n{confirmation_link}"

        smtp_host = 'smtp.gmail.com'  # Servidor SMTP de Gmail
        smtp_port = 587  # Puerto para TLS
        from_email = 'intellihome058@gmail.com'  # Tu dirección de correo
        password = 'Abc12345$'  # Tu contraseña de correo

        # Crea el mensaje
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Agrega el cuerpo del mensaje
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Conéctate al servidor
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()  # Inicia TLS
            server.login(from_email, password)  # Inicia sesión
            server.send_message(msg)  # Envía el correo
            print('Correo enviado con éxito!')
        except Exception as e:
            print(f'Error al enviar el correo: {e}')
        finally:
            server.quit()  # Cierra la conexión

    # Función para escribir un mensaje cifrado en el archivo
    def write_encrypted_message_to_file(self, message):
        encrypted_message = self.cipher.encrypt(message.encode('utf-8'))
        with open('datos.txt', 'ab') as file:  # 'ab' para append en modo binario
            file.write(encrypted_message + b'\n')

    # Función para verificar si un mensaje ya está en el archivo cifrado
    def is_message_in_encrypted_file(self, dato1_cliente, segundo_dato_cliente):
        try:
            with open('datos.txt', 'rb') as file:
                encrypted_lines = file.readlines()
                for encrypted_line in encrypted_lines:
                    try:
                        decrypted_message = self.cipher.decrypt(encrypted_line.strip()).decode('utf-8')
                        stored_parts = decrypted_message.split(",")
                        dato1_archivo = stored_parts[1]
                        segundo_dato_archivo = stored_parts[2]
                        if (segundo_dato_cliente == dato1_archivo and (dato1_cliente == segundo_dato_archivo)):
                            return True
                    except Exception as e:
                        print(f"Error al desencriptar una línea: {e}")
            return False
        except FileNotFoundError:
            return False 

    def is_message_in_encrypted_file2(self, dato1_cliente, segundo_dato_cliente):
        try:
            with open('datos.txt', 'rb') as file:
                encrypted_lines = file.readlines()
                for encrypted_line in encrypted_lines:
                    try:
                        decrypted_message = self.cipher.decrypt(encrypted_line.strip()).decode('utf-8')
                        stored_parts = decrypted_message.split(",")
                        segundo_dato_archivo = stored_parts[2]
                        tercer_dato_archivo = stored_parts[3] 
                        if segundo_dato_cliente == tercer_dato_archivo or dato1_cliente == segundo_dato_archivo:
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

class ConfirmationHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # Obtener el nombre de usuario del parámetro de consulta
        username = query_params.get('user', [None])[0]
        if username:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Gracias por confirmar tu registro!')
            print(f"El usuario {username} ha confirmado su registro.")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Error: No se proporciono el nombre de usuario.')

if __name__ == "__main__":
    server = ChatServer()
