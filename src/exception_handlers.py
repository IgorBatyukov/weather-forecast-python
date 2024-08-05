from enum import StrEnum
from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse

from src.models import HttpErrorResponse


class ErrorMessages(StrEnum):
    WEATHER_FILES_NOT_FOUND = 'WEATHER_FILES_NOT_FOUND'
    ERROR_PARSING_DATA = 'ERROR_PARSING_DATA'


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    response = JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=HttpErrorResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=HTTPStatus.INTERNAL_SERVER_ERROR.name
        ).dict()
    )
    return response
