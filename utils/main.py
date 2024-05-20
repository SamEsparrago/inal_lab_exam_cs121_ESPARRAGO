from utils.user_manager import UserManager
import os
import time

def main():
    while True:
        try:
            os.system('cls')
            print("Welcome to Dice Roll Game!")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice, or leave blank to cancel: ")
            if not choice:
                break
            if choice == "1":
                UserManager().register()
            elif choice == "2":
                UserManager().login()
            elif choice == "3":
                os.system('cls')
                msg = "Exiting program..."
                for char in msg:
                    print(char, end="")
                    time.sleep(0.05)
                break
            else:
                print("Invalid choice. Please try again.")
                time.sleep(0.5)
        except ValueError:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")
            time.sleep(0.5)
            
if __name__ == "__main__":
    main()