import socket
import threading
import _thread
import logging
import hashlib
import datetime
import time
import os


ready = False
archivo = None
lock = threading.Lock()
oks = []


def threaded(socketC, idCli):
    global oks
    global ready
    global lock
    m = hashlib.sha256()
    logging.info('Cliente #%i iniciado', idCli)

    # ok = int(socketC.recv(1024).decode('utf8'))
    logging.info('El cliente #%i está listo para recibir', idCli)
    # lock.acquire()
    # oks[idCli] = 1
    # esperar = False
    # for i in oks:
    #     if i == 0:
    #         esperar = True
    #         break
    # ready = not esperar
    # lock.release()
    #
    # while esperar:
    #     esperar = not ready

    with open(archivo, 'rb') as enviar:
        data = enviar.read()
        m.update(data)
        tiempoIni = time.time()
        numBytes = socketC.send(data)
        logging.info(
            'Archivo enviado al cliente #%i, bytes enviados: %i', idCli, numBytes)
        print('Archivo enviado al cliente ' + str(idCli))

        hashM = m.hexdigest()
        numBytes += socketC.send(('Hash:' + hashM).encode())
        tiempoFin = time.time()
        logging.info(
            'Hash enviado al cliente #%i, bytes enviados en total: %i', idCli, numBytes)
        print('Hash enviado al cliente ' + str(idCli))

        logging.info('Tiempo del envío al cliente #%i: %i',
                     idCli, (tiempoFin-tiempoIni))

    socketC.close()


def main():
    global archivo
    global oks
    print('Bienvenido')
    fecha = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
    nombreLog: str = './archivosS/log_' + fecha + '.log'
    logging.basicConfig(filename=nombreLog, level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(levelname)-8s %(message)s')

    host = '0.0.0.0'
    puerto = 55555
    logging.info('Conectado a %s en el puerto %s', host, puerto)

    socketS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketS.bind((host, puerto))
    print('Puerto: ', puerto)

    socketS.listen(5)
    print('Escuchando...')
    elegirArchivo = int(
        input('¿Qué archivo desea enviar? 1. 100 MB \t 2. 250 MB \n'))
    if elegirArchivo == 1:
        archivo = './data/100MB.zip'
        logging.info('Archivo a enviar: 100MB.zip con tamaño de 100 MB')
    else:
        archivo = './data/250MB.zip'
        logging.info('Archivo a enviar: 250MB.zip con tamaño de 250 MB')
    print('Se ha seleccionado el archivo ', archivo)

    filesize = os.path.getsize(archivo)

    numClientes = int(input(
        '¿A cuántos clientes desea enviar el archivo? Ingrese el número únicamente\n'))
    logging.info('Número de clientes: %i', numClientes)
    print('Se enviará el archivo a ' + str(numClientes) + ' clientes')
    for i in range(numClientes):
        oks.append(0)

    threads = []
    recibir = True
    while recibir:
        (socketC, direccion) = socketS.accept()
        socketC.send((str(len(threads)) + '–Prueba-' +
                      str(numClientes) + '.zip|' + str(filesize)).encode('utf8'))
        print('Se ha conectado el cliente ' + str(len(threads)) +
              '(' + str(direccion[0]) + ':' + str(direccion[1]) + ')')
        logging.info('Conexión con éxitosa con %s:%s. Asignado id: %i',
                     direccion[0], direccion[1], len(threads))
        threadAct = threading.Thread(
            target=threaded, args=(socketC, len(threads)))
        threads.append(threadAct)
        if len(threads) == numClientes:
            recibir = False
            for i in threads:
                i.start()
            threads = []

    socketS.close()


main()
