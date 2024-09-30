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

print(desencriptar_archivo('datos.txt', 'ygvUS3jxoJxxRuuf9hnHYO1S8FDJ5wRbT_IiWHS87Cg='))
