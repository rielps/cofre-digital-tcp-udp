import socket
from cofredigitaltcpudp.Utils.dados import carregar_usuarios

def servidor_udp_saldo():
    HOST = "127.0.0.1"
    PORT = 9992

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[UDP SALDO] Escutando em {HOST}:{PORT}")

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            mensagem = data.decode()
            partes = mensagem.strip().split(";")

            if len(partes) != 2:
                resposta = "erro;Formato inválido. Use usuario;senha"
            else:
                usuario, senha = partes
                usuarios = carregar_usuarios()  # <-- carrega dados atualizados

                if usuario in usuarios and usuarios[usuario]["senha"] == senha:
                    saldo = usuarios[usuario]["saldo"]
                    resposta = f"saldo;{usuario};{saldo}"
                else:
                    resposta = "erro;Credenciais inválidas"

            sock.sendto(resposta.encode(), addr)
    except KeyboardInterrupt:
        print("\n[UDP SALDO] Servidor finalizado pelo usuário.")
    finally:
        sock.close()

if __name__ == "__main__":
    servidor_udp_saldo()
