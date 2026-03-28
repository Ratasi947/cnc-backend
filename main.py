from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from supabase_client import supabase

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


# ======================
# MODEL
# ======================
class Drawing(BaseModel):
    id: str
    filename: str
    content: str


# ======================
# SAVE DRAWING
# ======================
@app.post("/api/save_drawing")
def save_drawing(data: Drawing):
    try:
        print("👉 DATA RECEIVED:", data)

        result = supabase.table("drawings").insert({
            "id": data.id,
            "filename": data.filename,
            "content": data.content
        }).execute()

        print("✅ INSERT RESULT:", result)

        return {"status": "ok", "data": result.data}

    except Exception as e:
        print("🔥 ERROR save_drawing:", str(e))
        return {"status": "error", "message": str(e)}


# ======================
# GET ALL
# ======================
@app.get("/api/drawings")
def get_drawings():
    try:
        result = supabase.table("drawings").select("*").execute()
        print("✅ GET ALL:", result)
        return {"status": "ok", "data": result.data}

    except Exception as e:
        print("🔥 ERROR get_drawings:", str(e))
        return {"status": "error", "message": str(e)}


# ======================
# GET BY ID
# ======================
@app.get("/api/drawings/{drawing_id}")
def get_drawing(drawing_id: str):
    try:
        result = (
            supabase
            .table("drawings")
            .select("*")
            .eq("id", drawing_id)
            .single()
            .execute()
        )

        print("✅ GET ONE:", result)

        return {"status": "ok", "data": result.data}

    except Exception as e:
        print("🔥 ERROR get_drawing:", str(e))
        return {"status": "error", "message": str(e)}


# ======================
# DELETE
# ======================
@app.delete("/api/drawings/{drawing_id}")
def delete_drawing(drawing_id: str):
    try:
        result = (
            supabase
            .table("drawings")
            .delete()
            .eq("id", drawing_id)
            .execute()
        )

        print("✅ DELETE:", result)

        return {"status": "ok", "data": result.data}

    except Exception as e:
        print("🔥 ERROR delete_drawing:", str(e))
        return {"status": "error", "message": str(e)}
