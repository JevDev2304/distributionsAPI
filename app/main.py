from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers.continuos import continuosRouter
from routers.discrete import discreteRouter

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://distributions-rouge.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE, etc.).
    allow_headers=["*"],  # Permitir todos los headers.
)

app.include_router(discreteRouter)
app.include_router(continuosRouter)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Cambiado a 0.0.0.0
