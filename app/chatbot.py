import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import google.genai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (images, etc.)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(BASE_DIR, "..")
app.mount("/static", StaticFiles(directory=ROOT_DIR), name="static")

# Chat request model
class ChatRequest(BaseModel):
    message: str

# Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Diet-related keywords
diet_keywords = [
    "diet", "food", "meal", "nutrition", "calories", "weight",
    "diabetes", "prediabetes", "obesity", "cholesterol", "metabolic syndrome",
    "hypertension", "blood pressure", "heart disease", "cardiac", "stroke",
    "pcos", "thyroid", "hypothyroidism", "hyperthyroidism",
    "ibs", "crohn", "ulcerative colitis", "acid reflux", "gastritis",
    "liver", "fatty liver", "hepatitis",
    "kidney", "renal", "dialysis",
    "anemia", "osteoporosis", "arthritis", "cancer nutrition", "pregnancy diet"
]

# Serve frontend
@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(ROOT_DIR, "index.html"))

# Chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    message = request.message.lower()

    if not any(keyword in message for keyword in diet_keywords):
        return {"reply": "I’m your Diet Assistant, so I only answer nutrition and diet-related questions. \
Please ask me about foods, calories, or diet plans for health conditions."}

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",   # ✅ supported model
            contents=[request.message]
        )
        return {"reply": response.text}
    except Exception as e:
        return {"reply": f"Error contacting Gemini API: {str(e)}"}

# Diet tips endpoint
@app.post("/dietTips")
async def diet_tips():
    prompt = "Give 3 evidence-based diet tips for healthy living."
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=[prompt]
        )
        return {"tips": response.text}
    except Exception as e:
        return {"tips": f"Error contacting Gemini API: {str(e)}"}
