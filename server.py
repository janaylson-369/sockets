# server.py
import socket

def start_server():
    # Configuração do servidor
    host = '127.0.0.133'   # Localhost
    port = 64535         # Porta para escutar

    # Criar um socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Vincular o socket ao endereço e porta
        server_socket.bind((host, port))

        # Escutar por conexões entrantes
        server_socket.listen(1)
        print(f"Servidor iniciado. Aguardando conexões em {host} {port}...")

        # Aceitar uma conexão
        conn, addr = server_socket.accept()
        with conn:
            print(f"Conexão estabelecida com {addr}")

            while True:
                # Receber dados do cliente
                data = conn.recv(1024)
                if not data:
                    break

                # Decodificar e exibir a mensagem
                message = data.decode('utf-8')
                print(f"Mensagem recebida do cliente: {message}")

                # Preparar e enviar resposta
                response = f"Servidor recebeu: {message}"
                conn.sendall(response.encode('utf-8'))

            print("Conexão encerrada")

if __name__ == "__main__":
   start_server()
