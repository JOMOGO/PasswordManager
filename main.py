import string
import random
import bcrypt
# import tkinter as tk

# TODO use math module somewhere
# TODO decide if I should use tkinter.
"""
# Creates GUI and renames window.
def new_window():
    window = tk.Toplevel(root)
    login_window = tk.Canvas(window)
    login_window.pack()


root = tk.Tk()
root.title("Password manger")
login = tk.Canvas(root)
login.pack()

# Row 0 | Close the application
tk.Button(root, text="Close application", fg="red", command=quit).pack()

# Row 1 | Asks for your username and password.
label_user = tk.Label(root, text="Username: ").pack()
entry_user = tk.Entry(root).pack()

# Row 2 | Asks for your password
label_password = tk.Label(root, text="Password: ").pack()
entry_password = tk.Entry(root).pack()

# Row 3 | Button to check info and login
button_login = tk.Button(root, text="Login", fg="green").pack()

# button = tk.Button(root, text="new window", bg='black', fg='#469A00', command=lambda: quit, new_window())
# button.pack()

# root.mainloop()
"""
# TODO make a master password with bcrypt
master_password = bytes(input(f"Pick your master password"))
# Hash a password for the first time, with a randomly-generated salt
hashed = bcrypt.hashpw(master_password, bcrypt.gensalt())

# Check that an password matches one that has previously been encrypted
while bcrypt.checkpw(master_password, hashed):

    # Characters to generate password from
    alphabets = list(string.ascii_letters)
    digits = list(string.digits)
    special_characters = "!@#$%^&*()"
    characters = list(string.ascii_letters + string.digits + special_characters)

    # Generate password based on parameters given.
    def generate_random_password():
        # Asks for length of password
        password_length = int(input("Enter password length: "))

        # Number of characters from each type minimum
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

        # picking random alphabets
        for i in range(alphabets_count):
            gen_password.append(random.choice(alphabets))

        # Picking random digits
        for i in range(digits_count):
            gen_password.append(random.choice(digits))

        # Picking random alphabets
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
        print(password_joined)

        # Asks for your username and the website
        username = input("What is the associated username or email for this login?")
        website = input("On what website is this?")

        # TODO Put info into database: Password, website, username)


    # Invoking the function
    generate_random_password()
