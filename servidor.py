import socket
import sqlite3
from datetime import datetime

# Esta funcion inicializa el socket escuchando en el puerto 5000.
def inicializar_socket():
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Seteamos el puerto y la IP
    servidor_socket.bind(('localhost', 5000))
    servidor_socket.listen(5)
    print("Servidor escuchando en localhost:5000...")
    return servidor_socket

# Esta funcion acepta conexiones del cliente y recibe los mensajes
def aceptar_conexiones(servidor_socket):
    while True:
        cliente_socket, direccion_cliente = servidor_socket.accept()
        print(f"Conexión establecida con {direccion_cliente}")

        try:
            while True:
                mensaje = cliente_socket.recv(1024).decode('utf-8')
                if not mensaje:
                    break

                print(f"Mensaje recibido de {direccion_cliente}: {mensaje}")
                guardar_mensaje_en_db(mensaje, direccion_cliente[0])

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                respuesta = f"Mensaje recibido: {timestamp}"
                cliente_socket.sendall(respuesta.encode('utf-8'))

        except Exception as e:
            print(f"Error al comunicarse con {direccion_cliente}: {e}")
        finally:
            cliente_socket.close()
            print(f"Conexión cerrada con {direccion_cliente}")

# Esta funcion guarda el mensaje recibido en la BD
def guardar_mensaje_en_db(contenido, ip_cliente):
    try:
        conexion = sqlite3.connect('database.db')
        cursor = conexion.cursor()

        # Creamos la tabla si esta no existe.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')

        # Guardamos el mensaje en la base de datos.
        fecha_envio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        ''', (contenido, fecha_envio, ip_cliente))

        conexion.commit()

    except sqlite3.Error as e:
        print(f"Error al trabajar con la base de datos: {e}")

    finally:
        if conexion:
            conexion.close()


if __name__ == "__main__":
    servidor = inicializar_socket()
    aceptar_conexiones(servidor)
