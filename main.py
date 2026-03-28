from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from supabase_client import supabase
import os

app = FastAPI()

# Serve thư mục web
app.mount("/web", StaticFiles(directory="web"), name="web")


# ======================
# HOME
# ======================
@app.get("/")
def home():
    return FileResponse("web/index.html")


# ======================
# TEST API
# ======================
@app.get("/api/hello")
def hello():
    return {"message": "FastAPI đã chạy thành công!"}


# ======================
# DEBUG ENV
# ======================
@app.get("/api/debug")
def debug():
    return {
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_KEY_exists": os.getenv("SUPABASE_KEY") is not None
    }


# ======================
# MODEL
# ======================
class Drawing(BaseModel):
    filename: str
    content: str


# ======================
# SAVE DRAWING
# ======================
@app.post("/api/save_drawing")
def save_drawing(data: Drawing):
    try:
        # kiểm tra dữ liệu đầu vào
        if not data.filename or not data.content:
            return {
                "status": "error",
                "message": "Thiếu filename hoặc content"
            }

        # insert vào supabase
        result = supabase.table("drawings").insert({
            "filename": data.filename,
            "content": data.content
        }).execute()

        return {
            "status": "ok",
            "data": result.data
        }

    except Exception as e:
        # log ra console (Render sẽ hiển thị)
        print("🔥 ERROR save_drawing:", str(e))

        return {
            "status": "error",
            "message": str(e)
        }
