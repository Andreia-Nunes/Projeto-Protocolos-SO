from threading import Thread
import btpAlterado


class ProcessadorCliente(Thread):

    def __init__(self, con, cliente):
        super().__init__()
        self.con = con
        self.cliente = cliente

    def run(self):
        print(f"Cliente conectado: {self.cliente}")

        while True:
            msg = self.con.recv(1024)
            if not msg or not btpAlterado.processamento(msg, self.con, self.cliente): break

        self.con.close()
        print(f"Cliente desconectado: {self.cliente}")