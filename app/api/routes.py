import urllib.parse
from fastapi import APIRouter, Request
from app.schemas.responses import SuccessResponse
from app.services.compiler_service import CompilerService

router = APIRouter()

@router.get("/sql/{full_path:path}", response_model=SuccessResponse)
async def compile_query(request: Request, full_path: str):
    """
    Catch-all endpoint that captures everything after the root '/'.
    """
    # 1. Reconstructing the original raw URL (path + query params)
    query_string = request.url.query
    raw_input = f"/{full_path}"
    
    if query_string:
        decoded_query = urllib.parse.unquote(query_string)
        raw_input += f"?{decoded_query}"
        
    # 2. Call the service that orchestrates the compiler
    result = CompilerService.compile_url_to_sql(raw_input)
    
    # 3. Return using the standardized schema
    return SuccessResponse(
        input_query=raw_input,
        sql=result["sql"],
        recognized_tables=result["recognized_tables"]
    )