import urllib.parse
from fastapi import APIRouter, Request, Depends, Header
from sqlmodel import Session
from app.schemas.responses import SuccessResponse
from app.services.compiler_service import CompilerService
from app.database.connection import get_session

router = APIRouter()

@router.get("/exercicio/{exercise_num}/{full_path:path}", response_model=SuccessResponse, tags=["Exercicios"])
async def compile_query(
    request: Request,
    full_path: str,
    x_user_name: str = Header(None, description="Nome do usuário"),
    x_user_email: str = Header(None, description="Email do usuário"),
    exercise_num: int = None,
    session: Session = Depends(get_session)
):
    
    # 1. Reconstructing the original raw URL (path + query params)
    full_path_decoded = urllib.parse.unquote(full_path)
    raw_input = f"/{full_path_decoded}"
    query_string = request.url.query
    
    if query_string:
        decoded_query = urllib.parse.unquote(query_string)
        if decoded_query not in raw_input:
            raw_input += f"&{decoded_query}" if "?" in raw_input else f"?{decoded_query}"
        
    # 2. Call the service that orchestrates the compiler
    result = CompilerService.compile_url_and_execute(
        raw_input,
        session,
        user_name=x_user_name,
        user_email=x_user_email,
        exercise_num=exercise_num
    )
    
    # 3. Return using the standardized schema
    return SuccessResponse(
        input_query=raw_input,
        sql=result["sql"],
        recognized_tables=result["recognized_tables"],
        result=result["result"],
        is_correct=result["is_correct"]
    )

@router.get("/sandbox/{full_path:path}", response_model=SuccessResponse, tags=["Teste livre"])
async def compile_sandbox(
    request: Request, 
    full_path: str, 
    session: Session = Depends(get_session)
):
    """Compilador livre para testes soltos da sintaxe."""
    if full_path == "favicon.ico":
        from fastapi.responses import Response
        return Response(status_code=204)

    # Decodifica URL e Query Params
    full_path_decoded = urllib.parse.unquote(full_path)
    raw_input = f"/{full_path_decoded}"
    
    query_string = request.url.query
    if query_string:
        decoded_query = urllib.parse.unquote(query_string)
        if decoded_query not in raw_input:
            raw_input += f"&{decoded_query}" if "?" in raw_input else f"?{decoded_query}"
        
    # Executa sem passar os dados de usuário (não salva no banco)
    result = CompilerService.compile_url_and_execute(raw_input=raw_input, session=session)
    
    return SuccessResponse(
        input_query=raw_input,
        sql=result["sql"],
        recognized_tables=result["recognized_tables"],
        result=result["result"] 
    )