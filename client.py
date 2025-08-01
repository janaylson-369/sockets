

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


#codigo alterado

import socket
import threading

def receber_mensagens(conn):
    """Lida com o recebimento contínuo de mensagens da conexão."""
    try:
        while True:
            mensagem = conn.recv(1024).decode()
            if not mensagem:
                print("\n[INFO] O outro peer encerrou a conexão.")
                break
            print(f"\n[Recebido] {mensagem}")
    except (socket.error, ConnectionResetError):
        print("\n[ERRO] Conexão perdida.")
    finally:
        conn.close()

def enviar_mensagens(conn):
    """Lida com o envio contínuo de mensagens."""
    while True:
        try:
            msg = input("Você: ")
            conn.send(msg.encode())
        except (socket.error, BrokenPipeError):
            print("[ERRO] Conexão perdida. Encerrando o chat.")
            break
    
def iniciar_peer(meu_ip, minha_porta, ip_remoto, porta_remota, eh_servidor):
    """Inicia o peer como servidor ou cliente."""
    
    if eh_servidor:
        # Modo Servidor: Espera por uma conexão
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((meu_ip, minha_porta))
        sock.listen(1)
        print(f"Peer 1 (Servidor) esperando conexão em {meu_ip}:{minha_porta}...")
        conn, addr = sock.accept()
        print(f"Peer 1 conectado por {addr}!")
    else:
        # Modo Cliente: Inicia a conexão
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Peer 2 (Cliente) tentando conectar a {ip_remoto}:{porta_remota}...")
        try:
            sock.connect((ip_remoto, porta_remota))
            print("Peer 2 conectado com sucesso!")
            conn = sock
        except ConnectionRefusedError:
            print(f"[ERRO] Não foi possível conectar ao peer em {ip_remoto}:{porta_remota}.")
            return
            
    # Uma vez conectado, ambas as partes podem enviar e receber
    
    thread_receber = threading.Thread(target=receber_mensagens, args=(conn,), daemon=True)
    thread_receber.start()
    
    enviar_mensagens(conn)
    
    conn.close()
    if eh_servidor:
        sock.close()


if __name__ == "__main__":
    MEU_IP = "10.10.132.208"
    MINHA_PORTA = 5000
    IP_REMOTO = "10.10.132.10"
    PORTA_REMOTA = 5001

    escolha = input("Você quer ser o 'servidor' (esperar conexão) ou o 'cliente' (iniciar conexão)? (s/c): ").lower()

    if escolha == 's':
        iniciar_peer(MEU_IP, MINHA_PORTA, IP_REMOTO, PORTA_REMOTA, eh_servidor=True)
    elif escolha == 'c':
        iniciar_peer(MEU_IP, MINHA_PORTA, IP_REMOTO, PORTA_REMOTA, eh_servidor=False)
    else:
        print("Escolha inválida. Por favor, reinicie e escolha 's' ou 'c'.")




#------------------------------------------------------------------#####

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
