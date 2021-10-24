import string
import random
import csv
import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Initialise
backend = default_backend()
iterations = 100_000
pw_correct = False


# Defining functions
def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))


def password_encrypt(message: bytes, password: str, iterations: int = iterations) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )


def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)


def generate_random_password():
    # Characters to generate password from
    alphabets = list(string.ascii_letters)
    digits = list(string.digits)
    special_characters = "!@#$%^&*()"
    characters = list(string.ascii_letters + string.digits + special_characters)

    # Asks for length of password and the amount of characters of each
    password_length = int(input("Enter password length: "))
    alphabets_count = int(input("Enter alphabets count in password: "))
    digits_count = int(input("Enter digits count in password: "))
    special_characters_count = int(input("Enter special characters count in password: "))
    characters_count = alphabets_count + digits_count + special_characters_count

    # Give error when the amount of minimum characters is greater then the number of allowed characters
    if characters_count > password_length:
        print("Characters total count is greater than the password length")
        return

    # initializing the password
    gen_password = []

    # picking random characters
    for i in range(alphabets_count):
        gen_password.append(random.choice(alphabets))

    for i in range(digits_count):
        gen_password.append(random.choice(digits))

    for i in range(special_characters_count):
        gen_password.append(random.choice(special_characters))

    # if the total character count is less than the password length add till it is equal
    if characters_count < password_length:
        random.shuffle(characters)
        for i in range(password_length - characters_count):
            gen_password.append(random.choice(characters))

    # shuffling the generated password
    random.shuffle(gen_password)

    # converting the list to string and printing it
    password_joined = str("".join(gen_password))

    # Asks for your username and the website
    website = input("On what website is this?")
    username = input("What is the associated username or email for this login?")
    message_joined = website + '' + username + '' + password_joined
    # Encrypts the password with the master password
    crypt_message = password_encrypt(message_joined.encode(), master_pw)

    # Put info into database csv file
    with open('passwords.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(crypt_message)


master_pw = input(f"Pick your master password: ")
print(master_pw)

while master_pw == master_pw:
    # Generate password based on parameters given.
    what_to_do = input(f"What do you want to do?\nOptions: New, Last3 or close: ")
    if what_to_do == "new":
        # Invoking the password generation function.
        generate_random_password()
    elif what_to_do == "last3":
        # TODO get the last 3 passwords from database and decrypt with master password THIS DOES NOT WORK YET
        # Open the file and read three lines efficiently.
        with open('passwords.csv', 'r') as f:  # open in binary for seek operations
            # Lines created above were 10 bytes long max, go back more than 3x that
            f.seek(-50, 2)  # 2 means end-of-file
            lines = f.readlines()  # read only the last few lines of the file

        token = bytes("token")
        for line in lines[-3:]:  # slice only the last three lines and display.
            print(password_decrypt(token, master_pw).decode())
    elif what_to_do == "close":
        exit()
    else:
        print(f"No option chosen")
