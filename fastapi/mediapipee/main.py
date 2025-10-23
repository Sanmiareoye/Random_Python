from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from enum import IntEnum
from typing import List, Optional
from pydantic import BaseModel, Field
from pathlib import Path
import os
from random import randint

api = FastAPI()


class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1


class TodoBase(BaseModel):
    todo_name: str = Field(
        ..., min_length=3, max_length=512, description="Name of the todo"
    )
    todo_description: str = Field(..., description="Description of todo")
    priority: Priority = Field(
        default=Priority.LOW, description="Priority of the todo."
    )


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    todo_id: int = Field(default=None, description="Unique identifier of the todo")


class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(
        default=None, min_length=3, max_length=512, description="Name of the todo"
    )

    todo_description: Optional[str] = Field(
        default=None, description="Description of todo"
    )

    priority: Optional[Priority] = Field(
        default=Priority.LOW, description="Priority of the todo."
    )


all_todos = [
    Todo(
        todo_id=1,
        todo_name="Sports",
        todo_description="Go to the gym",
        priority=Priority.HIGH,
    ),
    Todo(
        todo_id=2,
        todo_name="Read",
        todo_description="Read 10 pages",
        priority=Priority.LOW,
    ),
    Todo(
        todo_id=3,
        todo_name="Shop",
        todo_description="Go shopping",
        priority=Priority.MEDIUM,
    ),
    Todo(
        todo_id=4,
        todo_name="Study",
        todo_description="Study for exam",
        priority=Priority.LOW,
    ),
    Todo(
        todo_id=5,
        todo_name="Mediate",
        todo_description="Meditate for 20 minutes",
        priority=Priority.MEDIUM,
    ),
]


# GET, POST, PUT, DELETE
@api.get("/")
async def get_image():
    image_path = Path("1.jpg")
    if not image_path.is_file():
        return {"error": "Image not found on the server"}

    return FileResponse(image_path)


from fastapi.staticfiles import StaticFiles

api.mount("/images", StaticFiles(directory="images"), name="images")

IMAGEDIR = "./images/"  # Ensure folder exists


@api.post("/upload/")
async def upload_file(file: UploadFile):
    try:
        # Use the original filename

        contents = await file.read()

        with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
            f.write(contents)

        return {"filename": file.filename}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@api.get("/show/")
async def read_random_file():

    # get random file from the image directory
    files = os.listdir(IMAGEDIR)
    random_index = randint(0, len(files) - 1)

    path = f"{IMAGEDIR}{files[random_index]}"

    return FileResponse(path)


# path parameter is when its in the you provide it in the pat
# for e.g localhost:9999/todos/2
@api.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


# query paramter is -> localhost:9999/todos?first_n=3?
# if you dont specidy it in the url itll make it a query parameter
# specify type in argument
@api.get("/todos", response_model=List[Todo])
def get_todos(first_n: int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos


@api.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todos) + 1

    new_todo = Todo(
        todo_id=new_todo_id,
        todo_name=todo.todo_name,
        todo_description=todo.todo_description,
        priority=todo.priority,
    )
    all_todos.append(new_todo)

    return new_todo


@api.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            if updated_todo.todo_name is not None:
                todo.todo_name = updated_todo.todo_name
            if updated_todo.todo_description is not None:
                todo.todo_description = updated_todo.todo_description
            if updated_todo.priority is not None:
                todo.priority = updated_todo.priority
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@api.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            delete_todo = all_todos.pop(index)
            return delete_todo
    raise HTTPException(status_code=404, detail="Todo not found")
