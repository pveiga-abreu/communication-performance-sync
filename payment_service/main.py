# Payment Service

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PaymentRequest(BaseModel):
    order_id: str
    amount: float

@app.post("/process_payment")
def process_payment(payment_request: PaymentRequest):
    if payment_request.amount > 1000:
        return {"status": "Failed", "message": "Payment failed: amount exceeds limit."}
    return {"status": "Paid", "message": "Payment processed successfully."}
