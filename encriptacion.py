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

encriptar_archivo("intento.txt",generar_clave_secreta())