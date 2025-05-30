import socket

def start_client():
    # Configuração do servidor
    host = '127.0.0.133'  # Endereço do servidor
    port = 64535        # Porta do servidor

    # Criar um socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Conectar ao servidor
        client_socket.connect((host, port))
        print(f"Conectado ao servidor {host}:{port}")

        while True:
            # Obter mensagem do usuário
            message = input("Digite uma mensagem (ou 'sair' para encerrar): ")

            if message.lower() == 'sair':
                break

            # Enviar mensagem ao servidor
            client_socket.sendall(message.encode('utf-8'))

            # Receber resposta do servidor
            data = client_socket.recv(1024)
            print(f"Resposta do servidor: {data.decode('utf-8')}")

        print("Conexão encerrada")

if __name__ == "__main__":

 start_client()
