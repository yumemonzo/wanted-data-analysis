from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

# Static files for images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """메인 페이지로 각 버튼을 표시합니다."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/career", response_class=HTMLResponse)
async def show_career(request: Request):
    """경력 분석 이미지를 표시합니다."""
    image_paths = ["/static/images/career.jpg"]
    return templates.TemplateResponse("display_image.html", {"request": request, "image_paths": image_paths, "title": "경력 분석"})

@app.get("/location", response_class=HTMLResponse)
async def show_location_map():
    """위치 분석 HTML 페이지를 직접 반환합니다."""
    return FileResponse("app/location_map.html")

@app.get("/analysis/{section}", response_class=HTMLResponse)
async def show_analysis_section(request: Request, section: str):
    """주요업무, 자격요건, 우대사항의 빈도수 그래프와 워드클라우드 이미지를 표시합니다."""
    if section == "main_job":
        title = "주요업무 분석"
    elif section == "check_list":
        title = "자격요건 분석"
    elif section == "good_list":
        title = "우대사항 분석"
    else:
        return HTMLResponse("잘못된 섹션입니다.", status_code=404)

    bar_graph_path = f"/static/images/{section}_freq_bar_graph.jpg"
    wordcloud_path = f"/static/images/{section}_wordcloud.jpg"
    return templates.TemplateResponse("display_image.html", {
        "request": request, "title": title,
        "image_paths": [bar_graph_path, wordcloud_path]
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
