# Notification Service

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Notification(BaseModel):
    order_id: str
    message: str

@app.post("/notify")
def notify(notification: Notification):
    print(f"Notification for Order {notification.order_id}: {notification.message}")
    return {"status": "Notification sent"}
