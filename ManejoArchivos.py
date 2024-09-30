def LeerArchivo():
    ruta="Intento.txt"
    archivo=open(ruta) # coloca el contenido en memoria
    contenido=archivo.readlines()
    archivo.close()
    return contenido # retorna el contenido del archivo
######################################################
def EscribirArchivo(dato):
    ruta="Prueba.txt"
    archivo=open(ruta,"a")#a->append
    archivo.write(dato+"\n") # escribe el dato en el archivo
    archivo.close()
########################################################
def IngresarUsuario():
    nombre="Jacinto"
    apellido="Basurilla"
    edad=56
    registro=nombre+","+apellido+","+str(edad)
    EscribirArchivo(registro)
    nombre="Pepe"
    apellido="Botellas"
    edad=18
    registro=nombre+","+apellido+","+str(edad)
    EscribirArchivo(registro)
########################################################
def VerificaLogin(nombre):
    if isinstance(nombre,str):
            return VerificaUsuario(LeerArchivo(),nombre)

#Verifica si un usuario está en el archivo
def VerificaUsuario(listaUsuarios,usuario):
    if listaUsuarios==[]:
        return False
    elif listaUsuarios[0].split(",")[0]==usuario: #["jason","leiton","16\n"]
        return True
    else:
        return VerificaUsuario(listaUsuarios[1:],usuario)
        
    










    
