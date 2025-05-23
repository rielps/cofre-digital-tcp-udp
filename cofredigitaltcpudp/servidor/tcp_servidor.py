# cofredigitaltcpudp/servidor/tcp_servidor.py
import socket
import threading
import json
import time
from cofredigitaltcpudp.servidor.udp_saldo_servidor import servidor_udp_saldo
from cofredigitaltcpudp.Utils.dados import USUARIOS

CLIENTES_AUTENTICADOS = {}

UDP_IP = "127.0.0.1"
UDP_PORT = 9999

def enviar_udp(mensagem):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(mensagem.encode(), (UDP_IP, UDP_PORT))

def tratar_cliente(conn, addr):
    usuario = None
    conn.send(b"Bem-vindo! Realize seu login com seu usuario e senha.\n")

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            msg = json.loads(data.decode())

            if usuario is None:
                if msg["comando"] == "login":
                    u = msg["usuario"]
                    s = msg["senha"]
                    if u in USUARIOS and USUARIOS[u]["senha"] == s:
                        usuario = u
                        CLIENTES_AUTENTICADOS[conn] = u
                        conn.send(b"Login bem-sucedido!\n")
                    else:
                        conn.send(b"Credenciais invalidas.\n")
                else:
                    conn.send(b"Autentique-se primeiro.\n")
            else:
                if msg["comando"] == "abrir_cofre":
                    resposta = f"{usuario} abriu o cofre em {time.ctime()}"
                    conn.send(resposta.encode())
                    enviar_udp(f"NOTIFICACAO: {resposta}")
                elif msg["comando"] == "transferir":
                    destino = msg["destino"]
                    valor = msg["valor"]
                    if destino not in USUARIOS:
                        conn.send(b"Usuario destino nao existe.\n")
                    elif USUARIOS[usuario]["saldo"] < valor:
                        conn.send(b"Saldo insuficiente.\n")
                    else:
                        USUARIOS[usuario]["saldo"] -= valor
                        USUARIOS[destino]["saldo"] += valor
                        conn.send(b"Transferencia realizada.\n")
                        enviar_udp(f"NOTIFICACAO: {usuario} transferiu {valor} para {destino} em {time.ctime()}")
                else:
                    conn.send(b"Comando invalido.\n")
        except Exception as e:
            print(f"Erro com {addr}: {e}")
            break

    conn.close()
    print(f"Conexao encerrada: {addr}")

def main():
    host = "0.0.0.0"
    port = 12345
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Servidor TCP escutando em {host}:{port}")

    # Inicia o servidor UDP de saldo em uma thread daemon
    t_udp = threading.Thread(target=servidor_udp_saldo, daemon=True)
    t_udp.start()

    while True:
        conn, addr = server.accept()
        threading.Thread(target=tratar_cliente, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
