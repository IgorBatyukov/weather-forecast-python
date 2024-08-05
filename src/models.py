from pydantic import BaseModel


class HttpErrorResponse(BaseModel):
    detail: str
    status_code: int
