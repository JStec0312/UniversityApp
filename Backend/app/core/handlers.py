# app/core/exception_handlers.py
import logging
from http import HTTPStatus
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# jesli uzywasz python-jose:
try:
    from jose import JWTError, ExpiredSignatureError
except Exception:  # brak libki? pomin
    JWTError = ExpiredSignatureError = tuple()

from app.core.service_errors import AppError

log = logging.getLogger(__name__)

def _problem(request: Request, *, status: int, title: str,
             detail: str, code: str, extra: dict | None = None):
    return {
        "type": f"https://errors.uniaapp/{code.lower()}",
        "title": title,
        "status": status,
        "detail": detail,
        "instance": str(request.url),
        "code": code,
        "trace_id": getattr(request.state, "trace_id", None),
        **(extra or {}),
    }

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        # ostrzegamy, ale bez stack trace (to sa znane bledy domenowe)
        log.warning("AppError %s: %s", getattr(exc, "code", "UNKNOWN"), str(exc),
                    extra={"trace_id": getattr(request.state, "trace_id", None)})
        payload = _problem(
            request,
            status=getattr(exc, "status_code", HTTPStatus.INTERNAL_SERVER_ERROR),
            title=(getattr(exc, "code", "APP_ERROR")).replace("_", " ").title(),
            detail=getattr(exc, "message", str(exc)),
            code=getattr(exc, "code", "APP_ERROR"),
            extra=getattr(exc, "extra", None),
        )
        return JSONResponse(
            status_code=payload["status"],
            content=payload,
            media_type="application/problem+json",
            headers=getattr(exc, "headers", None),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        errors = [
            {
                "loc": ".".join(map(str, e["loc"])),
                "msg": e["msg"],
                "type": e["type"],
            }
            for e in exc.errors()
        ]
        payload = _problem(
            request,
            status=422,
            title="Validation Error",
            detail="The request failed validation.",
            code="VALIDATION_ERROR",
            extra={"errors": errors},
        )
        return JSONResponse(422, payload, media_type="application/problem+json")

    @app.exception_handler(IntegrityError)
    async def integrity_handler(request: Request, exc: IntegrityError):
        log.exception("IntegrityError", extra={"trace_id": getattr(request.state, "trace_id", None)})
        payload = _problem(
            request,
            status=409,
            title="Conflict",
            detail="Resource conflict.",
            code="CONFLICT",
        )
        return JSONResponse(409, payload, media_type="application/problem+json")

    @app.exception_handler(SQLAlchemyError)
    async def sa_handler(request: Request, exc: SQLAlchemyError):
        log.exception("SQLAlchemyError", extra={"trace_id": getattr(request.state, "trace_id", None)})
        payload = _problem(
            request,
            status=500,
            title="Database Error",
            detail="Database operation failed.",
            code="DB_ERROR",
        )
        return JSONResponse(500, payload, media_type="application/problem+json")

    if JWTError:
        @app.exception_handler(JWTError)  # ogolny problem z tokenem
        async def jwt_handler(request: Request, exc: Exception):
            code = "TOKEN_EXPIRED" if isinstance(exc, ExpiredSignatureError) else "INVALID_TOKEN"
            detail = "Token expired." if code == "TOKEN_EXPIRED" else "Invalid token."
            payload = _problem(
                request, status=401, title="Unauthorized", detail=detail, code=code
            )
            # WWW-Authenticate pomaga klientom poprawnie reagowac
            return JSONResponse(
                401, payload, media_type="application/problem+json",
                headers={"WWW-Authenticate": 'Bearer realm="api"'}
            )

    @app.exception_handler(StarletteHTTPException)
    async def http_handler(request: Request, exc: StarletteHTTPException):
        payload = _problem(
            request,
            status=exc.status_code,
            title="HTTP Error",
            detail=str(exc.detail),
            code="HTTP_ERROR",
        )
        return JSONResponse(
            exc.status_code, payload, media_type="application/problem+json",
            headers=getattr(exc, "headers", None)
        )

    @app.exception_handler(Exception)
    async def fallback_handler(request: Request, exc: Exception):
        log.exception("Unhandled exception", extra={"trace_id": getattr(request.state, "trace_id", None)})
        payload = _problem(
            request,
            status=500,
            title="Internal Server Error",
            detail="Something went wrong.",
            code="INTERNAL_ERROR",
        )
        return JSONResponse(500, payload, media_type="application/problem+json")


    