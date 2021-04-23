import socket
import random
import hashlib
import logging
import time
import datetime
import tqdm
import threading

size = 2**10
msgFromClientLastc = 'Thanks, UDP Server. I finished. HASH CORRECT'
msgFromClientLastic = 'Thanks, UDP Server. I finished. HASH INCORRECT'

bytesToSendLastMsgc = str.encode(msgFromClientLastc)
bytesToSendLastMsgic = str.encode(msgFromClientLastic)

msgFromClient = 'Hello UDP Server, I am ready'

bytesToSendFirstMsg = str.encode(msgFromClient)


def main():

    filesize = 104865944
    host = '54.172.254.195'
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
    sock.settimeout(1)
    print("Llegue")

    puertoUDP = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Connect to server on local computer
    s.sendto(bytesToSendFirstMsg, (host, puertoUDP))\

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

    sock.send(str(1).encode('utf8'))

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
            data, address = s.recvfrom(size)
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
                print("Termino el envío con exito")
                logging.info("Termino el envio con exito")
                fin = time.time()
                break
            elif (data.__contains__(b"Hash:")):

                j = dataTotal.find(b"Hash:")
                hs.update(dataTotal[:j])
                prueba = hs.hexdigest()

                i = data.find(b"Hash:")
                recibido = data[i+5:]
                recibidoD = recibido.decode()
                logging.info("Se recibe el hash junto con el archivo ")
                print("Se recibe el siguiente hash ", recibidoD)
                print("Se crea el siguiente hash de prueba ", prueba)

                if hs.hexdigest() == recibido.decode():
                    print("El hash fue verificado. Es correcto :)")
                    logging.info("Hash verificado. Archivo correcto")
                    s.sendto(bytesToSendLastMsgc, (host, puertoUDP))

                else:
                    print(
                        "El hash no pudo ser verificado. Hay un problema con el archivo recibido :(")
                    logging.info("Hash erroneo. Archivo incorrecto")
                    s.sendto(bytesToSendLastMsgic, (host, puertoUDP))

    logging.info('Bytes recibidos: %s , paquetes recibidos: %s , tiempo utilizado: %s, tasa de transferencia: %s', len(
        dataTotal), len(dataTotal)/1048576, (fin-inicio), (len(dataTotal)/(fin-inicio)))

    s.close()
    sock.close()


class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        main2()
        print("Exiting " + self.name)


# Create new threads
thread0 = myThread(0, "Thread-0", 0)
#thread1 = myThread(1, "Thread-1", 1)
#thread2 = myThread(2, "Thread-2", 2)
#thread3 = myThread(3, "Thread-3", 3)
#thread4 = myThread(4, "Thread-4", 4)
#thread5 = myThread(5, "Thread-5", 5)
#thread6 = myThread(6, "Thread-6", 6)
#thread7 = myThread(7, "Thread-7", 7)
#thread8 = myThread(8, "Thread-8", 8)
#thread9 = myThread(9, "Thread-9", 9)


# Start new Threads
thread0.start()
# thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()
# thread5.start()
# thread6.start()
# thread7.start()
# thread8.start()
# thread9.start()
