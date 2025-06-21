from sqlalchemy.orm import Session
from app.models.discount import Discount
from app.repositories.base_repository import BaseRepository
from datetime import date

class DiscountRepository(BaseRepository[Discount]):
    def __init__(self, db: Session):
        super().__init__(db, Discount)

    def get_by_admin_id(self, admin_id: int) -> list[Discount]:
        return self.db.query(self.model).filter(self.model.admin_id == admin_id).all()

    def get_active_discounts(self) -> list[Discount]:
        today = date.today()
        return self.db.query(self.model).filter(
            self.model.valid_until >= today
        ).order_by(self.model.valid_until).all()

    def get_expired_discounts(self) -> list[Discount]:
        today = date.today()
        return self.db.query(self.model).filter(
            self.model.valid_until < today
        ).order_by(self.model.valid_until.desc()).all()
    
