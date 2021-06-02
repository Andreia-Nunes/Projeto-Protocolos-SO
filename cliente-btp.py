#!/usr/bin/env python3
import socket
import sys

TAM_MSG = 1024      # Tamanho do bloco de mensagem
HOST = '127.0.0.1'  # IP do Servidor
PORT = 40000        # Porta que o Servidor escuta

def decodeCmdUsr(cmdUsr):
    cmdMap = {
        'cat': 'read',      # Mostrar o que está escrito no Arquivo
        'cd': 'cwd',        # Mudar de Diretório, nível acima ou abaixo
        'down': 'get',       # Baixar um Diretório ou Arquivo
        'exit': 'quit',      # Encerrar o Cliente
        'ls': 'list',       # Listar o que esta dentro do Diretório atual
        'mkdir': 'makedir', # Criar um Diretório no local atual
        'pwd': 'path',      # Mostra o caminho do Diretório atual
        'touch': 'add',     # Criar um Arquivo dentro do local atual
    }

    tokens = cmdUsr.split()
    if tokens[0].lower() in cmdMap: 
        tokens[0] = cmdMap[tokens[0].lower()]
        return " ".join(tokens)
    else:
        return False

if len(sys.argv) > 1:
    HOST = sys.argv[1]
print('Servidor:', HOST+':'+str(PORT))
serv = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(serv)
print('Para encerrar use EXIT, CTRL+D ou CTRL+C')

while True:
    try:
        cmdUsr = input('\nComando >> ')
    except:
        cmdUsr = 'EXIT'
    cmd = decodeCmdUsr(cmdUsr) 
    if not cmd: 
        print('Comando "{}" não existe.'.format(cmdUsr)) 
    else:
        sock.send(str.encode(cmd)) 
        dados = sock.recv(TAM_MSG) 
        if not dados:
            break
        msgStatus = dados.decode().split('\n')[0]
        dados = dados[len(msgStatus)+1:]
        print(msgStatus)
        cmd = cmd.split()
        cmd[0] = cmd[0].upper() 
        if cmd[0] == 'QUIT':
            break
        elif cmd[0] == 'READ':
            nomeArq = " ".join(cmd[1:])
            tamArq = int(msgStatus.split()[1])
            print('\nConteúdo do arquivo "{}":'.format(nomeArq))
            while tamArq > 0:
                dados = sock.recv(TAM_MSG)
                tamArq -= len(dados)
                dados = dados.decode()
                print(dados)
        elif cmd[0] == 'GET':
            nomeArq = " ".join(cmd[1:])
            tamArq = int(msgStatus.split()[1])
            print('Recebendo:', nomeArq)
            with open(nomeArq, 'wb') as arquivo:
               while True:
                dados = sock.recv(1024)
                arquivo.write(dados)
                tamArq -= len(dados)
                if tamArq == 0: break
        elif cmd[0] == 'LIST':
            numArq = int(msgStatus.split()[1])
            dados = dados.decode()
            while True:
                arquivos = dados.split('\n')
                residual = arquivos[-1]      
                for arq in arquivos[:-1]:
                    print(arq)
                    numArq -= 1
                if numArq == 0:
                    break
                dados = sock.recv(TAM_MSG)
                if not dados:
                    break
                dados = residual + dados.decode()
        elif cmd[0].upper() == "ADD":
            texto = None
            print('Digite "end" - sem as aspas - numa linha em branco e pressione Enter para enviar o texto.')
            print()
            print('Insira o texto abaixo:')
            while texto != "end":
                texto = input()
                sock.send(str.encode(texto))

sock.close()
