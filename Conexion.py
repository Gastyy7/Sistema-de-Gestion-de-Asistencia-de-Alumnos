import mysql.connector

class CConexion:

    def ConexionBaseDeDatos():
        try:
            conexion = mysql.connector.connect(user="root",password="root",
                                               host="127.0.0.1",
                                               database="gestioncursos",
                                               port="3306")
            print("Conexion Correcta a la BBDD")

            return conexion
        
        except mysql.connector.Error as error:
            print("Error al conectar a la base de datos {}".format(error))

            return conexion
    ConexionBaseDeDatos()