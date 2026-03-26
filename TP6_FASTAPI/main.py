from fastapi import FastAPI
from pydantic import BaseModel
import pickle

app = FastAPI(title="Full BI & AI API")

#  ECOMMERCE 
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True
    sales: int
    views: int

db = []

@app.post("/items/")
def create_item(item: Item):
    db.append(item)
    return item

@app.get("/items/")
def list_items():
    return {"items": db}

@app.get("/kpi/total_products")
def total_products():
    return {"total": len(db)}

#  BANK 
class Client(BaseModel):
    age: int
    income: float
    debt: float
    default: int  # 0 or 1

clients = []

@app.post("/clients/")
def add_client(client: Client):
    clients.append(client)
    return client

@app.get("/clients/")
def list_clients():
    return {"clients": clients}

@app.get("/kpi/clients")
def client_kpis():
    total = len(clients)
    avg_income = sum(c.income for c in clients)/total if total else 0
    default_rate = sum(c.default for c in clients)/total if total else 0
    return {
        "total_clients": total,
        "avg_income": avg_income,
        "default_rate": default_rate
    }

# AI 
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.post("/predict")
def predict(item: Item):
    features = [[item.price, item.sales, item.views]]
    return {"prediction": model.predict(features)[0]}
# Valeur totale du stock
@app.get("/kpi/total_value")
def total_value():
    total = sum(item.price for item in db)
    return {"total_value": total}

@app.get("/kpi/in_stock")
def in_stock_products():
    count = sum(1 for item in db if item.in_stock)
    return {"in_stock": count}