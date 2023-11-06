from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
app = FastAPI()


@app.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "books": "First Book"}
    )

@app.get("/swapped")
async def swapped(request: Request):
    return templates.TemplateResponse(
        "swapped.html", {"request": request, "books": "Swapped Book"}
    )

@app.get("/blog")
async def blog(request: Request):
    return templates.TemplateResponse(
        "blog.html", {"request": request, "books": "Swapped Book"}
    )

@app.get("/blog_switch")
async def blog_switch(request: Request):
    return  'Hello World'

