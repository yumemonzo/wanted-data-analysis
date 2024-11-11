# main.py
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
async def display_map():
    # Folium에서 생성한 HTML 파일 경로
    return FileResponse("location_map.html")
