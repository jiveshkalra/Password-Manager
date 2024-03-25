import json 
import base64
import os
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    os.system('pip install cryptography') 
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class PasswordManager():
    def __init__(self):
        self.key = None
        self.salt = None 
        self.password = None

    def generate_key(self):
        password = b"Replace this with your password"
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        self.key = base64.urlsafe_b64encode(kdf.derive(password))
        with open('key.key','wb') as key_file:
            key_file.write(self.key)
    
    def load_key(self):
        try:
            with open('key.key','rb') as key_file:
                self.key = key_file.read()
        except FileNotFoundError:
            self.generate_key()
            self.load_key()

    def load_json(self):
        try:
            with open('passwords.json','r') as json_file:
                return json.load(json_file) 
        except FileNotFoundError:
            with open('passwords.json','w') as json_file:
                json.dump({}, json_file)
            return {}
        except json.JSONDecodeError:
            return {}

    def save_json(self, data):
        try:
            with open('passwords.json','w') as json_file:
                json.dump(data, json_file)
        except Exception as e:
            print(f"Error saving JSON file: {e}")

    def encrypt_password(self, data):
        f = Fernet(self.key)
        return f.encrypt(data.encode())
    
    
    def decrypt_password(self, data):
        f = Fernet(self.key)
        return f.decrypt(data).decode()
    
    def save_password(self,password,website,email,username,others):
        data = self.load_json()
        try:
            id =  int(list(data.keys())[-1])
            id += 1 
        except IndexError:
            id = 0 
        password = self.encrypt_password(password)
        data[id] = {
            "website": website,
            "password": password.decode(),
            "email": email, 
            "username": username,
            "others": others
        } 
        self.save_json(data)
        return None

    def read_password(self, website):
        data = self.load_json() 
        for id, info in data.items(): 
            if info["website"] == website:
                return self.decrypt_password(info["password"].encode())
            
        return "Website not found"

    def list_websites(self):
        data = self.load_json()
        websites = []
        for id, info in data.items(): 
            websites.append(f"{info["website"]} - > {info["email"]}")
        return websites

def main():

    pw = PasswordManager()
    pw.load_key()
    print('''
          --------------- Welcome to Password Manager v0.1 -----------------
                                                     -- Made By Jivesh Kalra 
          Functions you can try : 
          1. Generate Key - Generates a new key for encrypting passwords (ONLY TO BE DONE ONE TIME)
          2. Save Password - Save a password for a website (requires password, website, email, username, and optional additional information)
          3. List Websites and Retrieve Password - Lists all the websites for which you have saved passwords and allows you to retrieve the passwords
          4. Exit - Exits the program
          ---------------------------------------------------------------------
    ''')
        
    choice = input("Choose the action you want to do : ")
    if choice == '1':
        print("Generating Key...")
        pw.generate_key()
        print('''
              The key has been generated and saved in key.key file 
              NOTE : Please keep this file safe and do not lose it. 
                If you lose this file, all your passwords will be lost.
              ''') 
    elif choice == '3':
        print("Please enter the following details: ")
        website = input("Enter the website: ")
        email = input("Enter the email: ")
        username = input("Enter the username: ")
        password = input("Enter the password: ")
        others = input("Enter the others: ")
        pw.save_password(password,website,email,username,others)
        print("Your password has been saved successfully!") 
    elif choice == '4':
        websites = pw.list_websites() 
        for number, website in enumerate(websites):
            print(f'[{number}] {website}')
        user_num = int(input("Select the Website number of the website you want password of: "))  
        print(f'Password for {websites[user_num]} is: ') 
        print(pw.read_password(websites[user_num])) 
    elif choice == '5':
        print("Exiting the program...")
        print("Have a nice day!")
        print("-----------------------------------------------------------------")
        exit()
    else:
        print("Invalid choice") 
 
 
if __name__=="__main__":
    while True:
        main()    

