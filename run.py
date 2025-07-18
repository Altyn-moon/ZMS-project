"""import uvicorn

if __name__ == "__main__":

    uvicorn.run("app.main:app", reload=True)

    uvicorn.run("app.main:app", reload=True)"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run("run:app", host="127.0.0.1", port=8000, reload=True)

import threading
from app.pikalka import start_reader_loop  # путь, если pikalka.py внутри app/

# Запуск RFID-считывателя в фоне
threading.Thread(target=start_reader_loop, daemon=True).start()

