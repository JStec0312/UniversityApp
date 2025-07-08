from datetime import datetime
from app.schemas.group_register_password import GroupRegisterPasswordCreate, GroupRegisterPasswordOut
from app.models.group_register_password import GroupRegisterPassword
from app.repositories.group_register_password_repository import GroupRegisterPasswordRepository
class GroupRegisterPasswordService:
    def __init__(self, group_register_password_repo: GroupRegisterPasswordRepository):
        self.group_register_password_repo = group_register_password_repo

    def create_group_register_password(self,  data: GroupRegisterPasswordCreate, given_by: int) -> None:
        import uuid
        group_register_password = GroupRegisterPassword(
            token=str(uuid.uuid4()),
            group_id=data.group_id,
            given_by=given_by,
            expires_at=data.expires_at
        )
        new_password_record = self.group_register_password_repo.create(group_register_password)
        return GroupRegisterPasswordOut(
            token = new_password_record.token,
            group_id= new_password_record.group_id,
            expires_at = new_password_record.expires_at
        )
    
        
    