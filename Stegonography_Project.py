import cv2
import os
import string
from Crypto.Cipher import AES
import base64
import hashlib

def pad_message(msg):
    # Padding to ensure the message is a multiple of 16 bytes
    while len(msg) % 16 != 0:
        msg += ' '
    return msg

def encrypt_message(msg, password):
    key = hashlib.sha256(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_message = base64.b64encode(cipher.encrypt(pad_message(msg).encode()))
    return encrypted_message.decode('utf-8')

def decrypt_message(encrypted_message, password):
    key = hashlib.sha256(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_message = cipher.decrypt(base64.b64decode(encrypted_message)).decode('utf-8').strip()
    return decrypted_message

img = cv2.imread("SecretX.jpg") # Replace with the correct image path

msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

encrypted_msg = encrypt_message(msg, password)

d = {}
c = {}

for i in range(255):
    d[chr(i)] = i
    c[i] = chr(i)

m = 0
n = 0
z = 0

for i in range(len(encrypted_msg)):
    img[n, m, z] = d[encrypted_msg[i]]
    n = n + 1
    m = m + 1
    z = (z + 1) % 3

cv2.imwrite("encryptedImage.jpg", img)
os.system("start encryptedImage.jpg")  # Use 'start' to open the image on Windows

message = ""
n = 0
m = 0
z = 0

pas = input("Enter passcode for Decryption: ")
if password == pas:
    for i in range(len(encrypted_msg)):
        message = message + c[img[n, m, z]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3
    decrypted_msg = decrypt_message(message, password)
    print("Decrypted message:", decrypted_msg)
else:
    print("Your Passcode Is Wrong 👻")
