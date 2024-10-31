from fastapi import FastAPI
import uvicorn
from routers.continuos import continuosRouter
from routers.discrete import discreteRouter

app = FastAPI()
app.include_router(discreteRouter)
app.include_router(continuosRouter)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
