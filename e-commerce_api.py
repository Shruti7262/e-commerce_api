from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from typing import Optional
import datetime


app = FastAPI()


# Database
products = {
  1:{
    "name": "TV",
    "price": 999.99,
    "quantity": 10
  },
  2:{
    "name": "Laptop",
    "price": 1299.99,
    "quantity": 5
  },
  3:{
    "name": "Phone",
    "price": 699.99,
    "quantity": 20
  },
  4:{
    "name": "Refrigerators",
    "price": 2999.99,
    "quantity": 15
  },
  5:{
    "name": "Washing machines",
    "price": 1099.99,
    "quantity": 25
  },
  6:{
    "name": "Air Conditioners",
    "price": 3699.99,
    "quantity": 27
  },
  7:{
    "name": "Microwaves",
    "price": 5999.99,
    "quantity": 1
  },
  8:{
    "name": "Shirts",
    "price": 299.99,
    "quantity": 55
  },
  9:{
    "name": "T-Shirts",
    "price": 459.99,
    "quantity": 27
  },
  10:{
    "name": "Jeans",
    "price": 399.99,
    "quantity": 10
  },
  11:{
    "name": "Shoes",
    "price": 1399.99,
    "quantity": 5
  },
  12:{
    "name": "Backpack",
    "price": 899.99,
    "quantity": 20
  },
  13:{
    "name": "Smartwatches",
    "price": 1999.99,
    "quantity": 10
  },
  14:{
    "name": "Tablets",
    "price": 4299.99,
    "quantity": 5
  },
  15:{
    "name": "Sunglasses",
    "price": 299.99,
    "quantity": 20
  },
  16:{
    "name": "Jewellery",
    "price": 9999.99,
    "quantity": 10
  },
  17:{
    "name": "Watches",
    "price": 1799.99,
    "quantity": 5
  },
  18:{
    "name": "Toys",
    "price": 499.99,
    "quantity": 20
  },
  19:{
    "name": "Fan",
    "price": 959.99,
    "quantity": 10
  },
  20:{
    "name": "Charger",
    "price": 299.99,
    "quantity": 5
  }
}

class Product(BaseModel):
    name: str
    price: float
    quantity: int

class UpdateProduct(BaseModel):
    name: Optional[str]
    price: Optional[float]
    quantity: Optional[int]

class UserAddress(BaseModel):
    city: str
    country: str
    zip_code: str

class OrderItem(BaseModel):
    product_id: int
    product_name : str
    bought_quantity: int
    total_amount: float

class Order(BaseModel):
    order_id: str
    timestamp: str
    items: List[OrderItem]
    user_address: UserAddress
    timestamp = datetime.datetime.now()


# Create list to store orders database
orders_db = []


# Get list of all the products
@app.get("/products")
def list_products():
    return list(products.values())


# Get product information by using product name
@app.get("/products/{name}")
def get_products(name : str):
    for product_id in products:
        if products[product_id]['name'] == name:
            return products[product_id]
    return {'Data' : 'Not Found'}


# Place Order
@app.post("/orders", response_model=Order)
def create_order( order: Order):
    orders_db.append(order)
    return order


# Get list of all orders using limit and offset
@app.get("/orders", response_model=List[Order])
def get_orders(limit: int = 10, offset: int = 0):
    return orders_db[offset : offset + limit]


# Get the list of order by using Order ID
@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: str):
    for order in orders_db:
        if order.order_id == order_id:
            return order
    return {"error": "Order not found"}



# Update product information 
@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product):
    if product_id not in products:
        return {"Error": "Product not found"}
    products[product_id] = product.dict()
    return  {"message": "Product quantity updated successfully"}
    # return(product)




# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
