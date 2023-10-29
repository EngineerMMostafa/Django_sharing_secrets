# Secret Sharing RESTful API
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

The application will now be running at http://127.0.0.1:3030
You can use an HTTP client like curl postman or httpie to interact with the API.

## API Endpoints
The following API endpoints are available:

- POST http://localhost:3030/api/user/register 
  - add new user 
   - payload : 
    ```json
          {"username": "test_user1",
           "password": "password1"
            }
    ```
  - response sample :
    ```json
    {
    "id": 1,
    "username": "test_user1",
    "private_key": "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUNkZ0lCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQW1Bd2dnSmNBZ0VBQW9HQkFLVThJaGtxWndZdXoxRWgKdkJSa014eVpHRGZsOGU1V2NIZ1JNZVdNUlM5RnA5R0xSb29SdEhQeUU1dDhrbWFyNEdPdzRHUm8rNjQxTzl5WQpUV2k5L0ZnZy9LSEI1eHByV1lmbUJ2NFQxVFpSVmNRM2NOcjZlMG5tQURrOHZXZTlhdUNodG4xeXhxWGVrZkhlCjNQbURuK0tBdWN1RnBHOW9aVGhYNTV3M3hiYzdBZ01CQUFFQ2dZQktsZ1ZTVk1paWl0aThaN3p0ZTNseTdFeDUKVnd2SktTMmxsU1Z2MTh5WEZSczJ4R2E0Qmx2dGhwV0JOMDhpbDIwM3N1em5obGd0Z0F3Z2ZJTmN4MzJ6VkZyVQpZaXBjanhKVWcrWEt2VENaV1RORkNlMHZZN1hVKytXeHNqTnF5RzJJdWh3WFJHdmZhNFFaajRocndoWERqR1Z1Cm5iR3hDQjkya1hSSlJxTEZrUUpCQU5ueDZEdk92dXlxSU9ubFlqeW55Q0dyNmdzUzFPR3JjZzFsSUc4bTY4TU4KVGJGeFk5T3NlZEhZYmVlWEUxWUxoc1E5NEZWVFF5WjZXOEFpYmtXV2Mva0NRUURDRmhrSzRPUGREY2cvNVNZbwovcGVsdkp4NHA5aFluUFF3Wmt2SVR1Sm5UOVNvUDFlWUlvWXc2eEw0V3RzTnc2bUZzcnNKOWlwSEJNN1RYblJuCmkyblRBa0JENnMzTExYOXo4d1IwdnlYZzd3dy82Zm55WDNqMXBsN1JhODB5dGpkTVBtNFN1Tm82RVlxWTZWQSsKbG1iUkxxQmRzVWFpY0dNQnI2bTk4enpYOUszSkFrQVhIZ2F4a3dQUkNwazFjeGZPZmpTVjJ4ZFFENzNuSUJxOQp3UkY1dEZ1bkxvMEgxVE9idlZENmRxVjF5MnlZQVJ3cC9wWGtvOXQ1Umd0VWhjV2JwN0ZkQWtFQWoxREZKanZECndzQ1htOTU1ZVhNMlAvY3NtQmdHdXNmeHhtWWVsQmErKzZFMlNuYmUzeTd4Vy9iQlptdDFPdkNoKzgzZWxYWkkKWTd1VWdlLzdhdHcvTVE9PQotLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tCg=="
    }
    ```

- GET http://localhost:3030/api/users 
  - get all users 
   - authentication : 
    ```
    HTTPBasicAuth("username", "password")
    ```
  - response sample :
    ```json
    [{
            "id": 1,
            "username": "test_user1"
        }, {
            "id": 2,
            "username": "test_user2"
        }, {
            "id": 3,
            "username": "test_user3"
        }
    ]
    ```

- POST http://localhost:3030/api/secrets/create 
  - add new user 
   - authentication : 
    ```
    HTTPBasicAuth("username", "password")
    ```
   - payload : 
    ```json
    {"content": "This is secret 1 from user testuser1.",
     "shared_with": ["test_user2", "test_user3"]
          }
    ```
  - response sample :
    ```json
    {"message":"Secret created successfully"}
    ```

