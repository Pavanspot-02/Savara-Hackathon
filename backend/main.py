from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import init_db
from app.routers import auth_router, notes_router, quiz_router, peers_router, dashboard_router

app = FastAPI(title="LearnSync API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()
    print("[DB] Database initialized.")

app.include_router(auth_router.router)
app.include_router(notes_router.router)
app.include_router(quiz_router.router)
app.include_router(peers_router.router)
app.include_router(dashboard_router.router)

@app.get("/")
def root():
    return {"app": "LearnSync", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}