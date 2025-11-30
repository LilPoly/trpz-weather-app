import getpass
import sys

from loguru import logger

from app.core.context import SecurityContext
from app.database.postgres import create_db
from app.models.user import RoleEnum
from app.schemas.user import UserCreate, UserLogin
from app.services.admin import AdminService
from app.services.weather import WeatherService


def main():
    logger.info("connecting to database...")
    create_db()
    logger.info("system is ready!")

    user_service = AdminService()
    weather_service = WeatherService()

    while True:
        current_user = SecurityContext.get_user()
        user_label = current_user.name if current_user else "Guest"

        role_label = f"[{current_user.role}]" if current_user else ""

        print("\n=================================")
        print(f"WEATHER APP CLI | User: {user_label} {role_label}")
        print("=================================")

        if not current_user:
            print("1. Sign Up")
            print("2. Sign In")
        else:
            print("3. Get the weather")
            print("4. History")
            print("5. Logout")

            if current_user.role == RoleEnum.ADMIN:
                print("6. Delete User (Admin Only)")

        print("0. Exit")

        choice = input(">>> Your choice: ")

        try:
            if choice == "1":
                print("\n--- Sign Up ---")
                email = input("Email: ")
                name = input("Name: ")
                password = getpass.getpass("Password: ")

                user_create = UserCreate(email=email, name=name, password=password)

                user_service.register(user_create)
                logger.info("User is successfully registered")

            elif choice == "2":
                print("\n--- Sign In ---")
                email = input("Email: ")
                password = getpass.getpass("Password: ")

                user_login = UserLogin(email=email, password=password)

                user = user_service.login(user_login)
                if user:
                    print(f"Hey, {user.name}!")

            elif choice == "3":
                print("\n--- Get The Weather ---")
                city = input("Your location: ")

                weather = weather_service.update_weather_for_city(city)

                print(f"\nWeather in {weather.location}:")
                print(f"Temperature: {weather.temperature}°C")
                print(f"Humidity: {weather.humidity}%")
                print(f"Wind Speed: {weather.wind_speed} m/s")
                print("We've saved it to our database.")

            elif choice == "4":
                print("\n--- DATA ANALYSIS ---")
                city = input("Your city: ")

                print("\nChoose an option:")
                print("1. Last saved record")
                print("2. Temperature graph (last 3 days)")

                sub_choice = input(">>> ")

                if sub_choice == "1":
                    weather = weather_service.get_weather_history(city)
                    if weather:
                        print(
                            f"Last record: {weather.temperature}°C ({weather.created_at})"
                        )
                    else:
                        print("No data in database.")

                elif sub_choice == "2":
                    try:
                        weather_service.show_temperature_chart(city, days=3)
                    except Exception as e:
                        print(f"Error while building a graph: {e}")

                else:
                    print("Invalid option.")

            elif choice == "5":
                SecurityContext.clear()
                print("You're logged out")

            elif choice == "6":
                if not current_user or current_user.role != RoleEnum.ADMIN:
                    print("You don't have permission!")
                    continue

                print("\n--- ADMIN PANEL: DELETE USER ---")
                print("Find user by email to retrieve ID.")

                target_email = input("Enter user's email: ")

                target_user = user_service.get_user_info_by_email(target_email)

                if target_user:
                    print("\nUser Found:")
                    print(f"   ID: {target_user.id}")
                    print(f"   Name: {target_user.name}")
                    print(f"   Email: {target_user.email}")
                    print(f"   Role: {target_user.role}")

                    confirm = input(
                        f"\nAre you sure you want to DELETE {target_user.name}? (y/n): "
                    )

                    if confirm.lower() == "y":
                        user_service.delete_user(target_user.id)
                        print(f"User '{target_user.name}' was deleted.")
                    else:
                        print("Operation cancelled.")
                else:
                    print("User with this email not found.")

            elif choice == "0":
                print("Ok, bye")
                sys.exit()

            else:
                print("What? I don't know this choice.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