- POST http://localhost:3030/api/user/secrets 
  - retrieve user secrets 
   - authentication : 
    ```
    HTTPBasicAuth("username", "password")
    ```
   - payload : 
    ```json
    {
        "private_key": "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUNkUUlCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQWw4d2dnSmJBZ0VBQW9HQkFNUng3VjQ0YjF6QWxwREQKenl5ajBzUy9nWmxVblRnQTJGaisvbjhGR0JLbzVRV3JlSEJEY1prR0VRblVmLzY0OEFWS25qSHFiaU9MSWx5Sgo5NW5Obkw3MFQ3c3lGY3ExV1BKa1VvUkdNTGVSd1lFNXZzV2c1cU1OdlpmN3MzbE04RFlNdkhiYVJTRlRYWTMyCjE2S3U0aGFlK2xjWUgzNGx1SUpLbkpycVpUelhBZ01CQUFFQ2dZQU1rWUZ2VXNzRk15a3U3K2cwWWZMZE5hZDAKQ083YUkydTBIZlJvYWdvRlA1c1BoczM0Mk1mTzA0MkpoSGYvOHhNZ000cjFoSnN4V1BpRTFTcnJRelZ4QVh2eQpBODVQS0s5UzVLckhwSmZucjMrbEVJVThoUDFzVU9zTnFMQ3pwam1LN3RIc1lpUHh1TzZ3RktsdjJldE55dm8vCnRSaU45UDh2alRjRW1xTnllUUpCQU9MMU1ySDRrOHZnMUNsdHNzSmxpNnIzOG4xU3ZVZ3dZenpRd0wzQ1JQaW8KK2tZUEpQRnRpMExDTDVrcmkyc1NzUE5UTmdWcER2TEN1ZThtTm05MytIMENRUURkbFN6KzE3eXVsV09HN1JwVQpZZFlJNVh4bzRhNTJCWHFYSlRnMktwTVc5OXArcEZVa09sR3hGOXR4eWRxZHkyS1p3dTJWV2oxSXYyazE0U0JOCnZsN2pBa0F1Z2p6UFI3ZFIwbExuNG5qOWFUM0QzV2V0MHVUREJGZHh3UDJlWlU4by9jZTd6NktzYnR4WTQ5NUoKTHlrMDJmRzFDMXBJcFl6UXBxTGZwUjhHbkxrcEFrQi8yYkVLb2dRV1g4LzdiQmRERk9oZ1hiazQ4dTZzM21CcgprV2dycU1rUitaU3llYk0rb2YrOHhOMHpmSnFOYldySStYWUlOUGNqWUg0ZVBuVmJKanF0QWtBN3RXRzcvSzZkCjF6ZnlWSklvaTRpVm1CY1gyU0Z5WXd3ZXhpWlBLa3hEM01keWxVUXB5S2NZb2tEZllZN1NCM0JaYmRzdnNZcGkKV0o5bXpDcU53WlhGCi0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS0K"
    }
    ```
  - response sample :
    ```json
    {
        "secrets": [{
                "content": "This is secret 1 from user testuser1.",
                "created_at": "2023-10-29T07:48:33.905184Z"
            }, {
                "content": "This is secret 2 from user testuser1.",
                "created_at": "2023-10-29T07:49:32.706819Z"
            }, {
                "content": "This is secret 2 from user testuser1.",
                "created_at": "2023-10-29T07:51:18.260292Z"
            }, {
                "content": "This is secret 3 from user testuser1.",
                "created_at": "2023-10-29T07:51:38.883363Z"
            }
        ]
    }
    ```

- POST http://localhost:3030/api/user/shared_secrets 
  - retrieve user secrets 
   - authentication : 
    ```
    HTTPBasicAuth("username", "password")
    ```
   - payload : 
    ```json
    {
        "private_key": "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUNkUUlCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQWw4d2dnSmJBZ0VBQW9HQkFNUng3VjQ0YjF6QWxwREQKenl5ajBzUy9nWmxVblRnQTJGaisvbjhGR0JLbzVRV3JlSEJEY1prR0VRblVmLzY0OEFWS25qSHFiaU9MSWx5Sgo5NW5Obkw3MFQ3c3lGY3ExV1BKa1VvUkdNTGVSd1lFNXZzV2c1cU1OdlpmN3MzbE04RFlNdkhiYVJTRlRYWTMyCjE2S3U0aGFlK2xjWUgzNGx1SUpLbkpycVpUelhBZ01CQUFFQ2dZQU1rWUZ2VXNzRk15a3U3K2cwWWZMZE5hZDAKQ083YUkydTBIZlJvYWdvRlA1c1BoczM0Mk1mTzA0MkpoSGYvOHhNZ000cjFoSnN4V1BpRTFTcnJRelZ4QVh2eQpBODVQS0s5UzVLckhwSmZucjMrbEVJVThoUDFzVU9zTnFMQ3pwam1LN3RIc1lpUHh1TzZ3RktsdjJldE55dm8vCnRSaU45UDh2alRjRW1xTnllUUpCQU9MMU1ySDRrOHZnMUNsdHNzSmxpNnIzOG4xU3ZVZ3dZenpRd0wzQ1JQaW8KK2tZUEpQRnRpMExDTDVrcmkyc1NzUE5UTmdWcER2TEN1ZThtTm05MytIMENRUURkbFN6KzE3eXVsV09HN1JwVQpZZFlJNVh4bzRhNTJCWHFYSlRnMktwTVc5OXArcEZVa09sR3hGOXR4eWRxZHkyS1p3dTJWV2oxSXYyazE0U0JOCnZsN2pBa0F1Z2p6UFI3ZFIwbExuNG5qOWFUM0QzV2V0MHVUREJGZHh3UDJlWlU4by9jZTd6NktzYnR4WTQ5NUoKTHlrMDJmRzFDMXBJcFl6UXBxTGZwUjhHbkxrcEFrQi8yYkVLb2dRV1g4LzdiQmRERk9oZ1hiazQ4dTZzM21CcgprV2dycU1rUitaU3llYk0rb2YrOHhOMHpmSnFOYldySStYWUlOUGNqWUg0ZVBuVmJKanF0QWtBN3RXRzcvSzZkCjF6ZnlWSklvaTRpVm1CY1gyU0Z5WXd3ZXhpWlBLa3hEM01keWxVUXB5S2NZb2tEZllZN1NCM0JaYmRzdnNZcGkKV0o5bXpDcU53WlhGCi0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS0K"
    }
    ```
  - response sample :
    ```json
    {
    "shared_secrets": [{
            "secret_owner": "test_user1",
            "content": "This is secret 1 from user testuser1.",
            "created_at": "2023-10-29T07:51:18.260292Z"
        }, {
            "secret_owner": "test_user3",
            "content": "This is secret 1 from user testuser3.",
            "created_at": "2023-10-29T07:51:38.883363Z"
        }
    ]
    }
    ```
