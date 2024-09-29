from cryptography.fernet import Fernet

def generar_clave_secreta():
    clave_secreta = Fernet.generate_key()
    with open('clave.key', 'wb') as file:
        file.write(clave_secreta)
    return clave_secreta

def encriptar_archivo(archivo, clave_secreta):
    cipher_suite = Fernet(clave_secreta)
    with open(archivo, 'rb') as file:
        contenido = file.read()
    contenido_encriptado = cipher_suite.encrypt(contenido)
    with open(archivo, 'wb') as file:
        file.write(contenido_encriptado)

def desencriptar_archivo(archivo, clave_secreta):
    cipher_suite = Fernet(clave_secreta)
    with open(archivo, 'rb') as file:
        contenido_encriptado = file.read()
    contenido_desencriptado = cipher_suite.decrypt(contenido_encriptado)
    with open(archivo, 'wb') as file:
        file.write(contenido_desencriptado)

# Generar la clave secreta una sola vez
#clave_secreta = generar_clave_secreta()

# Encriptar el archivo
#encriptar_archivo('intento.txt', clave_secreta)

#Desencriptar el archivo
desencriptar_archivo('intento.txt', "UVSIGK3moLuqpbhLBt4C9qKm1QvHIHPCnnK_imzD0zo=")