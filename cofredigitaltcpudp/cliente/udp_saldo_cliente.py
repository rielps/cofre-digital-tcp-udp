# cofredigitaltcpudp/cliente/udp_saldo_cliente.py
import socket

HOST = "127.0.0.1"
PORT = 9998

usuario = input("Usuario: ")
senha = input("Senha: ")

mensagem = f"{usuario};{senha}"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(3)

try:
    sock.sendto(mensagem.encode(), (HOST, PORT))
    data, _ = sock.recvfrom(1024)
    print("Resposta do servidor UDP:", data.decode())
except socket.timeout:
    print("Servidor UDP não respondeu.")
finally:
    sock.close()
