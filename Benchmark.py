from __future__ import print_function
import argparse
import os 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import numpy as np 
import matplotlib.pyplot as plt 
from collections import OrderedDict
import json
from math import log10
import time 



def init(file_path):
	key128 = os.urandom(16)
	key192 = os.urandom(24)
	key256 = os.urandom(32)
	iv = os.urandom(16)
	iv2 = os.urandom(8)

	with open(file_path, 'r+') as file:
		rl = file.readlines()
		lines = rl[:len(rl) // 50]
		length = len(lines)
	return key128, key192, key256, iv, iv2, lines, length



def prepare_encryptors_128bit(key, iv, iv2):
	print('Preparing 128bit Block Ciphers...')

	aes = Cipher(algorithms.AES(key), mode=modes.CBC(iv), backend=default_backend())
	blowfish = Cipher(algorithms.Blowfish(key), mode=modes.CBC(iv2), backend=default_backend())
	camellia = Cipher(algorithms.Camellia(key), mode=modes.CBC(iv), backend=default_backend())
	triple_DES = Cipher(algorithms.TripleDES(key), mode=modes.CBC(iv2), backend=default_backend())
	seed = Cipher(algorithms.SEED(key), mode=modes.CBC(iv), backend=default_backend())
	idea = Cipher(algorithms.IDEA(key), mode=modes.CBC(iv2), backend=default_backend())
	cast5 = Cipher(algorithms.CAST5(key), mode=modes.CBC(iv2), backend=default_backend())

	aes_encryptor = aes.encryptor()
	blowfish_encryptor = blowfish.encryptor()
	camellia_encryptor = camellia.encryptor()
	tripleDES_encryptor = triple_DES.encryptor()
	seed_encryptor = seed.encryptor() 
	idea_encryptor = idea.encryptor()
	cast5_encryptor = cast5.encryptor()

	encryptors = OrderedDict([('aes', aes_encryptor), ('blowfish', blowfish_encryptor), ('camellia', camellia_encryptor), 
		('3DES', tripleDES_encryptor), ('seed', seed_encryptor), ('idea', idea_encryptor), ('cast5', cast5_encryptor)])

	return encryptors



def prepare_encryptors_192bit(key, iv, iv2):
	print('Preparing 192bit Block Ciphers...')

	aes = Cipher(algorithms.AES(key), mode=modes.CBC(iv), backend=default_backend())
	blowfish = Cipher(algorithms.Blowfish(key), mode=modes.CBC(iv2), backend=default_backend())
	camellia = Cipher(algorithms.Camellia(key), mode=modes.CBC(iv), backend=default_backend())
	triple_DES = Cipher(algorithms.TripleDES(key), mode=modes.CBC(iv2), backend=default_backend())


	aes_encryptor = aes.encryptor()
	blowfish_encryptor = blowfish.encryptor()
	camellia_encryptor = camellia.encryptor()
	tripleDES_encryptor = triple_DES.encryptor()

	encryptors = OrderedDict([('aes', aes_encryptor), ('blowfish', blowfish_encryptor), ('camellia', camellia_encryptor), 
		('3DES', tripleDES_encryptor)])

	return encryptors



def prepare_encryptors_256bit(key, iv, iv2):
	print('Preparing 256bit Block Ciphers...')

	aes = Cipher(algorithms.AES(key), mode=modes.CBC(iv), backend=default_backend())
	blowfish = Cipher(algorithms.Blowfish(key), mode=modes.CBC(iv2), backend=default_backend())
	camellia = Cipher(algorithms.Camellia(key), mode=modes.CBC(iv), backend=default_backend())


	aes_encryptor = aes.encryptor()
	blowfish_encryptor = blowfish.encryptor()
	camellia_encryptor = camellia.encryptor()


	encryptors = OrderedDict([('aes', aes_encryptor), ('blowfish', blowfish_encryptor), ('camellia', camellia_encryptor)])

	return encryptors



def benchmark(lines, length, encryptors):
	results = OrderedDict([(k, 0) for k in encryptors.keys()])

	for name, _encryptor in encryptors.items():
		count = 0
		start = time.time()

		for line in lines:
			_encryptor.update(line.encode())

			count += 1
			if (count / length) * 100 % 10 == 0:
				print('============={0} {1}%============='.format(name.upper(), (count / length) * 100))

		end = time.time()
		results[name] = end - start

	print('Benchmark Done \r\n\r\n')
	
	return results



def plot_data(results_128, results_192, results_256):
	print('Plotting Data...')

	styles = plt.style.available
	plt.style.use(styles[5])

	fig, ax = plt.subplots()

	width = 0.35
	ax.bar(np.arange(len(results_128.keys())) * 1.5, results_128.values(), width=width, label='Block Cipher 128bit')
	ax.bar(np.arange(len(results_192.keys())) * 1.5 - width, results_192.values(), width=width, label='Block Cipher 192bit')
	ax.bar(np.arange(len(results_256.keys())) * 1.5 + width, results_256.values(), width=width, label='Block Cipher 256bit')
	ax.set_xlabel('Algorithms')
	ax.set_xticks(np.arange(len(results_128.keys())) * 1.5)
	ax.set_xticklabels(list(map(lambda x: x.upper(), results_128.keys())))
	ax.set_ylabel('Time')
	ax.set_title('Block Cipher Benchmark (2GB)')
	ax.legend()
	fig.tight_layout()
	plt.show()



def save_data(results):
	print('Saving data...')
	with open('results.json', 'w') as file:
		json.dump(results, file)



def main():
	parser = argparse.ArgumentParser(description='++++++++++CPU ENCRYPTION BENCHMARK++++++++++')
	parser.add_argument('-p', '--path', required=True, help='Text File Path')
	args = vars(parser.parse_args())

	__start = time.time()

	key128, key192, key256, iv, iv2, lines, length = init(args['path'])

	_encryptors_128bit = prepare_encryptors_128bit(key128, iv, iv2)
	_encryptors_192bit = prepare_encryptors_192bit(key192, iv, iv2)
	_encryptors_256bit = prepare_encryptors_256bit(key256, iv, iv2)

	print('Running 128bit Benchmark...')
	ordered_results_128 = benchmark(lines, length, _encryptors_128bit)
	print('Running 192bit Benchmark...')
	ordered_results_192 = benchmark(lines, length, _encryptors_192bit)
	print('Running 256bit Benchmark...')
	ordered_results_256 = benchmark(lines, length, _encryptors_256bit)

	plot_data(ordered_results_128, ordered_results_192, ordered_results_256)
	save_data({**ordered_results_128, **ordered_results_192, **ordered_results_256})

	__end = time.time()
	print('CPU Score : {0}'.format(1000 / log10(__end - __start)))
	

if __name__ == '__main__':
	main()