from enum import Enum
from fastapi import FastAPI, Query
from mysql.connector import connection
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from data import colors, info_api

from db import Db, Note, db_config

db = Db(db_config)


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# def get_color(color_id : str) -> dict:
#     for color in colors:
#         if (color_id == color["color_id"]):
#             return color
#     return { "error" : "Color not found"}

# def exist_color( color_id : str) -> bool:
#     for color in colors:
#         if color["color_id"] == color_id:
#             return True
#     return False

# def add_color( color : dict ) -> str:
#     colors.append(color)
#     return "Ok"


regexHex = "^(([0-9a-fA-F]{2}){3}|([0-9a-fA-F]){3})$"


@app.get("/")
def get_root():
    return info_api


@app.get("/get/{id}")
def get(id):
    results = db.get(id)
    return {"results": results}


@app.get("/getall")
def get_all():
    results = db.get_all()
    return {"results": results}


class Noote(BaseModel):
    title: str
    content: str
    color: str
    date: str


@app.post("/note")
def put_note(note: Noote):
    n = Note(note.title, note.content, note.color, note.date)
    db.put(n)
    return "Ok!"


@app.delete("/note/{id}")
def delete_note(id):
    message = db.delete(id)
    return message


@app.put("/note/{id}")
def update_note(id, note: Noote):
    db.updateEntire(id, note)
    return "Ok!"


# class Color(BaseModel):
#     color_id : str
#     name : str

# @app.get("/color")
# def get_color_(color_id : str = Query(..., min_length=6, max_length=6, regex = regexHex)):
#     color = get_color(color_id)
#     return { "message" : color }


# @app.get("/colors")
# def get_all_colors():
#     return { "colors" : colors }


# @app.post("/color")
# def create_color(color : Color):
#     if not exist_color( color.color_id ):
#         add_color(color.dict())
#         return { "message" : "Color registered!"}
#     else:
#         return { "message" : "Color already exists" }

# @app.delete("/color")
# def delete_color( color_id : str = Query( ..., max_length=6, min_length=6, regex=regexHex)):
#     if( exist_color(color_id) ):
#         for color in colors:
#             if ( color["color_id"] == color_id ):
#                 colors.remove(color)
#                 return { "message" : "deleted!" }
#     else: return { "message" : "Color doesn't exist" }


# @app.get("/validation/{id}")
# def validation(id : int, name:str = "Carlos", limit : Optional[str] = Query(None, min_length=5)):
#     return { "id" : id, "name" : name, "limit" : limit}


# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name == ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}
