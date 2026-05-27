from fastapi import Request
from fastapi.responses import JSONResponse
from app.schemas.responses import ErrorResponse

async def compiler_exception_handler(request: Request, exc: Exception):
    """
    Catches global exceptions (from the compiler logic) and converts them to HTTP 400 Bad Request.
    """
    response = ErrorResponse(
        message="Compilation Error",
        details=str(exc)
    )
    return JSONResponse(
        status_code=400,
        content=response.model_dump()
    )