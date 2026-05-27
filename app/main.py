from fastapi import FastAPI
from app.api.routes import router
from app.exceptions.handlers import compiler_exception_handler

def create_app() -> FastAPI:
    app = FastAPI(
        title="Custom SQL Compiler API - WebSQL",
        description="Receives custom query parameters and converts them into relational SQL.",
        version="1.0.0"
    )

    # Register the router (routes.py)
    app.include_router(router)

    # Register the global Exception Handler
    # Prevents "Internal Server Error" (500) if the user provides invalid syntax
    app.add_exception_handler(Exception, compiler_exception_handler)

    return app

app = create_app()