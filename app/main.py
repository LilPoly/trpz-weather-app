import sys

from loguru import logger

from app.database.postgres import create_db
from app.models.user import User
from app.uow.uow import UnitOfWork
from app.utils.hash_password import hash_password


def main():
    logger.info("connecting to the database")
    create_db()

    while True:
        print("\n test user menu")
        print("1. Sign up")
        print("2. All users")
        print("0. Exit")

        choice = input("Your choice: ")

        try:
            with UnitOfWork() as uow:
                if choice == "1":
                    email = input("Your email: ")

                    if uow.user.get_by_email(email):
                        print("oops, user with this email already exists")
                        continue

                    name = input("Your name: ")
                    password = input("Your password ")

                    new_user = User(
                        email=email,
                        name=name,
                        password_hash=hash_password(password),
                    )

                    uow.user.add(new_user)

                    uow.commit()
                    logger.info(f"User {name} successfully added")

                elif choice == "2":
                    users = uow.user.get_all()
                    print(f"\n{len(users)} users found in the database:")
                    for u in users:
                        print(f"ID: {u.id} | {u.name} ({u.email}) | Role: {u.role}")

                elif choice == "0":
                    print("bye")
                    sys.exit()

        except Exception as e:
            logger.debug(f"error: {e}")


if __name__ == "__main__":
    main()
