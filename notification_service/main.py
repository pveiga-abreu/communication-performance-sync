# Notification Service

from time import sleep

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Notification(BaseModel):
    order_id: str
    message: str


@app.post("/notify")
def notify(notification: Notification):
    # Simulatiing a processing time
    sleep(0.5)

    print(f"Notification for Order {notification.order_id}: {notification.message}")
    return {"status": "Notification sent"}
