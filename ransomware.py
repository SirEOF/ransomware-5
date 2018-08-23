from random import randint
from os.path import getsize
from os import remove
from struct import pack,unpack,calcsize
from Crypto.Cipher import AES 
import Crypto.Random
from hashlib import sha256
from getfiles import get_files,get_enc_files

chunksize=64*1024


password = 'chaitanyarahalkar'

key = sha256((password).encode('utf-8')).digest()

startpath = '/Users/chaitanyarahalkar/Downloads/Financial Information/'

def encrypt_file(filename,key):
	enc_file = filename + '.enc' 
	iv = Crypto.Random.OSRNG.posix.new().read(AES.block_size)
	encryptor = AES.new(key,AES.MODE_CBC,iv)
	filesize = getsize(filename)

	with open(filename,'rb') as f:
		with open(enc_file,'wb') as fout:
			fout.write(pack('<Q',filesize))
			fout.write(iv)

			while True:
				chunk = f.read(chunksize)
				if len(chunk) == 0:
					break
				elif len(chunk) % 16 !=0:
					chunk+= (' ' * (16 - len(chunk) % 16)).encode('utf-8')
				fout.write(encryptor.encrypt(chunk))
	remove(filename)


def decrypt_file(filename,key):
	orig_filename = filename.split('.enc')[0]
	with open(filename,'rb') as f:
		size = unpack('<Q',f.read(calcsize('Q')))[0]
		iv = f.read(16)
		decryptor = AES.new(key, AES.MODE_CBC,iv)

		with open(orig_filename,'wb') as fout:
			while True:
				chunk = f.read(chunksize)
				if len(chunk) == 0:
					break 
				fout.write(decryptor.decrypt(chunk))
			fout.truncate(size)
	remove(filename)

for file in get_files(startpath):
	print('Encrypting file : ' + file)
	encrypt_file(file,key)

for file in get_enc_files(startpath):
	print('Decrypting file : ' + file)
	decrypt_file(file,key)
