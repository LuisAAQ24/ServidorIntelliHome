import socket

def simple_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('172.18.155.12', 7070))  # Cambia esto según tu configuración
    client_socket.send("Hola, servidor".encode('utf-8'))
    
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Respuesta del servidor: {response}")
    
    client_socket.close()

if __name__ == "__main__":
    simple_client()
