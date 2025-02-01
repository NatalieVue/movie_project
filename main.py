from typing import Union
import sqlalchemy
from fastapi import FastAPI
from process_data import access_tables
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('_mpl-gallery')

# make data:
x = 0.5 + np.arange(8)
y = [4.8, 5.5, 3.5, 4.6, 6.5, 6.6, 2.6, 3.0]

# plot
fig, ax = plt.subplots()

ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)

ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))

plt.show()

app = FastAPI()

# SQL Alchemy or Pydantic but prob SqlAlchemy

data = access_tables()
print("all movies", data)

@app.get("/")
def read_root():
    # Instead of this message return Lion King movies
    data = access_tables()
    print("all movies", data)
    return {"message": f"Iz bitc, leave our World {data[0]}"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/leave")
def read_root():
    return {"message": "Bye Iz"}
