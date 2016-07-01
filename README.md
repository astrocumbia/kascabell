# kascabell

Kascabell es un pequeño módulo implementado en python para controlar la reproducción de música

## Módulos
* Config.py
	Dentro de este pequeño módulo leemos las configuraciones almacenadas en config.json
* scanner
	Esté módulo fue creado para encontrar al servidor de control principal
* start.sh
	Script para iniciar una instancia de VCL que pueda ser controlada por telnet
* VLC.py
	Módulo para controlar la instancia de vlc

## Configuración
### Comunicador 
Antes de ejecutar Kascabell debemos ejecutar una instancia del comunicador /comunicador/comunicador.py

### JSON
Configuramos el archivo config.json, especificando contraseñas, redes a escanear, etc

### Archivos
Todos los archivos de audio e imagenes se almacenan dentro de la carpeta Store

## Install
Antes de ejecutar la instancia de Kascabell necesitamos instalar las dependencias haciendo pip install install.txt

## Run
Ya configurado y con las dependencias instaladas hacemos ./main.py



