import os
import threading


semaforo = threading.Semaphore(1)


def processamento(msg, con, cliente):
    msg = msg.decode()
    print(f"Cliente {cliente} enviou {msg}")
    msg = msg.split()

    if msg[0].upper() == 'GET':
        nome_arquivo = " ".join(msg[1:])
        print(f"Arquivo solicitado: {nome_arquivo}")

        try:
            #Envio do tamanho do arquivo
            status_arquivo = os.stat(nome_arquivo)
            con.send(str.encode(f"+OK {status_arquivo.st_size}\n"))

            #Envio do arquivo
            arquivo = open(nome_arquivo, "rb")
            while True:
                dados = arquivo.read(1024)
                if not dados: break
                con.send(dados)
        except Exception as e:
            con.send(str.encode(f"-ERR {e}\n"))
    elif msg[0].upper() == 'LIST':
        #Envio do tamanho da lista de arquivos
        lista_arquivos = os.listdir(".")
        con.send(str.encode(f"+OK {len(lista_arquivos)}\n"))

        #Envio da lista de arquivos
        for nome_arquivo in lista_arquivos:
            if os.path.isfile(nome_arquivo):
                status_arquivo = os.stat(nome_arquivo)
                con.send(str.encode(f"arq: {nome_arquivo} - {status_arquivo.st_size/1024}KB\n"))
            elif os.path.isdir(nome_arquivo):
                con.send(str.encode(f"dir: {nome_arquivo}\n"))
            else:
                con.send(str.encode(f"esp: {nome_arquivo}\n"))
    elif msg[0].upper() == 'CWD':
        try:
            os.chdir(msg[1])
            con.send(str.encode(f"+OK\n"))
        except:
            con.send(str.encode(f"-ERR Diretório não existe\n"))
    elif msg[0].upper() == 'READ':
        nome_arquivo = " ".join(msg[1:])
        print(f"Arquivo solicitado: {nome_arquivo}")

        try:
            #Envio do tamanho do arquivo
            status_arquivo = os.stat(nome_arquivo)
            con.send(str.encode(f"+OK {status_arquivo.st_size}\n"))

            #Envio do arquivo
            arquivo = open(nome_arquivo, "rb")
            while True:
                dados = arquivo.read(1024)
                if not dados: break
                con.send(dados)
        except Exception as e:
            con.send(str.encode(f"-ERR {e}\n"))
    elif msg[0].upper() == 'MAKEDIR':
        try:
            os.mkdir('./' + msg[1])
            con.send(str.encode(f"+OK\n"))
        except:
            con.send(str.encode(f"-ERR Diretório já existe\n"))
    elif msg[0].upper() == 'PATH':
        try:
            caminho = os.getcwd()
            con.send(str.encode(f"+OK {caminho}\n"))
        except Exception as e:
            con.send(str.encode(f"-ERR {e}\n"))
    elif msg[0].upper() == 'ADD':
        semaforo.acquire()
        nome_arquivo = " ".join(msg[1:])
        con.send(str.encode(f"+OK\n"))
        with open(nome_arquivo, 'ab') as arquivo:
            while True:
                dados = con.recv(1024)
                if dados.decode() == "end": break
                arquivo.write(dados)
                arquivo.write(str.encode("\n"))
        semaforo.release()
    elif msg[0].upper() == 'QUIT':
        con.send(str.encode(f"+OK\n"))
        return False
    else:
        con.send(str.encode(f"-ERR Invalid command\n"))

    return True









