# Payment Service

from time import sleep

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class PaymentRequest(BaseModel):
    order_id: str
    amount: float


@app.post("/process_payment")
def process_payment(payment_request: PaymentRequest):
    # Allocate a list (~2 MB) for simulating data processing
    data = [b'x' * 1024 * 1024 for _ in range(2)]
    # Simulating a processing time
    sleep(3)
    # Clean memory
    del data

    if payment_request.amount > 1000:
        return {"status": "Failed", "message": "Payment failed: amount exceeds limit."}

    return {"status": "Paid", "message": "Payment processed successfully."}
