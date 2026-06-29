from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import router
from app.exceptions.handlers import compiler_exception_handler
from app.database.connection import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Roda antes do servidor começar a aceitar requisições
    create_db_and_tables()
    yield

def create_app() -> FastAPI:
    app = FastAPI(
        title="Custom SQL Compiler API - WebSQL",
        description="Receives custom query parameters and converts them into relational SQL.",
        version="1.0.0",
        lifespan=lifespan
    )

    app.include_router(router)

    app.add_exception_handler(Exception, compiler_exception_handler)

    return app

app = create_app()