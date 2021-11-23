import komm
from PIL import Image
import sys
import project_functions as pf # Archivo de funciones creadas
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import random

# Se realizan las instancias de las clases que se implementaran de las librerias incluidas

''' La clase HammingCode contiene metodos que codifican y decodifican paquetes de bits por 
medio del método de Hamming '''
hamming = komm.HammingCode(3)

# La clase ASKodulation simula una modulacion por amplitud de pulsos (ASK)
ask = komm.ASKModulation(4,base_amplitude=1)

# La clase AWGNChannel modela un canal de ruido gaussiano blanco aditivo (AWGN)
GaussianNoise = komm.AWGNChannel(snr=25, signal_power=1.0)

bc = [] # Copia de la secuencia de bits transmitida
bf = [] # Secuencia de bits original
bc_r = [] # Secuencia de bits recibidos
bf_r = [] # Secuencia de bits de informacion recibidos
bf_r_aux = [] # Array auxiliar para bf
bc_r_aux = [] # Array auxiliar para bc
xT = [] # Array de señal modulada
hits = 0 # Cantidad de bits transmitidos correctamente
misses = 0 # Cantidad de bits transmitidos con error

''' En la etapa de decodificacion se guardaran en el array bkR
los paquetes de 24 bits que componen la salida del codificador '''
bkR=[] 

''' En el array vR se guardaran los pixeles decodificados
en la etapa de decodificación'''
vR=[]

# Guarda en input_img el nombre de la imagen (con extensión), que se le pasa como parametro al programa
input_img = sys.argv[1]

# Se convierte la imagen.bmp en un mapa de pixeles
img = Image.open(input_img) # Abre la imagen y la guarda en img

""" A partir de la imagen guardada en img crea una lista de pixeles 
(cada pixel es un array de tamaño 3) y lo guarda en v_k """
v_k = list(img.getdata())

""" En el array bkt se guardaran los pixeles codificados de la lista v_k.
Cada pixel codificado sera un array de tamaño 3, que contiene los valores 
codificados de cada canal """
bkt = []

################################## Codificador de fuente ########################################

""" Con este ciclo for se codifica cada pixel en la lista v_k y se agrega
al array de pixeles codificados bkt """
for pixel in v_k:
	binary_pack = pf.code_pack(pixel) # Codifica un pixel y se guarda en binary_pack
	bkt.append(binary_pack) # Agrega el pixel codificado al array bkt

# Guarda en bkt_len la cantidad de pixeles codificados que hay en el array bkt
bkt_len = len(bkt)

""" Con este ciclo for se concatenan los canales codificados de cada pixel en
un solo numero binario, es decir, que ahora por cada pixel no se tendra un array
con 3 valores, sino un solo numero de 24 bits """
for i in range (bkt_len): 
	
	# Guarda en bkt_aux la concatenacion de los 3 canales de un pixel
	bkt_aux = "".join(bkt[i])

	# Guarda el numero concatenado en el espacio del pixel respectivo
	bkt[i] = bkt_aux 

""" Concatena todos los pixeles en una sola cadena, que corresponde a la salida 
del codificador """
bft = "".join(bkt)

################################### Codificador de canal #####################################

# Recorre la cadena de bits original y la separa en paquetes de 4 bits
for i in range(0,len(bft),4):
   bf.append(bft[i:i+4]) 

# Se multiplica cada paquete de 4 bits por la matriz generadora
for i in range(0,len(bf)):
    array_aux =[]
    for j in range(0,4):
        array_aux.append(int(bf[i][j]))

    bc.append(hamming.encode(array_aux))

bc_r = bc # Se copia la secuencia de bits transmitidos bc en la secuencia de bits recibidos bc_r

for i in range(len(bc_r)):
    for j in range(0,7):
        bc_r_aux.append(int(bc_r[i][j]))

bc_r = bc_r_aux
bf = "".join(bf)

################################ Modulador digital banda-base ##################################

''' Se modula la secuencia de bits, que sale del codificacdor de canal, 
a sus correspondientes puntos de constelacion'''
xT = ask.modulate(bc_r)

p = ask.constellation # Se guarda la constelacion de la modulacion en la variable p

print("Los valores de la constelación son:", p) # Se imprime la constelación de la modulacion

################################ Medio de transmisión ruidoso ##################################

xR = GaussianNoise(xT) # Se añade ruido blanco o Gaussiano a la señal modulada

prueba = [2.036898887954852, 2.0375157671303756, 1.910413252208127, 1.9320775329482969, 2.1148532047192887, 2.0220359818807916, 1.964830765655118, 2.2411193113619223, 2.156351787325047, 2.0270157797641484, 1.99651187526255, 2.1045548794488407, 1.8309695956328291, 1.6930808779146052, 2.1553076343539166]
prueba2 = []
prueba3 = []

for i in range(1379007,1379022):
    for j in range(0,100):
        prueba2.append(xT[i].real)
        prueba3.append(xR[i].real)

dt = 0.01
t = np.arange(0, 15, dt)

carrier = np.cos(45*t) # modulador

senal = prueba2*carrier # señal en salida del tx

awgn = prueba3*carrier # señal con ruido

fig, axs = plt.subplots(2, 1)
axs[0].plot(t, senal, color='blue')
axs[0].set_ylabel('señal modulada')

axs[1].plot(t, awgn, color='red')
axs[1].set_ylabel('señal con ruido')

fig.tight_layout()
plt.show()

############################### Demodulador digital banda-base #################################

'''Se demodula una secuencia de puntos recibidos en una secuencia de bits'''
bc_r_aux = ask.demodulate(xR,decision_method='hard') #bc_r_aux es un array de enteros que varian entre 1 y 0 (bits)

''' Se vacia bc_r y se guardan en ella, en una sola cadena, toda la secuencia de bits demodulada.
La diferencia con bc_r_aux es que en este caso la cadena de bits se guarda como un string'''
bc_r = ""

for i in range(len(bc_r_aux)):
    bc_r = bc_r+str(bc_r_aux[i])

################################## Decodificador de canal ######################################

# Recorre la cadena de bits bc_r y la separa en paquetes de 7 bits y se pasa por la matriz de verificación.
for i in range(0,len(bc_r),7):
    array_aux =[]
    for j in range(0,7):
        array_aux.append(int(bc_r[i+j]))
    
    bf_r.append(hamming.decode(array_aux))

#Se concatena los bits que están en la lista bf_r
array_aux =""
for i in range(0,len(bf_r)):
    for j in range(0,4):
        array_aux = array_aux + str(bf_r[i][j])

bf_r = array_aux

#Se calculan la cantidad de aciertos, errores y el BER del decodificador
for i in range(0,len(bf)):
    if bf[i] != bf_r[i]:
        misses+=1
    elif bf[i] == bf_r[i]:
        hits+=1

ber = misses/(misses+hits)

print("Etapa de Decodificador de Canal\nCantidad de aciertos: "+str(hits))
print("Cantidad de errores: "+str(misses))
print("Bit Error Rate (BER): {:0.4f}".format(ber)+"\n")

################################## Decodificador de fuente ######################################

# Recorre la cadena de bits unidos y la separa en paquetes de 24 bits
for i in range(0,len(bf_r), 24): 
	bkR.append(bf_r[i:i+24])

# Decodifica las cadenas de 24 bits y guarda los resultados en el array vR
for i in range(0, len(bkR)):
	vR.append(pf.decode_pack(bkR[i]))

# Convierte el mapa de pixeles recuperados en una imagen bmp y la guarda
newImg = Image.new(img.mode, img.size)
newImg.putdata(vR)
newImg.save('resultado_simetrico.bmp')