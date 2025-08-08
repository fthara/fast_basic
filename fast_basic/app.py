from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_basic.routers import auth, users
from fast_basic.schemas import Message

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/ola-mundo', response_class=HTMLResponse)
def ola_mundo():
    return """
    <html>
        <head>
            <title>Olá Mundo</title>
        </head>
        <body>
            <h1>Olá Mundo!</h1>
        </body>
    </html>
    """
