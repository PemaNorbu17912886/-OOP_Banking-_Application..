################################
# Your Name: Pema Norbu
# Your Section: 1 Electrical Engineering
# Your Student ID Number: 02230069
################################
# REFERENCES
# Links that you referred while solving
# the problem
# http://link.to.an.article/video.com
################################
# SOLUTION
# Your Solution Score:
# Put your number here
################################


import os
import random
import string


ACCOUNTS_FILE = "accounts.txt"


def create_account_number():
    return ''.join(random.choices(string.digits, k=10))

def create_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

class Account:
    def __init__(self, account_number, password, account_type, balance=0):
        self.account_number = account_number
        self.password = password
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        return self.balance

class PersonalAccount(Account):
    def __init__(self, account_number, password, balance=0):
        super().__init__(account_number, password, "Personal", balance)

class BusinessAccount(Account):
    def __init__(self, account_number, password, balance=0):
        super().__init__(account_number, password, "Business", balance)
def save_account(account):
    with open(ACCOUNTS_FILE, 'a') as f:
        f.write(f"{account.account_number},{account.password},{account.account_type},{account.balance}\n")

def load_accounts():
    accounts = {}
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as f:
            for line in f:
                account_number, password, account_type, balance = line.strip().split(',')
                balance = float(balance)
                if account_type == "Personal":
                    accounts[account_number] = PersonalAccount(account_number, password, balance)
                elif account_type == "Business":
                    accounts[account_number] = BusinessAccount(account_number, password, balance)
    return accounts

def create_account(account_type):
    account_number = create_account_number()
    password = create_password()
    if account_type == "Personal":
        account = PersonalAccount(account_number, password)
    elif account_type == "Business":
        account = BusinessAccount(account_number, password)
    save_account(account)
    return account

def login(account_number, password):
    accounts = load_accounts()
    account = accounts.get(account_number)
    if account and account.password == password:
        return account
    else:
        raise ValueError("YOUR ACCOUNT NUMBER DOES NOT MATCH WITH YOUR PASSWORD")

def delete_account(account_number):
    accounts = load_accounts()
    if account_number in accounts:
        del accounts[account_number]
        with open(ACCOUNTS_FILE, 'w') as f:
            for account in accounts.values():
                f.write(f"{account.account_number},{account.password},{account.account_type},{account.balance}\n")
        return True
    else:
        return False

def transfer_money(sender_account, receiver_account_number, amount):
    accounts = load_accounts()
    if receiver_account_number in accounts:
        receiver_account = accounts[receiver_account_number]
        sender_account.withdraw(amount)
        receiver_account.deposit(amount)
        with open(ACCOUNTS_FILE, 'w') as f:
            for account in accounts.values():
                f.write(f"{account.account_number},{account.password},{account.account_type},{account.balance}\n")
        return True
    else:
        raise ValueError("INVALID ACCOUNT NUMBER")
def main():
    while True:
        print("Welcome to the Banking Application")
        print("1. Create Bank Account")
        print("2. Login to your account")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            account_type = input("Choose yous bank type (Personal/Business): ")
            account = create_account(account_type)
            print(f"Account created successfully! Account Number: {account.account_number}, Password: {account.password}")
        elif choice == '2':
            account_number = input("Enter account your number: ")
            password = input("Enter your password: ")
            try:
                account = login(account_number, password)
                print("Login successfully!")
                while True:
                    print("1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Funds Transfer")
                    print("5. Delete Account")
                    print("6. Logout")
                    choice = input("Enter your choice: ")

                    if choice == '1':
                        print(f"Your balance is: {account.balance}")
                    elif choice == '2':
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                        print(f"Deposit successful! New balance: {account.balance}")
                    elif choice == '3':
                        amount = float(input("Enter amount to withdraw: "))
                        try:
                            account.withdraw(amount)
                            print(f"Withdrawal successful! New balance: {account.balance}")
                        except ValueError as e:
                            print(e)
                    elif choice == '4':
                        receiver_account_number = input("Enter Valid Account Number: ")
                        amount = float(input("transfer: "))
                        try:
                            transfer_money(account, receiver_account_number, amount)
                            print(f"Transfer successful! New balance: {account.balance}")
                        except ValueError as e:
                            print(e)
                    elif choice == '5':
                        confirmation = input("Are you sure you want to delete your account? (yes/no): ")
                        if confirmation.lower() == 'yes':
                            if delete_account(account.account_number):
                                print("Account deleted successfully!")
                                break
                            else:
                                print("Account deletion failed!")
                    elif choice == '6':
                        print("Logged out successfully!")
                        break
                    else:
                        print("Invalid choice!")
            except ValueError as e:
                print(e)
        elif choice == '3':
            print("Thank you for using the Banking Application. Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
