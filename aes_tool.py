from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os
import getpass


# ---------------- PASSWORD STRENGTH ----------------

def check_password_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(not c.isalnum() for c in password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"


# ---------------- KEY DERIVATION ----------------

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,              # 32 bytes = AES-256
        salt=salt,
        iterations=600000,
    )

    return kdf.derive(password.encode())


# ---------------- ENCRYPTION ----------------

def encrypt_file():
    file_path = input("Enter file path to encrypt: ").strip()

    if not os.path.isfile(file_path):
        print("File not found!")
        return

    password = getpass.getpass("Enter password: ")

    print("Password strength:", check_password_strength(password))

    if len(password) < 8:
        print("Password must contain at least 8 characters!")
        return

    try:
        with open(file_path, "rb") as file:
            data = file.read()

        # Generate random salt
        salt = os.urandom(16)

        # Generate AES-256 key
        key = derive_key(password, salt)

        # Generate random nonce
        nonce = os.urandom(12)

        # AES-256-GCM encryption
        aesgcm = AESGCM(key)
        encrypted_data = aesgcm.encrypt(nonce, data, None)

        # Create output folder
        os.makedirs("encrypted_files", exist_ok=True)

        filename = os.path.basename(file_path)
        output_path = os.path.join(
            "encrypted_files",
            filename + ".encrypted"
        )

        # Store:
        # salt + nonce + encrypted data
        with open(output_path, "wb") as file:
            file.write(salt)
            file.write(nonce)
            file.write(encrypted_data)

        print("\nFile encrypted successfully!")
        print("Saved to:", output_path)

    except Exception as e:
        print("Encryption failed:", e)


# ---------------- DECRYPTION ----------------

def decrypt_file():
    file_path = input("Enter encrypted file path: ").strip()

    if not os.path.isfile(file_path):
        print("Encrypted file not found!")
        return

    password = getpass.getpass("Enter password: ")

    try:
        with open(file_path, "rb") as file:
            encrypted_file = file.read()

        # Check minimum size
        if len(encrypted_file) < 28:
            print("Invalid encrypted file!")
            return

        # Extract salt
        salt = encrypted_file[:16]

        # Extract nonce
        nonce = encrypted_file[16:28]

        # Extract encrypted data
        encrypted_data = encrypted_file[28:]

        # Derive the same AES-256 key
        key = derive_key(password, salt)

        # AES-256-GCM decryption
        aesgcm = AESGCM(key)

        try:
            decrypted_data = aesgcm.decrypt(
                nonce,
                encrypted_data,
                None
            )
        except Exception:
            print("\nInvalid password or corrupted encrypted file!")
            return

        # Create output folder
        os.makedirs("decrypted_files", exist_ok=True)

        filename = os.path.basename(file_path)

        if filename.endswith(".encrypted"):
            filename = filename[:-10]

        output_path = os.path.join(
            "decrypted_files",
            filename
        )

        with open(output_path, "wb") as file:
            file.write(decrypted_data)

        print("\nFile decrypted successfully!")
        print("Saved to:", output_path)

    except Exception as e:
        print("Decryption failed:", e)


# ---------------- MAIN MENU ----------------

def main():
    while True:
        print("\n==============================")
        print(" AES FILE ENCRYPTION TOOL")
        print("==============================")
        print("1. Encrypt File")
        print("2. Decrypt File")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            encrypt_file()

        elif choice == "2":
            decrypt_file()

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
