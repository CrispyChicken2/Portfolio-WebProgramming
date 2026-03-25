from fastapi import FastAPI
import pandas as pd

app = FastAPI()


class Identity:
    def __init__(self, name: str, surname: str, age: int):
        self.name = name
        self.surname = surname
        self.age = age


@app.get("/identity")
def read_identity():
    identity = Identity(name="John", surname="Doe", age=30)
    return {"name": identity.name, "surname": identity.surname, "age": identity.age}
