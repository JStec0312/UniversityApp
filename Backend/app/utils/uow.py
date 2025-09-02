# app/services/uow.py
from contextlib import contextmanager
from sqlalchemy.orm import Session

@contextmanager
def uow(session: Session):
    
    if session.in_transaction():
        with session.begin_nested():
            yield
    else:
        with session.begin():
            yield
