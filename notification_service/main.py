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
    # Allocate a list (~1 MB) for simulating data processing
    data = [b'x' * 1024 * 1024 for _ in range(1)]
    # Simulating a processing time
    sleep(0.5)
    # Clean memory
    del data

    print(f"Notification for Order {notification.order_id}: {notification.message}")
    return {"status": "Notification sent"}
