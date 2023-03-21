from fastapi import FastAPI
from router import router


app = FastAPI(
    title="Web scraping API", description="Fastapi + uvicorn", version="0.1.0"
)

app.include_router(router.router)
