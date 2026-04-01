from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel

app = FastAPI()
file = pd.read_csv("data.csv")


class Identity(BaseModel):
    name : str
    surname : str
    age : int

@app.get("/data")
def get_data():
    return file.to_dict(orient="records")

@app.get("/identity")
def read_identity():
    identity = Identity(name="John", surname="Doe", age=30)
    return {identity}