from pydantic import BaseModel
from typing import Optional, Any


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[Any]
    trace_id: Optional[str]
