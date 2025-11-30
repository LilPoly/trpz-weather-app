from app.core.context import SecurityContext
from app.models.user import RoleEnum
from app.schemas.user import UserDTO
from app.services.user import UserService
from app.uow.uow import UnitOfWork


class AdminService(UserService):
    def get_user_info_by_email(self, email: str) -> UserDTO:
        current_user = SecurityContext.get_user()
        if not current_user or current_user.role != RoleEnum.ADMIN:
            raise PermissionError("Only the administrator can search for users!")

        with UnitOfWork() as uow:
            user = uow.user.get_by_email(email)

            if user:
                return UserDTO.model_validate(user)
            return None

    def delete_user(self, user_id: int) -> bool:
        current_user = SecurityContext.get_user()

        if not current_user or current_user.role != RoleEnum.ADMIN:
            raise PermissionError("Only the administrator can delete users!")

        if current_user.id == user_id:
            raise ValueError("You cannot delete your own account!")

        with UnitOfWork() as uow:
            user_to_delete = uow.user.get_by_id(user_id)
            if not user_to_delete:
                raise ValueError(f"User with ID {user_id} now found.")

            uow.user.delete(user_id)
            uow.commit()
            return True
