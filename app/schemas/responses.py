from pydantic import BaseModel
from typing import List, Optional

class SuccessResponse(BaseModel):
    status: str = "success"
    input_query: str
    sql: str
    recognized_tables: List[str]
    result: List[dict]
    is_correct: Optional[bool] = None

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    details: Optional[str] = None