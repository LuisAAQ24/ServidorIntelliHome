from cryptography.fernet import Fernet
def desencriptar_archivo_por_lineas(archivo, clave):
    # Convertir la clave de string a bytes
    clave_bytes = clave.encode('utf-8')
    cipher_suite = Fernet(clave_bytes)

    with open(archivo, 'rb') as file:
        for linea in file:
            try:
                contenido_desencriptado = cipher_suite.decrypt(linea.strip())
                print(contenido_desencriptado.decode('utf-8'))
            except Exception as e:
                print(f"Error al desencriptar la línea: {e}")
desencriptar_archivo_por_lineas("propiedades.txt","pQXGLozTYThpxI6mbfbadXo3gTx4wYO9_E0vqGUMTpg=")