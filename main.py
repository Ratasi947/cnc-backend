from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve thư mục web (chứa HTML)
app.mount("/web", StaticFiles(directory="web"), name="web")

# Trang chủ → trả về index.html
@app.get("/")
def home():
    return FileResponse("web/index.html")

# API mẫu
@app.get("/api/hello")
def hello():
    return {"message": "FastAPI đã chạy thành công!"}

from supabase_client import supabase

from pydantic import BaseModel

class Drawing(BaseModel):
    filename: str
    content: str

@app.post("/api/save_drawing")
def save_drawing(data: Drawing):
    result = supabase.table("drawings").insert({
        "filename": data.filename,
        "content": data.content
    }).execute()
    return {"status": "ok", "data": result.data}
