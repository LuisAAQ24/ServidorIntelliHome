import socket
import threading
import serial 
from cryptography.fernet import Fernet
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import uuid  # Para generar un token único
from urllib.parse import urlparse, parse_qs  # Para procesar la URL

class ChatServer:
    def __init__(self, host='0.0.0.0', port=6060):
        print(host, port)
        self.arduino= None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"Servidor escuchando en {host}:{port}")
        self.clients = []
        self.pending_confirmations = {}  # Almacenar las confirmaciones pendientes
        self.contrasena= None
        self.correo= None
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
                message = client_socket.recv(4096).decode('utf-8').strip()
                if message:
                    print(f"Cliente dice: {message}")
                    if message.startswith("GET"):
                        self.handle_http_request(message, client_socket)
                        continue 
                    message_parts = message.split(",")
                    tipo_mensaje = message_parts[0]  # "configuracion", "registro" o "login"
                    response = "tipo de mensaje no válido\n"
                    if tipo_mensaje == "configuracion":
                        self.correo = message_parts[1]
                        self.contrasena = message_parts[2]
                            
                            # Verificar si el correo existe
                        if self.verificarCorreo(self.correo):
                                # Omitir token y enviar correo directamente
                            confirmation_link = f"http://172.18.173.122:6060/confirm"
                            subject = "Confirmación de Cambios de Contraseña"
                            content = f"Se ha solicitado un cambio de contraseña. Por favor, confirma haciendo clic en el siguiente enlace: {confirmation_link}"
                            self.send_email(self.correo, subject, content)

                            response = "Enviado\n"
                        else:
                            response = "Fallo\n"
                    elif tipo_mensaje == "alquilar":
                        self.write_encrypted_message_to_file(message.strip(),"alquileres.txt")
                        response ="true\n"
                    elif tipo_mensaje == "publicar":
                        self.write_encrypted_message_to_file(message.strip(),"propiedades.txt")
                        response ="true\n"
                    elif tipo_mensaje == "leds":
                        self.conexionArduino(message_parts[1])
                    elif tipo_mensaje == "obtener_alquileres":
                        response = self.obtener_alquileres() 
                    elif tipo_mensaje == "registro":
                        if self.handle_registration(message_parts):
                            response = "false\n"
                        else:
                            self.write_encrypted_message_to_file(message.strip(),"datos.txt")
                            response = "true\n"
                    elif tipo_mensaje == "login":
                        if self.verificarLogin(message_parts[1], message_parts[2]):
                            response = "true\n"
                        else:
                            response = "false\n"
                    else:
                        response = "tipo de mensaje no válido\n"

                    print(f"Respuesta enviada: {response}")
                    client_socket.send(response.encode('utf-8'))
                else:
                    break

            except ConnectionResetError:
                # Manejar el error cuando el cliente cierra la conexión abruptamente
                print("El cliente cerró la conexión abruptamente.")
                break
            except Exception as e:
                print(f"Error al manejar el cliente: {e}")
                break

    def verificarCorreo(self, correo):
        """Verifica si el correo existe en el archivo de datos."""
        try:
            with open('datos.txt', 'rb') as file:
                encrypted_lines = file.readlines()
                for encrypted_line in encrypted_lines:
                    decrypted_message = self.cipher.decrypt(encrypted_line.strip()).decode('utf-8')
                    stored_parts = decrypted_message.split(",")
                    if correo == stored_parts[2]:  # Correo en la posición correspondiente
                        return True
            return False
        except FileNotFoundError:
            return False
    def conexionArduino(self, mensaje):
        if self.arduino != None:
            self.arduino.write(mensaje.encode("utf-8"))
    def send_email(self, to_email, subject, content):
        message = Mail(from_email='intellihome060@gmail.com',
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
            return True  # Ya existe un registro
        else:
            self.write_encrypted_message_to_file(",".join(message_parts),"datos.txt")
            return False

    def write_encrypted_message_to_file(self, message, file):
        try:
            encrypted_message = self.cipher.encrypt(message.encode('utf-8'))
            with open(file, 'ab') as file:
                file.write(encrypted_message + b'\n')
        except Exception as e:
            print(f"Error al escribir en el archivo: {e}")

    def obtener_alquileres(self):
        try:
            alquileres = []
            with open('propiedades.txt', 'rb') as file:
                encrypted_lines = file.readlines()
                for encrypted_line in encrypted_lines:
                    decrypted_message = self.cipher.decrypt(encrypted_line.strip()).decode('utf-8')
                    alquiler_data = decrypted_message.split(",") 
                    

                    descripción = alquiler_data[1] 
                    capacidad = alquiler_data[2]  
                    ubicacion = alquiler_data[3]  
                    amenidades =  alquiler_data[4]    
                    precio = alquiler_data[5] 
                    reglas = alquiler_data[6] 
                    fechainicio = alquiler_data[7]
                    fechafin = alquiler_data[8]   

                        # Formatear como "dato1,dato2,dato3,dato4,dato5,dato6"
                    alquiler = f"{descripción},{capacidad},{ubicacion},{amenidades},{precio},{reglas},{fechainicio},{fechafin}"
                    alquileres.append(alquiler)


            return "\n".join(alquileres)  # Cada alquiler en una nueva línea

        except FileNotFoundError:
            return "Error: No se encontró el archivo de alquileres\n"
        except Exception as e:
            return f"Error al leer los alquileres: {e}\n"

    def verificarLogin(self, dato1_cliente, dato2_cliente):
        try:
            with open('datos.txt', 'rb') as file:
                encrypted_lines = file.readlines()
                for encrypted_line in encrypted_lines:
                    decrypted_message = self.cipher.decrypt(encrypted_line.strip()).decode('utf-8')
                    stored_parts = decrypted_message.split(",")
                    if (dato1_cliente == stored_parts[1] and
                            (dato2_cliente == stored_parts[2] or dato2_cliente == stored_parts[3] or dato2_cliente == stored_parts[4])):
                        return True
            return False
        except FileNotFoundError:
            return False

    def is_message_in_encrypted_file2(self, dato1_cliente, segundo_dato_cliente):
        try:
            with open('datos.txt', 'rb') as file:
                encrypted_lines = file.readlines()
                for encrypted_line in encrypted_lines:
                    decrypted_message = self.cipher.decrypt(encrypted_line.strip()).decode('utf-8')
                    stored_parts = decrypted_message.split(",")
                    if (segundo_dato_cliente == stored_parts[2] or dato1_cliente == stored_parts[3]):
                        return True
            return False
        except FileNotFoundError:
            return False

    def close_server(self):
        for client in self.clients:
            client.close()
        self.server_socket.close()
        self.arduino.close()

    def handle_http_request(self, request, client_socket):
        try:
            print("solicitud")
            # Analiza la solicitud HTTP
            headers = request.splitlines()
            request_line = headers[0]
            method, path, _ = request_line.split()
            # Ejecuta la función de actualización de la contraseña siempre que se reciba una solicitud
            self.update_password()
            
            # Envía una respuesta de confirmación al cliente
            response = "Confirmada\n"
            print(response)
            client_socket.send(response.encode('utf-8'))

        except Exception as e:
            # Si ocurre algún error, envía una respuesta de error
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
                if self.correo == stored_parts[2]:  # Correoo en la posición correspondiente
                    # Actualiza la contraseña
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
