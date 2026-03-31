from google import genai
import os
from google.genai import types
from pydantic import BaseModel,Field
from typing import List
from dotenv import load_dotenv

load_dotenv()

class receiptData(BaseModel):
    date: str = Field(description="日付はYYYY/MM/DDの形式で入力してください。")
    prise: int = Field(description="金額は数値で入力してください。")
    store_name: str
    eligible_invoice_number: str = Field(description="Tから始まる13ケタの数列です。")
    consamption_tax: int
    summary: str



client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

with open(r'C:\Users\01385-202309-02\MyProjects\AI-Bookkeeping\servise\20260311_134640.jpg', 'rb') as f:
    image_data = f.read()

response = client.models.generate_content(
    model = "models/gemini-2.5-flash",
    contents = [
        types.Part.from_bytes(
            data=image_data,
            mime_type="image/jpeg"
        )
    ],
    config={
        "response_mime_type": "application/json",
        "response_schema":receiptData,

    },

)

print(response.text)
