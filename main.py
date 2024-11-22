import uvicorn
from fastapi import FastAPI
from doctor.service import router as center_route
from auth.app import auth_route

app = FastAPI()
# Подключаем маршруты
app.include_router(auth_route)
app.include_router(center_route)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=30000)
