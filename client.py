

import socket
import threading

def receber_mensagens(conn):
    while True:
        try:
            mensagem = conn.recv(1024).decode()
            if mensagem:
                print(f"\n[Recebido] {mensagem}")
        except:
            break

def iniciar_peer(meu_ip, minha_porta, ip_remoto, porta_remota):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((meu_ip, minha_porta))
    servidor.listen(1)
    print(f"Esperando conexão em {meu_ip}:{minha_porta}...")

    def aceitar_conexao():
        conn, addr = servidor.accept()
        print(f"Conectado por {addr}!")
        threading.Thread(target=receber_mensagens, args=(conn,), daemon=True).start()
        return conn
    
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((ip_remoto, porta_remota))
        print(f"Conectado ao peer {ip_remoto}:{porta_remota}")
    except Exception as e:
        print(f"[Erro ao conectar: {e}]")
        cliente = None

    conexao_recebida = aceitar_conexao()

    while True:
        msg = input("Você: ")
        if cliente:
            try:
                cliente.send(msg.encode())
            except:
                print("[Erro ao enviar para peer remoto.]")
        
        try:
            conexao_recebida.send(msg.encode())
        except:
            print("[Erro ao enviar para conexão recebida.]")


if __name__ == "__main__":
    iniciar_peer("localhost", 5000, "localhost", 5001)




#the end

import socket

def start_client():
    # Configuração do servidor
    host = '127.0.0.1'  # Endereço do servidor
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
