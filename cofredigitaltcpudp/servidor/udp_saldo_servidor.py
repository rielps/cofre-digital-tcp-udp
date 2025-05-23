# cofredigitaltcpudp/servidor/udp_saldo_servidor.py
import socket
from cofredigitaltcpudp.Utils.dados import USUARIOS

def servidor_udp_saldo():
    HOST = "127.0.0.1"
    PORT = 9998

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[UDP SALDO] Escutando em {HOST}:{PORT}")

    while True:
        data, addr = sock.recvfrom(1024)
        mensagem = data.decode()
        partes = mensagem.strip().split(";")

        if len(partes) != 2:
            resposta = "erro;Formato inválido. Use usuario;senha"
        else:
            usuario, senha = partes
            if usuario in USUARIOS and USUARIOS[usuario]["senha"] == senha:
                saldo = USUARIOS[usuario]["saldo"]
                resposta = f"saldo;{usuario};{saldo}"
            else:
                resposta = "erro;Credenciais inválidas"

        sock.sendto(resposta.encode(), addr)
