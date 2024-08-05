import uvicorn
from fastapi import FastAPI


from src.utils import calculate_forecast
from src.exception_handlers import general_exception_handler


app = FastAPI()
app.add_exception_handler(Exception, general_exception_handler)


@app.get('/')
async def health_check():
    return {'healthy': True}


@app.get('/getForecast')
async def get_forecast(from_ts: int, to_ts: int, lat: int, long: int):
    forecast = await calculate_forecast(from_ts, to_ts, long, lat)
    return forecast


if __name__ == '__main__':
    try:
        uvicorn.run('main:app', host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        pass
