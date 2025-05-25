import json
import os

ARQUIVO_USUARIOS = "cofredigitaltcpudp/Utils/usuarios.json"

# Carrega os usuários a partir de um arquivo JSON
def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r") as f:
            return json.load(f)
    return {}

# Salva os usuários no arquivo JSON
def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4)

# Inicializa a variável global
USUARIOS = carregar_usuarios()