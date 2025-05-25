import socket
import json

HOST = "127.0.0.1"
PORT = 12345

def enviar_comando(sock, comando_dict):
    msg = json.dumps(comando_dict)
    sock.send(msg.encode())
    resposta = sock.recv(1024).decode()
    print(">>", resposta)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    # Espera a mensagem inicial do servidor
    print(sock.recv(1024).decode())

    while True:
        acao = input("Digite 'login' ou 'cadastrar': ").strip().lower()
        if acao in ("login", "cadastrar"):
            break
        else:
            print("Comando inválido.")

    usuario = input("Usuario: ")
    senha = input("Senha: ")
    enviar_comando(sock, {"comando": acao, "usuario": usuario, "senha": senha})

    while True:
        cmd = input("Comando (abrir_cofre / transferir / sair): ").strip()
        if cmd == "sair":
            break
        elif cmd == "abrir_cofre":
            enviar_comando(sock, {"comando": "abrir_cofre"})
        elif cmd == "transferir":
            destino = input("Destino: ")
            valor = int(input("Valor: "))
            enviar_comando(sock, {"comando": "transferir", "destino": destino, "valor": valor})
        else:
            print("Comando desconhecido.")

    sock.close()

if __name__ == "__main__":
    main()
