from app.repositories.base_repository import BaseRepository
from app.models.group_register_password import GroupRegisterPassword
from datetime import datetime
class GroupRegisterPasswordRepository(BaseRepository[GroupRegisterPassword]):
    def __init__(self, db):
        super().__init__(db, GroupRegisterPassword)

    def get_by_token(self, token: str) -> GroupRegisterPassword | None:
        return self.db.query(self.model).filter(
            self.model.token == token
        ).first()


    def set_expired(self, token: str) -> None:
        group_register_password = self.get_by_token(token)
        if group_register_password:
            group_register_password.expires_at = datetime.now()
            self.db.commit()

    