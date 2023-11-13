from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List

app = FastAPI()

class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"

class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType

dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier')
}

@app.get("/dog", response_model=List[Dog])
async def get_dogs(kind: Optional[DogType] = None):
    if kind:
        return [dog for dog in dogs_db.values() if dog.kind == kind]
    return list(dogs_db.values())

@app.post("/dog", response_model=Dog)
async def create_dog(dog: Dog):
    if dog.pk in dogs_db:
        raise HTTPException(status_code=400, detail="Dog with this PK already exists")
    dogs_db[dog.pk] = dog
    return dog

@app.get("/dog/{pk}", response_model=Dog)
async def get_dog_by_pk(pk: int):
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dogs_db[pk]

@app.patch("/dog/{pk}", response_model=Dog)
async def update_dog(pk: int, updated_dog: Dog):
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="Dog not found")
    dogs_db[pk] = updated_dog
    return updated_dog