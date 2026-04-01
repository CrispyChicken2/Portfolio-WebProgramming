from fastapi import FastAPI, Request, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()


class Project(BaseModel):
    name: str
    description: str
    is_published: bool | None = None


projects: list[Project]
projects = []

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def show_home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        context={"projects": projects, "welcome_message": "Bienvenue sur mon ePortfolio !"},
    )


@app.get("/admin", response_class=HTMLResponse)
def show_admin(request: Request):
    return templates.TemplateResponse(
        request,
        "admin.html",
        context={"projects": projects},
    )


@app.get("/projects/{project_id}")
def read_project(project_id: int, detail: int | None = None):
    return {"project_id": project_id, "project": projects[project_id], "detail": detail}


@app.post("/projects")
def create_project(
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    is_published: Annotated[str, Form()],
    admin: Annotated[str, Form()] = None,
):
    if admin != "true":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not admin action",
        )

    project = {
        "name": name,
        "description": description,
        "is_published": True if is_published == "true" else False,
    }

    projects.append(project)

    return RedirectResponse("/admin", status_code=303)


@app.put("/projects/{project_id}")
def update_project(project_id: int, project: Project):
    projects[project_id].update(project.dict())

    response = {"project_name": projects[project_id]["name"], "project_id": project_id}

    return response