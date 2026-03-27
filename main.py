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
