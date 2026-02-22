import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import google.genai as genai
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
import markdown

# Load environment variables
load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
templates = Jinja2Templates(directory="templates")

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
    "pcos","pcod","thyroid", "hypothyroidism", "hyperthyroidism",
    "ibs", "crohn", "ulcerative colitis", "acid reflux", "gastritis",
    "liver", "fatty liver", "hepatitis",
    "kidney", "renal", "dialysis",
    "anemia", "osteoporosis", "arthritis", "cancer nutrition", "pregnancy diet"
]

# Serve frontend
@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    message = request.message.lower()

    if not any(keyword in message for keyword in diet_keywords):
        reply = markdown.markdown(
            "I’m your Diet Assistant, so I only answer nutrition and diet-related questions. "
            "Please ask me about foods, calories, or diet plans for health conditions."
        )
        return {"reply": reply}

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=[request.message]
        )
        formatted_reply = markdown.markdown(response.text)
    
        return {"reply": formatted_reply}
    except Exception as e:
        return {"reply": markdown.markdown(f"Error contacting Gemini API: {str(e)}")}



