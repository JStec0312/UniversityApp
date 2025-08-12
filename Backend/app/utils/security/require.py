# app/security/require_shortcuts.py
from fastapi import Depends
from app.utils.role_enum import RoleEnum
from app.utils.security.require_roles import require_roles  # <- twoja funkcja

class _Require:
    def roles(self, *roles: str):
        """Dowolna z podanych ról."""
        return Depends(require_roles(list(roles)))

    # predefy – krótko i czytelnie
    @property
    def student(self):
        return Depends(require_roles([RoleEnum.STUDENT.value]))

    @property
    def admin(self):
        return Depends(require_roles([RoleEnum.ADMIN.value]))

    @property
    def superior(self):
        return Depends(require_roles([RoleEnum.SUPERIOR_ADMIN.value]))

    @property
    def admin_or_superior(self):
        return Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.SUPERIOR_ADMIN.value]))

    @property
    def all(self):
        return Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.SUPERIOR_ADMIN.value, RoleEnum.STUDENT.value]))
    

require = _Require()
