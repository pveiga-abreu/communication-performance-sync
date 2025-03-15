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
    # Simulatiing a processing time
    sleep(3)

    if payment_request.amount > 1000:
        return {"status": "Failed", "message": "Payment failed: amount exceeds limit."}

    return {"status": "Paid", "message": "Payment processed successfully."}
