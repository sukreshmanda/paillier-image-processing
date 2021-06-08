import numpy as np
from PIL import Image
from paillier import *
import sys
from matplotlib import pyplot as plt

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
    
class main:
	def __main__(self):
		self.imagepath = None
		self.c_image = None
		self.image = None
		self.is_image_loaded = False
		self.is_encrypted = False
		
		self.pail = paillier()
		self.priv, self.pub = self.pail.generate_keypair(20)
		
	def start(self):
		pass
def nothing():
	pail = paillier()
	image = pail.open_image('simple.png')
	priv, pub = pail.generate_keypair(20)	
	c_image = pail.encrypt_image(pub,image)

	#c_image = pail.multiply_by_const(pub, c_image, 2)	

	#c_image = pail.swap_colors(pub, c_image, 'red', 'green')

	#c_image = pail.flip_image(pub, c_image)	
	
	#c_image = pail.mirroring_image(pub, c_image)

	#p_image = pail.increase_color(pub, c_image, "red", 100)

	#c_image = pail.brightness(pub,c_image, 40)

	d_image = pail.decrypt_image(priv, pub, c_image)

	pail.save_image(d_image)

if __name__ == '__main__':

	pail = paillier()
	original = pail.open_image(sys.argv[1])
	priv, pub = pail.generate_keypair(20)	
	c_image = pail.encrypt_image(pub, original)
	
	print("Enter help for options..")
	while(True):
		a = input(bcolors.OKCYAN+"(paillier)#> "+bcolors.ENDC)
		try:
			inputs = a.strip().split()
			if(inputs[0] == 'brightness'):
				c_image = pail.brightness(pub,c_image, int(inputs[1]))
			elif(inputs[0] == 'color'):
				c_image = pail.increase_color(pub, c_image, inputs[1], int(inputs[2]))
			elif(inputs[0] == 'mirror'):
				c_image = pail.mirroring_image(pub, c_image)
			elif(inputs[0] == 'flip'):
				c_image = pail.flip_image(pub, c_image)
			elif(inputs[0] == 'swap'):
				c_image = pail.swap_colors(pub, c_image, inputs[1] , inputs[2] )
			elif(inputs[0] == 'multiply'):
				c_image = pail.multiply_by_const(pub, c_image, 2)
			elif(inputs[0] == 'print'):
				print(c_image)
			elif(inputs[0] == 'show'):
				fig = plt.figure(figsize=(10, 7))
				
				fig.add_subplot(1, 2, 1)
				if(len(original.shape) == 2):
					plt.imshow(original, cmap='gray')
				else:
					plt.imshow(original)
				plt.axis('off')
				plt.title("Original")
				
				result = pail.decrypt_image(priv, pub, c_image) 
				fig.add_subplot(1, 2, 2)
				if(len(result.shape) == 2):
					plt.imshow(result, cmap='gray')
				else:
					plt.imshow(result)
				plt.axis('off')
				plt.title("Result")
		
				plt.show()
			elif(inputs[0] == 'keys'):
				print(bcolors.OKGREEN+"{} {}".format(pub,priv)+bcolors.ENDC)
			elif(inputs[0] == 'help'):
				print(bcolors.OKGREEN+"\tbrightness {value}\n\tcolor {color} {value}\n\tmirror\n\tflip\n\tswap {color1} {color2}\n\tmultiply {value}\n\tshow\n\tprint\n\tkeys"+bcolors.ENDC)
			else:
				print("Wrong input...")
				print(bcolors.OKGREEN+"\tbrightness {value}\n\tcolor {color} {value}\n\tmirror\n\tflip\n\tswap {color1} {color2}\n\tmultiply {value}\n\tshow\n\tprint\n\tkeys"+bcolors.ENDC)
		except:
			print("Wrong input...")
			print(bcolors.OKGREEN+"\tbrightness {value}\n\tcolor {color} {value}\n\tmirror\n\tflip\n\tswap {color1} {color2}\n\tmultiply {value}\n\tshow\n\tprint\n\tkeys"+bcolors.ENDC)
