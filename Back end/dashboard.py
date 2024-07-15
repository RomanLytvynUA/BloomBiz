from src import app, db
import argparse
import os
from src.models.auth import RegistrationCode, User
import secrets
import string
from fake_data import populate_fake_data


def invalidate_code(code):
    code_obj = RegistrationCode.query.filter_by(code=code).first()
    if not code_obj:
        print(f"Could not find code {code}...")
    else:
        db.session.delete(code_obj)
        db.session.commit()
        print(f"{code} - INVALID")


def generate_reg_code():
    letters_uppercase = string.ascii_uppercase
    digits = string.digits

    code = (
        secrets.choice(letters_uppercase)
        + secrets.choice(letters_uppercase)
        + "".join(secrets.choice(digits) for _ in range(4))
        + secrets.choice(letters_uppercase)
        + secrets.choice(letters_uppercase)
        + secrets.choice(letters_uppercase)
    )

    # check for duplicate
    if len(RegistrationCode.query.filter_by(code=code).all()):
        generate_reg_code()
    else:
        new_code = RegistrationCode(code=code)
        db.session.add(new_code)
        db.session.commit()

        return new_code.code


action = input(
    "Select action to perform:\n"
    "[1] Generate a registration code\n"
    "[2] View registration codes\n"
    "[3] Invalidate all registration codes\n"
    "[4] Invalidate a registration code\n"
    "[5] View users\n"
    "[6] Delete an account\n"
    "[7] Create an account\n"
    "[fd] Populate fake data\n"
    "\n[e] Exit\n"
    "[h] Show this help sheet\n\n"
)

prompted = True
while True:
    if not prompted:
        action = input("Select action to perform: ")
        os.system("cls" if os.name == "nt" else "clear")
    prompted = False

    with app.app_context():
        match action:
            case "h":
                action = input(
                    "Select action to perform:\n"
                    "[1] Generate a registration code\n"
                    "[2] View registration codes\n"
                    "[3] Invalidate all registration codes\n"
                    "[4] Invalidate a registration code\n"
                    "[5] View users\n"
                    "[6] Delete an account\n"
                    "[7] Create an account\n"
                    "[fd] Populate fake data\n"
                    "\n[e] Exit\n"
                    "[h] Show this help sheet\n\n"
                )
                prompted = True
            case "e":
                break
            case "1":
                print("Generating registration code...")
                print(f"Code: {generate_reg_code()}")

            case "2":
                codes = RegistrationCode.query.all()
                if len(codes):
                    print("Valid registration codes:")
                    for i, code in enumerate(codes):
                        print(f"  [{i+1}] {code.code}")
                else:
                    print("No valid registration codes found...")

            case "3":
                if input("Invalidate ALL registration codes[Y/n]? ") == "Y":
                    print("Invalidating registration codes...")
                    for code in RegistrationCode.query.all():
                        invalidate_code(code.code)
                else:
                    print("Exiting...")

            case "4":
                code = input("Enter rigistration code to invalidate: ")
                if input(f"Invalidate {code} registration code[Y/n]? ") == "Y":
                    invalidate_code(code)
                else:
                    print("Exiting...")

            case "5":
                users = User.query.all()
                if len(users):
                    print("Users:")
                    for i, user in enumerate(users):
                        print(f"  [{i+1}] {user.username}")
                else:
                    print("No users found...")

            case "6":
                username = input("Enter account username to be deleted: ")
                if input(f"Delete user with username {username}[Y/n]? ") == "Y":
                    print("Deleting the user...")
                    user_obj = User.query.filter_by(username=username).first()
                    if not user_obj:
                        print(f"User with username {username} doesn't exist.")
                    else:
                        db.session.delete(user_obj)
                        db.session.commit()
                        print(f"{username} - DELETED")
                else:
                    print("Exiting...")

            case "7":
                username = input("Enter username: ")
                password = input("Enter password: ")

                if len(User.query.filter_by(username=username).all()):
                    print("Username has to be unique.")
                else:
                    new_user = User(username=username, password=password)
                    db.session.add(new_user)
                    db.session.commit()
                    print(f"Created new user successfuly.")

            case "fd":
                populate_fake_data()
