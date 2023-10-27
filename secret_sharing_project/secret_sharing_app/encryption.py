from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


def generate_symmetric_key():
    """
    Generate a secret using Fernet symmetric key (AES)
    :return: symmetric_key
    """
    return Fernet.generate_key()


def generate_rsa_key_pair():
    """
    Generate an RSA key pair for a new user
    :return: private & public keys
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=1024,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem


def encrypt_secret(secret_content, symmetric_key):
    """
    Encrypt a secret using Fernet (AES)
    :param secret_content:
    :param symmetric_key:
    :return: encrypted_secret
    """
    fernet = Fernet(symmetric_key)
    encrypted_secret = fernet.encrypt(secret_content.encode('utf-8'))
    return encrypted_secret


def encrypt_symmetric_key(symmetric_key, recipient_public_key):
    """
    Encrypt the symmetric key with the recipient's public key (RSA)
    :param symmetric_key:
    :param recipient_public_key:
    :return: encrypted_symmetric_key
    """
    public_key = serialization.load_pem_public_key(recipient_public_key, backend=default_backend())
    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_symmetric_key


def decrypt_secret(encrypted_secret, symmetric_key):
    """
    Decrypt a secret using Fernet (AES)
    :param encrypted_secret:
    :param symmetric_key:
    :return: decrypted_secret
    """
    fernet = Fernet(symmetric_key)
    decrypted_secret = fernet.decrypt(encrypted_secret)
    return decrypted_secret.decode('utf-8')


def decrypt_symmetric_key(encrypted_symmetric_key, recipient_private_key):
    """
    Decrypt the symmetric key using the user's private key (RSA)
    :param encrypted_symmetric_key:
    :param recipient_private_key:
    :return: original_symmetric_key
    """
    private_key = serialization.load_pem_private_key(recipient_private_key, password=None, backend=default_backend())
    symmetric_key = private_key.decrypt(
        encrypted_symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return symmetric_key
