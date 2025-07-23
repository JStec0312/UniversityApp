from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory

