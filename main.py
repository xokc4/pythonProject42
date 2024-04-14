from datetime import datetime

import app
from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import create_engine
import aiosqlite


DATABASE_URL = "sqlite:///mydatabase.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
app = FastAPI()

users = sqlalchemy.Table(
"users",
metadata,
sqlalchemy.Column("id", sqlalchemy.Integer,
primary_key=True),
sqlalchemy.Column("password", sqlalchemy.String(32)),
sqlalchemy.Column("email", sqlalchemy.String(32)),
sqlalchemy.Column("first_name", sqlalchemy.String(32)),
sqlalchemy.Column("last_name", sqlalchemy.String(128)),
)
products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(128)),
    sqlalchemy.Column("description", sqlalchemy.String(256)),
    sqlalchemy.Column("price", sqlalchemy.Float),
)
orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id")),
    sqlalchemy.Column("order_date", sqlalchemy.DateTime),
    sqlalchemy.Column("status", sqlalchemy.String(50))
)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)
class OrderIn(BaseModel):
    user_id: int
    product_id: int
    order_date: datetime
    status: str

class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: datetime
    status: str
class ProductIn(BaseModel):
    name: str = Field(max_length=128)
    description: str = Field(max_length=256)
    price: float
class Product(BaseModel):
    id: int
    name: str = Field(max_length=128)
    description: str = Field(max_length=256)
    price: float
class UserIn(BaseModel):
    password:str = Field(max_length=32)
    email:str = Field(max_length=32)
    first_name : str = Field(max_length=32)
    last_name : str = Field(max_length=128)
class User(BaseModel):
    id: int
    password:str = Field(max_length=32)
    email:str = Field(max_length=32)
    first_name : str = Field(max_length=32)
    last_name : str = Field(max_length=128)
@app.post("/order/", response_model=Order)
async def create_orders(order: OrderIn):
    query = orders.insert().values(user_id=order.user_id,
                                     product_id=order.product_id,
                                     order_date=order.order_date,
                                   status=order.status)
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}


@app.get("/order/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/order/{orders_id}", response_model=Order)
async def read_orders(orders_id: int):
    query = orders.select().where(orders.c.id == orders_id)
    return await database.fetch_one(query)


@app.put("/order/{orders_id}", response_model=Order)
async def update_orders(orders_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id ==
    orders_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": orders_id}

@app.delete("/order/{orders_id}")
async def delete_orders(orders_id: int):
    query = orders.delete().where(orders.c.id == orders_id)
    await database.execute(query)
    return {'message': 'order deleted'}

@app.post("/product/", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(name=product.name,
                                     description=product.description,
                                     price=product.price)
    last_record_id = await database.execute(query)
    return {**product.dict(), "id": last_record_id}
@app.get("/product/", response_model=List[Product])
async def read_product():
    query = products.select()
    return await database.fetch_all(query)
@app.get("/product/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)
@app.put("/product/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id ==
    product_id).values(**new_product.dict())
    await database.execute(query)
    return {**new_product.dict(), "id": product_id}
@app.delete("/product/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {'message': 'product deleted'}
@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(email=user.email,password=user.password,
                                  first_name=user.first_name,
    last_name=user.last_name)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}
@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)
@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id ==
    user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}
