from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routers import auth, question, answer

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/", tags=["Home"])
async def read_root():
    return {"message": "Welcome to the Procon simulation IUH 🚩"}

@app.get("/", tags=["Home"])
async def healcheck():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(question.router)
app.include_router(answer.router)