import socket

# Esta funcion se conecta con el servidor en el puerto 5000 para poder enviar mensajes.
def conectar_al_servidor():
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect(('localhost', 5000))
        
        while True:
            mensaje = input("Escribi tu mensaje (o 'exito' para salir): ")

            if mensaje.lower() == 'exito':
                print("Cerrando conexión...")
                break

            cliente_socket.sendall(mensaje.encode('utf-8'))

            respuesta = cliente_socket.recv(1024).decode('utf-8')
            print(respuesta)

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cliente_socket.close()

if __name__ == "__main__":
    conectar_al_servidor()
