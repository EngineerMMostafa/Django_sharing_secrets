from django.test import TestCase
import encryption


class TestEncryptionMethods(TestCase):
    def test_symmetric_encryption_decryption(self):
        secret = 'TEST SECRET'
        symmetric_key = encryption.generate_symmetric_key()

        encrypted_secret = encryption.encrypt_secret(secret, symmetric_key)
        decrypted_secret = encryption.decrypt_secret(encrypted_secret, symmetric_key)

        self.assertEqual(secret, decrypted_secret)

    def test_asymmetric_encryption_decryption(self):
        secret = 'TEST SECRET'
        private_key, public_key = encryption.generate_rsa_key_pair()

        encrypted_symmetric_key = encryption.encrypt_symmetric_key(private_key, public_key)
        decrypted_symmetric_key = encryption.decrypt_symmetric_key(encrypted_symmetric_key, private_key)

        symmetric_key = encryption.generate_symmetric_key()
        encrypted_secret = encryption.encrypt_secret(secret, symmetric_key)
        decrypted_secret = encryption.decrypt_secret(encrypted_secret, decrypted_symmetric_key)

        self.assertEqual(secret, decrypted_secret)
