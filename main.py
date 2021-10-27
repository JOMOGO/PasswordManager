import string
import random
import csv
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d


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

    # encrypting
    message_joined = message_joined.encode()
    encrypted_message = fernet_master_pw.encrypt(message_joined)

    # Put info into database csv file
    with open('passwords.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(encrypted_message)


master_pw = input("Pick your master password: ")
fernet_master_pw = Fernet(master_pw)

while master_pw == master_pw:
    # Generate password based on parameters given.
    what_to_do = input(f"What do you want to do?\nOptions: New, Last3 or close: ")
    if what_to_do == "new":
        # Invoking the password generation function.
        generate_random_password()
    elif what_to_do == "last3":
        # TODO get the last 3 passwords from database and decrypt with master password THIS DOES NOT WORK YET
        with open('passwords.csv') as f:
            f = bytes(f)
            last3 = list(f)[-3:]
            decrypted = fernet_master_pw.decrypt(f)
            print(decrypted)

    elif what_to_do == "close":
        exit()
    else:
        print(f"No option chosen")
