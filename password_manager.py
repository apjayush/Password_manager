from cryptography.fernet import Fernet
import getpass
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    while True:
        try:
            choice = input("Would you like to add a new password or view existing one (view, add), press q to quit?\n")
            if choice.lower() =="add":
                add()
            elif choice.lower() == "view":
                view()
            elif choice.lower() == "remove":
                remove()
            elif choice.lower() == "update":
                update()            
            elif choice.lower() == "q":
                print("Exiting the program")
                break   
            else:
                print("Enter a valid input from the options available ") 
        except ValueError:
            print("Invalid input!! Try Again")


def authentication():
    try:
        with open('master_pass.txt', "rb") as file:
            stored_encrypted_password = file.read()
            master_pass = input(('Enter the master password\n'))

            key =  os.getenv('MY_ENCRYPTION_KEY').encode()

            # print(type(key))

            fernet = Fernet(key)

        decrypted_master_pass = fernet.decrypt(stored_encrypted_password).decode()

        if master_pass == decrypted_master_pass:
            print("Authentication successful!")
            fer,status = fernet, True
            return fer,status
        else:
            fer,status = fernet, False
            return None,status
    except Exception as e:
        print("Error occurred during authentication:", e)
        return None, False

    
  
def add():
    try:
        fernet, verified = authentication()
        if verified:
            print("Adding a new password...")
            name = input('Enter your username\n')
            password = input('Enter your password\n')
            encrypted_password = fernet.encrypt(password.encode())  # Encrypt and decode
            with open('passwords.txt', 'ab') as f:
                    f.write(name.encode() + b"|" + encrypted_password + b"\n")  # Write a newline after each password     
    except Exception as e:
        print("Error while adding passwords", e)
        
            
        
def view():
    try:
        fernet, verified = authentication()
        if verified:
            print("To view your password...")
            name = input('Enter your username\n')
            # password = input('Enter your password\n')
            # encrypted_password = fernet.encrypt(password.encode())  # Encrypt and decode
            with open("passwords.txt", "rb") as file:
                data = file.readlines()
                for line in data:
                    arr = line.split(b"|")
                    if(arr[0]==name.encode()):
                        print("Password", fernet.decrypt(arr[1]).decode())  
                        break  
                else:
                        print(f"No password found for username {name}")
        else:
            print("Wronng Credentials")            
    except Exception as e:
        print("Error while viewing password", e)            

def remove():
    pass

def update():
    pass


if __name__ == "__main__":
    main()

