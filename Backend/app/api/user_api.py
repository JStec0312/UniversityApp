# app/api/user_api.py
from urllib import response
from fastapi import APIRouter, Depends, Query, HTTPException, BackgroundTasks, Response, Request
from sqlalchemy.orm import Session
from app.exceptions.service_errors import EmailAlreadyExistsException, ServerErrorException, UserAlreadyVerifiedException, UserNotFoundException, UserNotVerifiedException, InvalidCredentialsException
from app.core.db import get_db
from app.schemas.student import StudentVerificationIn
from app.schemas.user import UserCreate, UserOut, EmailOut, UserAuthIn, UserAuthOut
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory
from app.utils.security.require import require
from app.utils.send_verification_mail import send_verification_email
from app.utils.role_enum import RoleEnum
from app.utils.security.jwt_tokens import create_access_token
import os
router = APIRouter()

SECURE = os.getenv("SECURE_COOKIES", "false").lower() == "true"   # dev: False, prod: True
SAMESITE = os.getenv("COOKIE_SAMESITE", "lax")                    # prod (inne domeny): "none"
COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN")                        # zwykle None
TTL = int(os.getenv("ACCESS_TTL", "3600"))

@router.post("/", response_model=UserOut, status_code=201)
def create_user(user_in: UserCreate, response: Response, request: Request, background: BackgroundTasks,  db: Session = Depends(get_db)):
    user_repo = RepositoryFactory(db).get_user_repository()
    user_service = ServiceFactory.get_user_service(user_repo)
    try:
        new_user = user_service.create_user(user_in)
    except EmailAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ServerErrorException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    token = user_service.issue_verification_token(new_user.id)
    background.add_task(
        send_verification_email,
        to_email=new_user.email,
        to_user=new_user.display_name,
        verification_token=token,
        university_id=new_user.university_id,
    )
    response.headers["Location"] = str(request.url_for("get_user", user_id=new_user.id))
    return new_user


@router.post("/token/{user_id}")
def resend_verification_token(user_id: int, background: BackgroundTasks, request:Request, db: Session = Depends(get_db)):
    user_repo = RepositoryFactory(db).get_user_repository()
    user_service = ServiceFactory.get_user_service(user_repo)
    try:
        token, to_email, to_user, user_university_id = user_service.prepare_verification_token(user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserAlreadyVerifiedException as e:
        raise HTTPException(status_code=409, detail=str(e))
    
    background.add_task(
        send_verification_email,
        to_email=to_email,
        to_user=to_user,
        verification_token=token,
        university_id=user_university_id,
    )
    return {"status": "queued"}

@router.get("/email", response_model=EmailOut, status_code=200)
def get_user_email(db: Session = Depends(get_db), user = require.all):
    user_repo = RepositoryFactory(db).get_user_repository()
    user_service = ServiceFactory.get_user_service(user_repo)
    try:
        email = user_service.get_user_email(user["user_id"])
        return EmailOut(email=email)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.get("/search", response_model=list[UserOut])
def search_users (
    db: Session = Depends(get_db),
    user: dict = require.all,
    name: str = Query(..., min_length=1, max_length=100),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    user_repo = RepositoryFactory(db).get_user_repository()
    user_service = ServiceFactory.get_user_service(user_repo)
    return user_service.search_users(name=name, university_id=user["university_id"], limit=limit, offset=offset)

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, user = require.all, db: Session = Depends(get_db)):
    user_repo = RepositoryFactory(db).get_user_repository()
    user_service = ServiceFactory.get_user_service(user_repo)
    try:
        user = user_service.get_user_by_id(user_id=user_id, university_id=user["university_id"])
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return UserOut(id=user.id, display_name=user.display_name, avatar_image_url=user.avatar_image_url)


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}


@router.post("/login", response_model=UserAuthOut)
def login(user_in: UserAuthIn, response: Response, db: Session = Depends(get_db)):
    user_repo = RepositoryFactory(db).get_user_repository()
    user_service = ServiceFactory.get_user_service(user_repo)
    try:
        user, roles = user_service.authenticate_user(user_in)
    except UserNotFoundException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except UserNotVerifiedException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    token = create_access_token(
        user_id=user.id,
        university_id=user.university_id,
        roles=roles,
        ttl_sec=3600
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=SECURE,          # prod: True
        samesite=SAMESITE,      # prod (inne domeny): "none"
        path="/",
        max_age=TTL,
        domain=COOKIE_DOMAIN,   # zwykle None
    )

    return UserAuthOut(
        id=user.id,
        display_name=user.display_name,
        roles=roles,
        university_id=user.university_id,
        avatar_image_url=user.avatar_image_url
    )

