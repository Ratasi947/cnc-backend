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

@app.post("/api/save_drawing")
def save_drawing(filename: str, content: str):
    data = {
        "filename": filename,
        "content": content
    }
    result = supabase.table("drawings").insert(data).execute()
    return {"status": "ok", "data": result.data}
