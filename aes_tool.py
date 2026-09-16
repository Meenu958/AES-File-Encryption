from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import getpass


# AES encryption
def encrypt_file():
    filename = input("Enter file name: ")

    if not os.path.exists(filename):
        print("File not found!")
        return

    password = getpass.getpass("Enter password: ")

    # Create a 32-byte AES key from the password
    key = password.ljust(32, "0").encode()[:32]

    # Create a random IV
    iv = os.urandom(16)

    # Create AES cipher
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()

    # Read the file
    with open(filename, "rb") as file:
        data = file.read()

    # Encrypt the data
    encrypted_data = encryptor.update(data) + encryptor.finalize()

    # Save encrypted file
    output = "encrypted_files/" + os.path.basename(filename) + ".encrypted"

    with open(output, "wb") as file:
        file.write(iv + encrypted_data)

    print("File encrypted successfully!")
    print("Saved as:", output)


# AES decryption
def decrypt_file():
    filename = input("Enter encrypted file name: ")

    if not os.path.exists(filename):
        print("File not found!")
        return

    password = getpass.getpass("Enter password: ")

    key = password.ljust(32, "0").encode()[:32]

    # Read encrypted file
    with open(filename, "rb") as file:
        data = file.read()

    # Get IV
    iv = data[:16]

    # Get encrypted data
    encrypted_data = data[16:]

    # Create AES cipher
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()

    # Decrypt
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Create output filename
    original_name = os.path.basename(filename).replace(".encrypted", "")
    output = "decrypted_files/" + original_name

    # Save decrypted file
    with open(output, "wb") as file:
        file.write(decrypted_data)

    print("File decrypted successfully!")
    print("Saved as:", output)


# Main menu
while True:

    print("\n===== AES FILE ENCRYPTION TOOL =====")
    print("1. Encrypt file")
    print("2. Decrypt file")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        encrypt_file()

    elif choice == "2":
        decrypt_file()

    elif choice == "3":
        print("Program closed.")
        break

    else:
        print("Invalid choice!")
