#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install pycryptodome
# OR:
# pip install pycryptodomex


from Crypto.PublicKey import RSA


secret_code = "Unguessable"
key = RSA.generate(2048)
encrypted_key = key.export_key(passphrase=secret_code, pkcs=8, protection="scryptAndAES128-CBC")

with open("rsa_key.bin", "wb") as f:
    f.write(encrypted_key)

print(key.publickey().export_key())
