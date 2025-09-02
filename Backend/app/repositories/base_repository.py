"""
Base repository module for database operations.

Uwaga: Repozytoria NIE robią commitów. Commit/rollback ogarnia warstwa serwisu
w transakcji (with session.begin()). Repo robi tylko add/query/flush.
"""

from typing import Generic, Iterable, TypeVar, Type, List, Optional, Dict, Any, Sequence
from sqlalchemy.orm import Session
from sqlalchemy import func

T = TypeVar("T")

class BaseRepository(Generic[T]):
    """
    Generic CRUD + query helpers for SQLAlchemy models.
    """

    def __init__(self, session: Session, model: Type[T]):
        self.session = session          # <- do UoW w serwisie
        self.model: Type[T] = model

    # ---- Reads ----

    def get_by_id(self, id: int, *, for_update: bool = False) -> Optional[T]:
        q = self.session.query(self.model).filter(self.model.id == id)
        if for_update:
            q = q.with_for_update()
        return q.first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        *,
        order_by: Optional[Sequence[Any]] = None,
    ) -> List[T]:
        q = self.session.query(self.model)
        if order_by:
            q = q.order_by(*order_by)
        return q.offset(skip).limit(limit).all()

    def count(self) -> int:
        return self.session.query(func.count(self.model.id)).scalar() or 0

    def filter(self, **kwargs) -> List[T]:
        q = self.session.query(self.model)
        for key, value in kwargs.items():
            q = q.filter(getattr(self.model, key) == value)
        return q.all()

    def get_paginated_with_conditions(
        self,
        conditions: Iterable[Any] = (),
        offset: int = 0,
        limit: int = 100,
        *,
        order_by: Optional[Sequence[Any]] = None,
        for_update: bool = False,
    ) -> List[T]:
        q = self.session.query(self.model).filter(*conditions)
        if order_by:
            q = q.order_by(*order_by)
        if for_update:
            q = q.with_for_update()
        return q.offset(offset).limit(limit).all()

    def count_with_conditions(self, conditions: Iterable[Any] = ()) -> int:
        return self.session.query(func.count(self.model.id)).filter(*conditions).scalar() or 0

    def get_first_with_conditions(
        self,
        conditions: Iterable[Any] = (),
        *,
        for_update: bool = False,
    ) -> Optional[T]:
        q = self.session.query(self.model).filter(*conditions)
        if for_update:
            q = q.with_for_update()
        return q.first()

    def exists_with_conditions(self, conditions: Iterable[Any] = ()) -> bool:
        # Wydajne sprawdzenie istnienia: SELECT EXISTS(SELECT 1 FROM ... WHERE ...)
        inner = self.session.query(self.model).filter(*conditions).exists()
        return self.session.query(inner).scalar() is True

    # ---- Writes (bez commitów) ----

    def create(self, obj: T) -> T:
        self.session.add(obj)
        self.session.flush()       # zapewnia m.in. nadanie ID
        return obj

    def update_by_id(self, id: int, updates: Dict[str, Any]) -> Optional[T]:
        obj = self.get_by_id(id, for_update=True)
        if not obj:
            return None
        for field, value in updates.items():
            setattr(obj, field, value)
        self.session.flush()
        return obj

    def delete_by_id(self, id: int) -> Optional[T]:
        obj = self.get_by_id(id, for_update=True)
        if not obj:
            return None
        self.session.delete(obj)
        self.session.flush()
        return obj
