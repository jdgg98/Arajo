import komm
from PIL import Image
import sys
import project_functions as pf # Archivo de funciones creadas

hamming = komm.HammingCode(3)


bc = [] # Copia de la secuencia de bits transmitida
bf = [] # Secuencia de bits original
bc_r = [] # Secuencia de bits recibidos
bf_r = [] # Secuencia de bits de informacion recibidos
bf_r_aux = [] # Array auxiliar para bf
hits = 0
misses = 0

#file = open("bft_short.txt")
#bft = file.read()
#file.close()

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

print("len bc_r: "+str(len(bc_r[0])))

for i in range(0,len(bc_r)):
    bf_r.append(hamming.decode(bc_r[i]))

print("len bf_r: "+str(len(bf_r[0])))

for i in range(len(bf_r)):
    for j in range(0,4):
        bf_r_aux.append(str(bf_r[i][j]))

bf = "".join(bf)
bf_r = "".join(bf_r_aux)

for i in range(0,len(bf)):
    if bf[i] != bf_r[i]:
        misses+=1
    elif bf[i] == bf_r[i]:
        hits+=1

print("Cantidad de aciertos: "+str(hits))
print("Cantidad de errores: "+str(misses))
#print(bf_r)

''' En la etapa de decodificacion se guardaran en el array bkR
los paquetes de 24 bits que componen la salida del codificador '''
bkR=[] 

''' En el array vR se guardaran los pixeles decodificados
en la etapa de decodificación'''
vR=[]

# Recorre la cadena de bits unidos y la separa en paquetes de 24 bits
for i in range(0,len(bf_r), 24): 
	bkR.append(bf_r[i:i+24])

# Decodifica las cadenas de 24 bits y guarda los resultados en el array vR
for i in range(0, len(bkR)):
	vR.append(pf.decode_pack(bkR[i]))

# Convierte el mapa de pixeles recuperados en una imagen bmp y la guarda
newImg = Image.new(img.mode, img.size)
newImg.putdata(vR)
newImg.save('resultado_ideal.bmp')