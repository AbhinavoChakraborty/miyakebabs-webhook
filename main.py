from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define expected payload structure
class WebhookPayload(BaseModel):
    order_id: str
    outlet_id: int
    customer_id: int
    order_date: str
    total_amount: float
    payment_mode: str
    status: str


@app.get("/")
def read_root():
    return {"message": "Miya Kebabs Webhook is live 🚀"}

@app.post("/webhook")
async def receive_webhook(payload: WebhookPayload):
    print("Received webhook payload:", payload.dict())  # Log the data
    return {"message": "Webhook received successfully"}
