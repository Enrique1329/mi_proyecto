import mysql.connector
from datetime import datetime

class Usuario:
    def __init__(self, nombre_usuario, contrasena):
        self.__nombre_usuario = nombre_usuario
        self.__contrasena = contrasena

    def validar_acceso(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Si tienes contraseña, ponla aquí
                database="usuarios_bd2"
            )
            cursor = conexion.cursor()
            consulta = "SELECT contrasena FROM usuarios WHERE nombre_usuario = %s"
            cursor.execute(consulta, (self.__nombre_usuario,))
            resultado = cursor.fetchone()

            if resultado:
                if resultado[0] == self.__contrasena:
                    registrar_intento(self.__nombre_usuario, self.__contrasena, "exitoso")
                    return True
                else:
                    registrar_intento(self.__nombre_usuario, self.__contrasena, "contrasena incorrecta")
                    return False
            else:
                registrar_intento(self.__nombre_usuario, self.__contrasena, "usuario no registrado")
                return False

        except mysql.connector.Error as err:
            print(f"Error al conectar con la base de datos: {err}")
            return False


def registrar_intento(usuario, contrasena, estado):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Si tienes contraseña, ponla aquí
            database="usuarios_bd2"
        )
        cursor = conexion.cursor()
        consulta = """
            INSERT INTO intentos (usuario_intento, contrasena_intento, estado, fecha_hora)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(consulta, (usuario, contrasena, estado, datetime.now()))
        conexion.commit()
        cursor.close()
        conexion.close()
    except mysql.connector.Error as err:
        print(f"Error al registrar intento: {err}")


def crear_base_y_tablas():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""  # Si tienes contraseña, ponla aquí
        )
        cursor = conexion.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS usuarios_bd2")
        cursor.close()
        conexion.close()

        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usuarios_bd2"
        )
        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_usuario VARCHAR(50) UNIQUE,
                contrasena VARCHAR(50)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS intentos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_intento VARCHAR(50),
                contrasena_intento VARCHAR(50),
                estado VARCHAR(50),
                fecha_hora DATETIME
            )
        """)

        usuarios_predeterminados = [
            ("jeremy", "1234"),
            ("andy", "1234"),
            ("enrique", "1234")
        ]

        for usuario, contrasena in usuarios_predeterminados:
            cursor.execute("""
                INSERT IGNORE INTO usuarios (nombre_usuario, contrasena)
                VALUES (%s, %s)
            """, (usuario, contrasena))

        conexion.commit()
        cursor.close()
        conexion.close()
    except mysql.connector.Error as err:
        print(f"Error al crear base de datos o tablas: {err}")


def pedir_datos_y_validar():
    nombre = input("Ingrese su nombre de usuario: ")
    clave = input("Ingrese su contraseña: ")
    usuario = Usuario(nombre, clave)

    if usuario.validar_acceso():
        print("Acceso exitoso. \u00a1Bienvenido!")
    else:
        print("Acceso denegado. Usuario o contraseña incorrectos.")


if __name__ == "__main__":
    crear_base_y_tablas()
    pedir_datos_y_validar()
