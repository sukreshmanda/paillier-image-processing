import math
import primes
import numpy as np
from PIL import Image

class PrivateKey(object):

	def __init__(self, p, q, n):
		self.l = (p-1) * (q-1)
		self.m = paillier.invmod(self.l, n)

	def __repr__(self):
		return '<PrivateKey: {} {}>'.format(self.l, self.m)

class PublicKey(object):

	@classmethod
	def from_n(cls, n):
		return cls(n)

	def __init__(self, n):
		self.n = n
		self.n_sq = n * n
		self.g = n + 1

	def __repr__(self):
		return '<PublicKey: {}>'.format(self.n)

class paillier:
	def __init__(self):
		self.prime_r = 1
		
	def invmod(a, p, maxiter=1000000):

		if a == 0:
			raise ValueError('0 has no inverse mod {}'.format(p))
		r = a
		d = 1
		for i in range(min(p, maxiter)):
			d = ((p // r + 1) * d) % p
			r = (d * a) % p
			if r == 1:
				break
		else:
			raise ValueError('{} has no inverse mod {}'.format(a, p))
		return d

	def modpow(self, base, exponent, modulus):

		result = 1
		while exponent > 0:
			if exponent & 1 == 1:
				result = (result * base) % modulus
			exponent = exponent >> 1
			base = (base * base) % modulus
		return result

	def generate_keypair(self, bits):
		p = primes.generate_prime(bits / 2)
		q = primes.generate_prime(bits / 2)
		n = p * q
		return PrivateKey(p, q, n), PublicKey(n)

	def encrypt(self, pub, plain):
		if(self.prime_r == 1):
			while True:
				self.prime_r = primes.generate_prime(int(round(math.log(pub.n, 2))))
				if self.prime_r > 0 and self.prime_r < pub.n:
					break
		x = pow(self.prime_r, pub.n, pub.n_sq)
		cipher = (pow(pub.g, plain, pub.n_sq) * x) % pub.n_sq
		return cipher

	def e_add(self, pub, a, b):
		"""Add one encrypted integer to another"""
		return a * b % pub.n_sq

	def e_add_const(self, pub, a, n):
		"""Add constant n to an encrypted integer"""
		return int(a) * self.modpow(int(pub.g), int(n), int(pub.n_sq)) % int(pub.n_sq)

	def e_mul_const(self, pub, a, n):
		"""Multiplies an encrypted integer by a constant"""
		a = int(a)
		return self.modpow(a, n, pub.n_sq)

	def decrypt(self, priv, pub, cipher):
		cipher = int(cipher)
		x = pow(cipher, priv.l, pub.n_sq) - 1
		plain = ((x // pub.n) * priv.m) % pub.n
		return plain

	def open_image(self,path):
		image = np.array(Image.open(path))
		return image
	
	def save_image(self,image):
		image = image.astype(np.uint8)
		im = Image.fromarray(image)
		if(len(image.shape) == 3):
			if(image.shape[2] == 4):
				im.save("output.png")
			else:
				im.save("output.jpg")
		else:
			im.save("output.png")
		
	def encrypt_image_temp(self, pub, image):
		img = []
		dimens = image.shape
		for row in image.flatten():
			img.append(self.encrypt(pub,int(row)))
		if(len(dimens) == 3):
			return np.array(img).reshape(dimens[0], dimens[1], -1)
		elif(len(dimens) == 2):
			return np.array(img).reshape(dimens[0], -1)
		else:
			return None
				
	def encrypt_image(self, pub, image):
		string = "Pillier homomorphic encryption is very difficult to generate so it uses a lot resources so of no of channels*width*height >= 2488320 we are stoping it early so that there won't be any waiting......."
		if(np.prod(image.shape) >= 2488320):
			print(string)
			return
		return self.encrypt_image_temp(pub, image)
		
	def decrypt_image(self, priv, pub, image):
		img = []
		dims = image.shape
		for pixel in image.flatten():
			temp = self.decrypt(priv, pub, pixel)
			if(temp > 255):
				img.append(255)
			else:
				img.append(temp)
		if(len(dims) == 4):
			return np.array(img).reshape(dims[0], dims[1], dims[2], -1)
		elif(len(dims) == 3):
			return np.array(img).reshape(dims[0], dims[1], -1)
		elif(len(dims) == 2):
			return np.array(img).reshape(dims[0], -1)
		else:
			return None
			
	def brightness(self, pub, image, value):
		img = []
		dims = image.shape
		for pixel in image.flatten():
			img.append(self.e_add_const(pub, pixel, value))
		if(len(dims) == 3):
			return np.array(img).reshape(dims[0], dims[1], -1)
		elif(len(dims) == 2):
			return np.array(img).reshape(dims[0], -1)
		else:
			None

	def increase_color(self, pub, image, color, value):
		color_schema = {
			"red" : 0,
			"green" : 1,
			"blue" : 2,
			"luminance" : 3
		}
		img = []
		if len(image.shape) == 2:
			return "You con't change "+color+" channel of a gray scale image"
		elif(len(image.shape) >= 3):
			color_channel = image[:,:,color_schema[color]]
			copy = color_channel.copy()
			for i in copy.flatten():
				img.append(self.e_add_const(pub, i, value))
			color_channel = np.array(img).reshape(color_channel.shape[0], -1)

			image[:,:,color_schema[color]] = color_channel
			return image
			
	def mirroring_image(self, pub, image):
		i = 0
		j = image.shape[1]-1
		while(i < j and i+j < image.shape[1]):
			temp = image[:,i].copy()
			image[:,i] = image[:,j].copy()
			image[:,j] = temp.copy()
			i+=1
			j-=1
		return image
		
	def flip_image(self, pub, image):
		i = 0
		j = image.shape[0]-1
		while(i < j and i+j < image.shape[0]):
			temp = image[i].copy()
			image[i] = image[j].copy()
			image[j] = temp.copy()
			i+=1
			j-=1
		return image
		
	def swap_colors(self, pub, image, color1, color2):
		color_schema = {
			"red" : 0,
			"green" : 1,
			"blue" : 2,
			"luminance" : 3
		}
		img = []
		if len(image.shape) == 2:
			return "You con't change "+color+" channel of a gray scale image"
		else:
			first_channel = image[:,:,color_schema[color1]].copy()
			second_chennel = image[:,:,color_schema[color2]].copy()
			image[:,:,color_schema[color2]] = first_channel
			image[:,:,color_schema[color1]] = second_chennel
			return image
	def multiply_by_const(self, pub, image, e):
		img = []
		copy = image.copy()
		dims = image.shape
		for pixel in copy.flatten():
			img.append(self.e_mul_const(pub, pixel, e))
		if(len(dims) == 2):
			return np.array(img).reshape(dims[0], -1)
		elif(len(dims) == 3):
			return np.array(img).reshape(dims[0], dims[1], -1)
		else:
			return np.array(img).reshape(dims[0], dims[1], dims[2] -1)

if __name__ == '__main__':
	priv, pub = generate_keypair(16)
	x = 255
	cx = encrypt(pub, x)
	print(cx)
	y = 1
	cy = encrypt(pub, y)
	print(cy)
	cz = e_add(pub, cx, cy)
	print(cz)
	z = decrypt(priv, pub, cz)
	print(z)
		
