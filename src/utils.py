import os
import struct
from http import HTTPStatus
from pathlib import Path

import aiofiles

from src.exception_handlers import ErrorMessages


def get_offset(header: tuple, x: int, y: int) -> int:
    min_x = header[2]
    max_x = header[3]
    min_y = header[0]
    step_x = header[5]
    step_y = header[4]
    max_steps_x = (abs(min_x) + abs(max_x)) // step_x + 1
    matrix_x = round(abs(x - min_x) / step_x)
    matrix_y = round(abs(y - min_y) / step_y)
    return ((matrix_y * max_steps_x) + matrix_x) * 4 + 32


def get_ts(file_name: str) -> int:
    return int(file_name.split('.')[0])


async def get_temp_from_snapshot(file_path: Path, x: int, y: int) -> float:
    async with aiofiles.open(file_path, 'rb') as f:
        header_bin = await f.read(8 * 4)
        header = struct.unpack('7if', header_bin)
        offset = get_offset(header, x, y)
        await f.seek(offset)
        temp_bin = await f.read(4)
    return struct.unpack('1f', temp_bin)[0]


async def calculate_forecast(from_ts: int, to_ts: int, x: int, y: int) -> dict:
    current_dir = Path(__file__).resolve().parent
    bucket_path = current_dir.parent.joinpath('data')
    response = {}
    for file_name in os.listdir(bucket_path):
        current_ts = get_ts(file_name)
        if from_ts <= current_ts <= to_ts:
            file_path = bucket_path.joinpath(file_name)
            try:
                temp = await get_temp_from_snapshot(file_path, x, y)
                response[current_ts] = {'temp': temp}
            except Exception as exc:
                raise Exception(HTTPStatus.INTERNAL_SERVER_ERROR, ErrorMessages.ERROR_PARSING_DATA) from exc
    return response
