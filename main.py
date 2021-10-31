"""
Name:           Robin Groot
Version:        2.0
Inputs:         Password length | amount of letters, digits and special characters | Master password
Outputs:        Website | Username | Password
Description:    This program will ask for your inputs to generate a password and save that with the website and username
Important note: You can use a different master password to create and see new passwords but you can't use it on old ones
"""
import string
import random
import csv
import cryptocode
import os


# Gives the last N lines in a file
def get_last_n_lines(file_name, n):
    # Create an empty list to keep the track of last n lines
    list_of_lines = []
    # Open file for reading in binary mode
    with open(file_name, 'rb') as read_obj:
        # Move the cursor to the end of the file
        read_obj.seek(0, os.SEEK_END)
        # Create a buffer to keep the last read line
        buffer = bytearray()
        # Get the current position of pointer i.e eof
        pointer_location = read_obj.tell()
        # Loop till pointer reaches the top of the file
        while pointer_location >= 0:
            # Move the file pointer to the location pointed by pointer_location
            read_obj.seek(pointer_location)
            # Shift pointer location by -1
            pointer_location = pointer_location - 1
            # read that byte / character
            new_byte = read_obj.read(1)
            # If the read byte is new line character then it means one line is read
            if new_byte == b'\n':
                # Save the line in list of lines
                list_of_lines.append(buffer.decode()[::-1])
                # If the size of list reaches n, then return the reversed list
                if len(list_of_lines) == n:
                    return list(reversed(list_of_lines))
                # Reinitialize the byte array to save next line
                buffer = bytearray()
            else:
                # If last read character is not eol then add it in buffer
                buffer.extend(new_byte)
        # As file is read completely, if there is still data in buffer, then its first line.
        if len(buffer) > 0:
            list_of_lines.append(buffer.decode()[::-1])
    # return the reversed list
    return list(reversed(list_of_lines))


# Asks for inputs and checks if they are numbers then changes them from strings to ints
def password():
    # Asks for length of password and the amount of characters of each
    s_password_length = input("Enter password length: ")
    s_alphabets_count = input("Enter alphabets count in password: ")
    s_digits_count = input("Enter digits count in password: ")
    s_special_characters_count = input("Enter special characters count in password: ")
    check_int = s_password_length + s_alphabets_count + s_digits_count + s_special_characters_count
    if check_int.isnumeric():
        global password_length, alphabets_count, digits_count, special_characters_count, characters_count
        password_length = int(s_password_length)
        alphabets_count = int(s_alphabets_count)
        digits_count = int(s_digits_count)
        special_characters_count = int(s_special_characters_count)
        characters_count = alphabets_count + digits_count + special_characters_count
    else:
        print("You can only give whole numbers, Try again.")
        password()


# The main function that generates the password based on your inputs
def generate_random_password():
    # Characters to generate password from
    alphabets = list(string.ascii_letters)
    digits = list(string.digits)
    special_characters = "!@#$%^&*()"
    characters = list(string.ascii_letters + string.digits + special_characters)

    # Asks for inputs for your password
    password()

    # Give error when the amount of minimum characters is greater then the number of allowed characters
    if characters_count > password_length:
        print("Characters total count is greater than the password length")
        password()

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
    website = website.capitalize().strip()
    username = input("What is the associated username or email for this login?")
    message_joined = website + ' | ' + username + ' | ' + password_joined

    # encrypting
    encrypted_message = cryptocode.encrypt(message_joined, master_pw)

    # Put info into database csv file
    with open('passwords.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(encrypted_message)


# Main loop | Asks for master password and what you want to do
master_pw = input("Pick your master password: ")
while master_pw == master_pw:
    what_to_do = input(f"What do you want to do?\nOptions: New, Last or Close: ")
    what_to_do = what_to_do.strip()
    if what_to_do == "new":
        generate_random_password()
    elif what_to_do == "last":
        # Iterate over the list of last n lines and print one by one.
        last_number = int(input("How many passwords do you want to see from newest to oldest."))
        last_lines = get_last_n_lines("passwords.csv", last_number+1)
        print('Last 3 lines of File:\nWebsite | Username | Password')
        for line in last_lines:
            line = cryptocode.decrypt(line, master_pw)
            print(line)
    elif what_to_do == "close":
        exit()
    else:
        print(f"No option chosen, Try again.")
