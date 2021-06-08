from paillier import *
import random
test_cases = []

def generate_test_cases(n):
	for i in range(n):
		a = random.randint(0, 999999999999999999999999999999)
		b = random.randint(0, 999999999999999999999999999999)
		c = a+b
		test_cases.append([a, b, c])

generate_test_cases(100)
for case in test_cases:
	a = case[0]
	b = case[1]
	z = case[2]
	
	pri, pub = generate_keypair(128)
	
	ca = encrypt(pub, a)
	cz = e_add_const(pub, ca, b)
		
	c = decrypt(pri, pub, cz)
	if(c == z):
		print("Test case passed...")
	else:
		print("{} -> {}".format(z,c))
