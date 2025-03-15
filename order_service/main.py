import uuid
from datetime import datetime

import requests
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/orders_db"

# Database setup
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)


class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    items = Column(String)  # Simplified for demo purposes
    total_amount = Column(Float)
    status = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Order(BaseModel):
    customer_id: str
    items: list
    total_amount: float


Base.metadata.create_all(bind=engine)

app = FastAPI()

Instrumentator().instrument(app).expose(app)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "OK"}


# Order routes
@app.post("/create_order", status_code=201)
def create_order(order: Order):
    order_id = str(uuid.uuid4())
    db = SessionLocal()

    try:
        new_order = OrderModel(
            id=order_id,
            customer_id=order.customer_id,
            items=str(order.items),
            total_amount=order.total_amount,
            status="Created",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(new_order)
        db.commit()

        # Notify user of created order
        requests.post(
            "http://notification-service:8001/notify",
            json={"order_id": order_id, "message": "Order created successfully"},
        )

        # Process payment
        response = requests.post(
            "http://payment-service:8002/process_payment",
            json={"order_id": order_id, "amount": order.total_amount},
        )
        payment_status = response.json()

        # Update order status based on payment
        new_order.status = payment_status["status"]
        new_order.updated_at = datetime.utcnow()

        db.commit()

        # Notify user of payment status
        requests.post(
            "http://notification-service:8001/notify",
            json={"order_id": order_id, "message": payment_status["message"]},
        )

        return {"order_id": order_id, "status": new_order.status}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    db = SessionLocal()
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    db.close()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
