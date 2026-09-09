from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import connect_to_mongo, close_mongo_connection
from app.routes import router as books_router
@asynccontextmanager
async def lifespan(app: FastAPI):
await connect_to_mongo()
yield
await close_mongo_connection()
app = FastAPI(
title="Book Library API",
description="Asynchronous CRUD API for managing books with FastAPI and MongoDB Atlas",
version="1.0.0",
lifespan=lifespan
)
app.include_router(books_router)
@app.get("/health", tags=["Health"])
async def health_check():
return {"status": "ok"}
