from processadorCliente import ProcessadorCliente
import socket


HOST = '0.0.0.0'     #IP do servidor
PORT = 40000         #Porta do servidor

serv = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(serv)
sock.listen(50)

while True:
    try:
        con, cliente = sock.accept()
    except: break

    processador = ProcessadorCliente(con, cliente)
    processador.start()

sock.close()