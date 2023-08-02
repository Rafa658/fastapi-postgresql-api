from fastapi import FastAPI
from pydantic import BaseModel
from api.todos.router import router as todos_router
from api.auth.router import router as auth_router

class Tarefa(BaseModel):
    titulo: str
    desc: str
    status: str

app = FastAPI()

@app.get("/")
async def root():
    return "API Mention"

app.include_router(todos_router, prefix="/todos", tags=["todos"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)