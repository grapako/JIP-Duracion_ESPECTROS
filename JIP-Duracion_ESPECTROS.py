#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 14:14:12 2018
@author: JIP
Descripción: La idea es leer atributos de los archivos en una carpeta. En particular
me interesa leer la fecha de creación y luego de modificación para calcular
cuánto tardó en converger.
"""
###############################################################################
# Módulos a importar:
import os
import numpy as np
import datetime

###############################################################################
# Código:
# con getcwd lee los bsf desde la ruta en donde se ejecuta el script
rutadearchivos = os.getcwd() #+ "\\"

''' Te devuelve la lista de archivos en el directorio de ejecución del script
de la extensión especificada y ordenados por fecha de creación. Lo uso
sólo para extraer el primero creado y luego redefino la lista'''

listadearchivos = sorted((f for f in os.listdir(rutadearchivos) \
                        if f.endswith(".bsf") \
                        and os.path.isfile(f)), key=os.path.getctime)

(mode,ino,dev,nlink,uid,gid,size,atime,modificadoel,inicialcreadoel) = \
os.stat(rutadearchivos + "\\" + listadearchivos[0]) # Archivo inicial

''' Redefino la lista de archivos en el directorio de ejecución del script
de la extensión especificada y ordenados por fecha de modificación.'''

listadearchivos = sorted((f for f in os.listdir(rutadearchivos) \
                        if f.endswith(".bsf") \
                        and os.path.isfile(f)), key=os.path.getmtime)

(mode,ino,dev,nlink,uid,gid,size,atime,finalmodificadoel,creadoel) = \
os.stat(rutadearchivos + "\\" + listadearchivos[len(listadearchivos)-1]) # Ultimo modificado

# Ahora puedo hacer la cuenta. Duración de todo el proceso, al momento de ejecutar el script.
# Duración h:mm:ss
tiempotranscurrido = str(datetime.timedelta(seconds=(finalmodificadoel-inicialcreadoel)))

resultado=[]
for f in range(0,len(listadearchivos)):
    
    archivoactual=listadearchivos[f]
    
    (mode,ino,dev,nlink,uid,gid,size,atime,modificadoel,creadoel) = \
    os.stat(rutadearchivos + "\\" + archivoactual)
    
    tamañomb = round(size/1024/1024,1)
# Duración
    duracion=str(datetime.timedelta(seconds=(modificadoel-creadoel))) # Duración h:mm:ss
        
    resultado.append([archivoactual,duracion,tamañomb])
    
###############################################################################
# Impresión en pantalla
    
    print(archivoactual, "de {} MB".format(tamañomb), "Terminó en",duracion)

lineheader1="\nCatidad de rangos espectrales calculados: {}".format(len(listadearchivos))
print(lineheader1)

lineheader2="Tiempo total transcurrido: {}".format(tiempotranscurrido)
print(lineheader2)
###############################################################################
# Escritura de archivo

#cabeceras=["\t Archivo","\t   Duración"]

y=str(input("¿Exporto?(s-n): "))
if y=="s":
    filename="JIP-Duración_espectros.dat"
    np.savetxt(filename,
               resultado,
               fmt="%-27s %8s %6s",
               delimiter="\t",
               newline="\n", # La \r es para windows
               comments="",
               footer="\n".join([lineheader1,lineheader2]))
    print("\nExportado al directorio actual")
else:
    print("\nCareta")