from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from definitions import PRIVATE_KEY_PATH, PUBLIC_KEY_PATH


def encrypt_string(value):
    with open(PUBLIC_KEY_PATH, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    encrypted = public_key.encrypt(
        bytes(value, 'utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted


def decrypt_bytes(encrypted_bytes: bytes) -> str:
    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            backend=default_backend(),
            password=None
        )

        decrypted_bytes = private_key.decrypt(encrypted_bytes,
                                              padding.OAEP(
                                                  mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                  algorithm=hashes.SHA256(),
                                                  label=None))
        return decrypted_bytes.decode('utf-8')

