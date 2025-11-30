from app.core.context import SecurityContext
from app.models.user import User
from app.schemas.user import UserCreate, UserDTO, UserLogin
from app.uow.uow import UnitOfWork
from app.utils.hash_password import hash_password, verify_password


class UserService:
    def register(self, user_data: UserCreate) -> UserDTO:
        with UnitOfWork() as uow:
            if uow.user.get_by_email(user_data.email):
                raise ValueError(
                    f"sorry, we already have {user_data.email} in our database"
                )

            hashed_pwd = hash_password(user_data.password)
            new_user = User(
                name=user_data.name, email=user_data.email, password_hash=hashed_pwd
            )

            uow.user.add(new_user)
            uow.commit()

            return UserDTO.model_validate(new_user)

    def login(self, login_data: UserLogin) -> UserDTO:
        with UnitOfWork() as uow:
            user = uow.user.get_by_email(login_data.email)
            if not user:
                raise ValueError(
                    f"we can't find user with this email. here's yout email {login_data.email}, please check again"
                )

            if not verify_password(login_data.password, user.password_hash):
                raise ValueError("ooops, incorrect password")

            user_dto = UserDTO.model_validate(user)

            SecurityContext.set_user(user_dto)

            return user_dto
