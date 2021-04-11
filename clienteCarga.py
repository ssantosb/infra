import socket
import random
import hashlib
import logging
import time
import datetime
import tqdm
import threading


def main():

    filesize = 104865944
    host = '34.205.154.39'
    puerto = 55555
    print('Hola, Cliente')
    fecha = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
    logging.basicConfig(filename="./archivosC/Log" + fecha + ".log", level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    print('Se terminó de configurar el log de su pronta conexión')
    hs = hashlib.sha256()
    print(hs)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, puerto))
    print("Se conecto satisfactoriamente con el host ",
          host, " en el puerto: ", puerto)
    print("Cliente comenzará a recibir información")
    logging.info("Cliente comenzará a recibir información")

    data = sock.recv(1024)
    strings = data.decode('utf8').split('|')
    filename = strings[0]
    strings2 = filename.split('-')[0].split("-")
    idcliente = strings2[0]
    idcliente = idcliente[0]
    filesize = int(strings[1])
    print("Cliente ", idcliente, " recibirá archivo ",
          str(filename), " con peso ", str(filesize))
    logging.info("Cliente " + idcliente + " recibirá archivo " +
                 str(filename) + " con peso " + str(filesize))

    #input("Presione enter para enviar la confirmación de que se encuentra listo para recibir el archivo")

    # sock.send(str(1).encode('utf8'))

    print("Cliente ", str(idcliente),
          " envia confirmación de estado preparado para recibir archivo")
    logging.info("Cliente " + str(idcliente) +
                 " envia confirmación de estado preparado para recibir archivo")
    dataTotal = b''
    inicio = time.time()
    cond = True
    filename = str('./archivosC/archivosRecibidos/' + filename)

    progress = tqdm.tqdm(range(
        filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

    with open(filename, "wb") as f:
        while True:
            data = sock.recv(1048576)
            dataTotal += data

            f.write(data)
            progress.update(len(data))
            if data and cond:
                cond = False
                print("Cliente ", str(idcliente),
                      " recibe el primer paquete del archivo")
                logging.info("Cliente " + str(idcliente) +
                             " recibe el primer paquete del archivo")
                inicio = time.time()
            if not data:
                print("Cliente ", str(idcliente),
                      " Termino el envío con exito")
                logging.info("Cliente " + str(idcliente) +
                             " Termino el envio con exito")
                fin = time.time()
                break
            elif (data.__contains__(b"Hash:")):

                j = dataTotal.find(b"Hash:")
                hs.update(dataTotal[:j])
                prueba = hs.hexdigest()

                i = data.find(b"Hash:")
                recibido = data[i+5:]
                recibidoD = recibido.decode()
                logging.info("Cliente " + str(idcliente) +
                             " Se recibe el hash junto con el archivo ")
                print("Cliente ", str(idcliente),
                      " Se recibe el siguiente hash ", recibidoD)
                print("Cliente ", str(idcliente),
                      " Se crea el siguiente hash de prueba ", prueba)

                if hs.hexdigest() == recibido.decode():
                    print("Cliente ", str(idcliente),
                          " El hash fue verificado. Es correcto :)")
                    logging.info("Cliente " + str(idcliente) +
                                 " Hash verificado. Archivo correcto")
                else:
                    print(
                        "Cliente ", str(idcliente), " El hash no pudo ser verificado. Hay un problema con el archivo recibido :(")
                    logging.info("Hash erroneo. Archivo incorrecto")

    logging.info('Cliente: %s ,Bytes recibidos: %s , paquetes recibidos: %s , tiempo utilizado: %s, tasa de transferencia: %s', idcliente, len(
        dataTotal), len(dataTotal)/1048576, (fin-inicio), (len(dataTotal)/(fin-inicio)))

    sock.close()


exitFlag = 0


class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        main()
        print("Exiting " + self.name)


# Create new threads
thread0 = myThread(0, "Thread-0", 0)
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)
thread3 = myThread(3, "Thread-3", 3)
thread4 = myThread(4, "Thread-4", 4)


# Start new Threads
thread0.start()
thread1.start()
thread2.start()
thread3.start()
thread4.start()
