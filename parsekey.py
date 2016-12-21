#!/usr/bin/env python

import rsa, re, sys

def display(idents, data):
	result = re.findall(r'(' + idents[0][0] + '.*' +
						idents[0][1] + ')', data,re.DOTALL)
	for res in result: print idents[1](res)


PUBKEY_IDENTIFIER =  (('-----BEGIN PUBLIC KEY-----', '-----END PUBLIC KEY-----'),
					 rsa.PublicKey.load_pkcs1_openssl_pem)
PRIVKEY_IDENTIFIER = (('-----BEGIN PRIVATE KEY-----', '-----END PRIVATE KEY-----'),
					 rsa.PrivateKey.load_pkcs1)

try:

	data = open(sys.argv[1], 'r').read()

	for ident in (PUBKEY_IDENTIFIER, PRIVKEY_IDENTIFIER):
		display(ident, data)

except:

	print 'Usage: {0} [filename]'.format(sys.argv[0])
