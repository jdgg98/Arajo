
"""
El archivo project_functions.py contiene todas las funciones 
creadas para ser implementadas en ProyectoArajo.py
"""

from os import error
import random

# Funcion que convierte un numero decimal a binario
def dec_a_bin(decimal):
    if decimal <= 0:
        return "0"
    # Aquí almacenamos el resultado
    binario = ""
    # Mientras se pueda dividir...
    while decimal > 0:
        # Saber si es 1 o 0
        residuo = int(decimal % 2)
        # E ir dividiendo el decimal
        decimal = int(decimal / 2)
        # Ir agregando el número (1 o 0) a la izquierda del resultado
        binario = str(residuo) + binario
    return binario

# Funcion que convierte un numero binario de 8 bits en un numero decimal
def bin_a_dec(binario):
	decimal = 0
		
	for j in range (8):
		decimal = decimal + int(binario[j])*(pow(2,(7-j)))

	return decimal

# Funcion que codifica un pixel de 3 canales: red,green,blue
def code_pack(pack):
	
	r = str(dec_a_bin(pack[0]))
	g = str(dec_a_bin(pack[1]))
	b = str(dec_a_bin(pack[2]))
	
	coded = [r,g,b]
	coded_aux = []
	aux = ""
	
	for code in coded:
		code_len = len(code)
		
		if code_len == 0:
			aux = "00000000"+code
			
		elif code_len == 1:
			aux = "0000000"+code
			
		elif code_len == 2:
			aux = "000000"+code
			
		elif code_len == 3:
			aux = "00000"+code
			
		elif code_len == 4:
			aux = "0000"+code
			
		elif code_len == 5:
			aux = "000"+code
			
		elif code_len == 6:
			aux = "00"+code
		
		elif code_len == 7:
			aux = "0"+code
			
		else:
			aux = code
		coded_aux.append(aux)
		
	coded = coded_aux
	return coded 

# Funcion que decodifica un paquete de 32 bits
def decode_pack(pack):

	r = bin_a_dec(pack[0:8])
	g = bin_a_dec(pack[8:16])
	b = bin_a_dec(pack[16:24])

	decoded = (r,g,b)

	return decoded

def canal_bs(binary_chain):
	hits = 0
	misses = 0
	bf_r = ""

	for i in range(0,len(binary_chain)):
		P_err = random.randrange(0,100)
		aux_bit = binary_chain[i]

		if(P_err <= 30):
			if(binary_chain[i] == "1"):
				aux_bit = "0"
			elif(binary_chain[i] == "0"):
				aux_bit = "1"

		bf_r = bf_r+aux_bit

	for i in range(0,len(bf_r)):
		if bf_r[i] != binary_chain[i]:
			misses+=1
		elif bf_r[i] == binary_chain[i]:
			hits+=1

	print("Cantidad de aciertos: "+str(hits))
	print("Cantidad de errores: "+str(misses))

	return bf_r

"""
def canal_bs(binary_chain):
	hits = 0
	misses = 0
	bf_r = ""

	for i in range(0,len(binary_chain),4):
		P_err = random.randrange(0,100)
		err_bit = random.randrange(0,4)
		aux_chain = []

		for j in range(4):
			aux_chain.append(binary_chain[i+j])

		#print("Cadena original: "+binary_chain[i:i+7])

		if(P_err <= 40):
			#print("Ocurrió cambio")
			if(aux_chain[err_bit] == "1"):
				aux_chain[err_bit] = "0"
			elif(aux_chain[err_bit] == "0"):
				aux_chain[err_bit] = "1"

		aux_chain = "".join(aux_chain)
		#print("Cadena nueva: "+aux_chain)
		bf_r = bf_r+aux_chain

	for i in range(0,len(bf_r)):
		if bf_r[i] != binary_chain[i]:
			misses+=1
		elif bf_r[i] == binary_chain[i]:
			hits+=1

	print("Cantidad de aciertos: "+str(hits))
	print("Cantidad de errores: "+str(misses))

	return bf_r"""