from cryptography.fernet import Fernet

def desencriptar_archivo(archivo, clave):

    cipher_suite = Fernet(clave)
    
    # Leer el contenido encriptado del archivo
    with open(archivo, 'rb') as file:
        contenido_encriptado = file.read()
    
    # Desencriptar el contenido del archivo
    contenido_desencriptado = cipher_suite.decrypt(contenido_encriptado)
    
    # Devolver el contenido desencriptado

    return contenido_desencriptado.decode('utf-8')

# Ejemplo de uso
contenido_desencriptado = desencriptar_archivo('intento.txt', 'oYNJjntI5kThiiL7DHgCxJcXppI5dT2v3tafJozxTBI=')
print(contenido_desencriptado[0])