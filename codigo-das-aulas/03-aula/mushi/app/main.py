from fastapi import FastAPI
from app.routers.anime import router
app = FastAPI()

app.include_router(router=router)
