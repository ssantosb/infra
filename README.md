# Laboratorio 4
A continuación se presentan los requerimientos para poder ejecutar la aplicación de cliente y servidor respectivamente.
## Ejecución del servidor 
**Preparación de archivos:**
En primer lugar, se deben descargar los archivos https://transfer.sh/Mitg3/100MB.zip y https://transfer.sh/iutKe/Archivo250MB.zip en la carpeta _data_ con los
nombres 100MB.zip y 250MB.zip respectivamente, adicionalmente, se puede descargar el video https://www.youtube.com/watch?v=YBnGBb1wg98 en formato mp4 y darle
el nombre Zimzalabim.mp4. 

**Ejecución:**
Se debe correr el archivo servidor.py con python3 y seguir las instrucciones del mismo para realizar la correcta transferencia.
Nota: El servidor fue pensado para ser desplegado en la nube, por tanto, en la línea 70 se utiliza la dirección IP '0.0.0.0', si su despliegue es local debe
colocar la dirección IP fija de la máquina entre las comillas sencillas.

**Revisión del log del servidor:** Los archivos log del servidor se encuentran en la carpeta _ArchivosS_.
## Ejecución del cliente
**Ejecución:**
Se debe editar la línea 24 (host) del código ubicado en cliente.py para colocar la dirección IP del servidor, la región a editar es aquella entre comillas sencillas,
a continuación se muestra un ejemplo: host = '34.227.110.129'.
Posteriormente, se debe correr el archivo cliente.py con python3 y seguir las instrucciones del mismo para realizar la correcta transferencia.

**Revisión del log del servidor:** Los archivos log del cliente se encuentran en la carpeta _ArchivosC_.
