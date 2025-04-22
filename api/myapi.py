from fastapi import FastAPI,HTTPException
from typing import List
from pydantic import BaseModel


app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Hello, FastAPI!"}


class Item(BaseModel):
    name: str
    quantity: int
    price: float

# class ItemWithID(Item):
#     id: int



inventory = {}
item_counter = 1



@app.post("/items/", response_model=Item)
def add_item(item: Item):
    global item_counter
    inventory[item_counter] = item
    item_counter = item_counter + 1
    return item





@app.get("/items/", response_model=List[Item])
def get_all_items():
    return list(inventory.values())



@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    item = inventory.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item



@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    inventory[item_id] = updated_item
    return updated_item



@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    del inventory[item_id]
    return {"message": "Item deleted successfully"}
