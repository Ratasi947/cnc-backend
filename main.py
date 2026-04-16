from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase_client import supabase

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Tạm thời cho phép tất cả. Sau này thực tế thì thay bằng link web của Sếp
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        # 1) Kiểm tra ID đã tồn tại chưa
        existing = (
            supabase
            .table("drawings")
            .select("id")
            .eq("id", data.id)
            .execute()
        )

        if existing.data:
            # ID đã tồn tại → trả về thông báo
            return {
                "status": "exists",
                "message": "ID này đã có, bạn muốn Update nó đúng không? Dữ liệu trước đó sẽ bị xóa và thay mới."
            }

        # 2) Nếu chưa tồn tại → insert mới
        result = supabase.table("drawings").insert({
            "id": data.id,
            "filename": data.filename,
            "content": data.content
        }).execute()

        return {"status": "ok", "data": result.data}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# ======================
# UPDATE
# ======================
@app.put("/api/drawings/{drawing_id}")
def update_drawing(drawing_id: str, data: Drawing):
    try:
        # Kiểm tra ID có tồn tại không
        existing = (
            supabase
            .table("drawings")
            .select("id")
            .eq("id", drawing_id)
            .execute()
        )

        if not existing.data:
            return {
                "status": "not_found",
                "message": "ID không tồn tại, không thể update."
            }

        # Update dữ liệu
        result = (
            supabase
            .table("drawings")
            .update({
                "filename": data.filename,
                "content": data.content
            })
            .eq("id", drawing_id)
            .execute()
        )

        return {
            "status": "ok",
            "message": "Update thành công!",
            "data": result.data
        }

    except Exception as e:
        print("🔥 ERROR update_drawing:", str(e))
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

# ======================
# API: LẤY DANH SÁCH SẢN PHẨM BÁN LẺ
# ======================
@app.get("/api/products")
def get_products():
    try:
        # Tương lai: Sếp tạo bảng "products" trên Supabase và dùng dòng dưới:
        # result = supabase.table("products").select("barcode, name, sell_price, category_id").execute()
        # return {"status": "ok", "data": result.data}

        # Hiện tại (Giả lập trả về từ Server để Sếp test thông mạch):
        data_tu_server = [
            { "barcode": '893111', "name": 'Gạo Thơm 5kg (TỪ SERVER)', "price": 120000, "category": 'THỰC PHẨM', "icon": '🌾' },
            { "barcode": '893222', "name": 'Nếp Cái Hoa Vàng (TỪ SERVER)', "price": 45000, "category": 'THỰC PHẨM', "icon": '🍚' },
            { "barcode": '893333', "name": 'Cam Sành (TỪ SERVER)', "price": 35000, "category": 'TRÁI CÂY', "icon": '🍊' },
        ]
        return {"status": "ok", "data": data_tu_server}

    except Exception as e:
        return {"status": "error", "message": str(e)}
