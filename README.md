# Secret Sharing" RESTful API
The API should allow users to share encrypted secrets with other users and manage their shared secrets securely

## Application  Encryption theory

In this Django app for secret sharing, encryption plays a critical role in keeping sensitive information secure. To protect users secrets secured and ensure that only authorized users (owner or shared with members) can decrypt them, the application employs a combination of symmetric and asymmetric encryption algorithms. Here's a brief overview of the encryption techniques used in this app:

1. **Symmetric Encryption**:
   - **AES (Advanced Encryption Standard)**: Symmetric encryption is used for its speed and efficiency. In AES, the same key is used for both encryption and decryption. When a user creates a secret message, the app generates a random symmetric key. This key is then used to encrypt the secret message. The symmetric key itself is protected using asymmetric encryption before being shared with authorized recipients.

2. **Asymmetric Encryption**:
   - **RSA (Rivest–Shamir–Adleman)**: Asymmetric encryption is used for securely exchanging the symmetric keys used for message encryption. Each user has a pair of public and private keys. The public key is used for encrypting messages or keys, while the private key is used for decryption.
   
   When a user share a secret with another user, the sender encrypts the randomly generated symmetric key with recipient's public key. This encrypted symmetric key is then sent along with the encrypted message. The recipient uses their private key to decrypt the symmetric key, which is then used to decrypt the secret message.

3. **Key Management**:
   - **User Profiles**: Each user in the system has their own public and private key pair, only public key stored in user profile. User shall securely keep their private key.


4. **Access Control**:
   - **User Authentication**: Users are required to authenticate themselves before they can access their secret messages or generate new ones.

   - **Authorization**: Access to secrets is restricted to the owner and authorized members. Authorization mechanisms, such as role-based access control, determine who can access and decrypt a given secret.

By combining symmetric and asymmetric encryption, your Django app achieves a high level of security. Symmetric encryption is used for its efficiency in encrypting messages, while asymmetric encryption ensures secure key exchange, making it possible for users to securely share secrets with each other. This layered approach helps protect secret messages from unauthorized access, even if the underlying database is compromised.

## App Environment Variables

The following environment variables need to be set for the application to work correctly:

- `ALLOWED_HOSTS`: Set it to `*` or specify a comma-separated list of allowed hosts.

- `CSRF_TRUSTED_ORIGINS`: Set it to `http://127.0.0.1,http://localhost` or update it with your trusted origins.

- `POSTGRES_DB`: Set it to `secret_sharing` or update it with the desired name for the PostgreSQL database.

- `POSTGRES_USER`: Set it to `postgres` or update it with the desired PostgreSQL username.

- `POSTGRES_PASSWORD`: Set it to `Password1` or update it with the desired PostgreSQL password.

- `DB_HOST`: Set it to `db` or update it with the hostname of your PostgreSQL database.

- `POSTGRES_NAME`: Set it to `secret_sharing` or update it with the desired name for the PostgreSQL database.

- `POSTGRES_PORT`: Set it to `5432` or update it with the desired port for the PostgreSQL database.

- `DEBUG`: Set it to `1` to enable debug mode. Update it to `0` in a production environment.



## Running the Application
- run the following command to build images and run containers
  ```sh
    docker-compose up --build
  ```

The application will now be running at http://127.0.0.1:3030.
You can use an HTTP client like curl postman or httpie to interact with the API.
