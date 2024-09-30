from cryptography.fernet import Fernet

key =  "e72FtEbHr0prsNSSaXeG0S-tQ4Etocijj4BPX7XNFaY="# Cargar clave existente
cipher = Fernet(key)
def is_message_in_encrypted_file(message):
    try:
        with open('datos.txt', 'rb') as file:
            encrypted_lines = file.readlines()
            for encrypted_line in encrypted_lines:
                try:
                    decrypted_message = cipher.decrypt(encrypted_line.strip()).decode('utf-8')
                    if decrypted_message == message:
                        return True
                except Exception as e:
                    print(f"Error al desencriptar una línea: {e}")
        return False
    except FileNotFoundError:
        return False  # Si el archivo no existe, el mensaje no está
print(is_message_in_encrypted_file("1111,2225"))