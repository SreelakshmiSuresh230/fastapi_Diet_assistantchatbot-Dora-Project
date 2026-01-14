📘 Dora — Gemini Diet Assistant Chatbot (FastAPI)

Dora is a diet-focused AI assistant built with FastAPI and powered by Google GenAI (Gemini models). It responds only when the user message contains diet or nutrition-related keywords, helping users with personalized diet tips, meal guidance, and health-related nutrition information.

🧠 Features

✔ Conversational AI chatbot UI
✔ Powered by Gemini-2.5-flash model
✔ Diet-specific keyword filtering
✔ Provides diet advice only for nutrition questions
✔ Custom diet tips endpoint
✔ Static file serving + frontend integration

🧱 File Structure
FASTAPI_AI_CHATBOT/
│
├── app/
│   └── chatbot.py              # Backend server
│
├── static/
│   └── images.jpg              # Bot image used in UI
│
├── templates/
│   └── index.html              # Frontend chat UI
│
├── .env                        # Environment config
├── .gitignore
├── list_models.py              # Optional model util
├── README.md                  # ← You are here
└── requirements.txt

🛠️ Prerequisites

Install Python 3.9+

Make sure you have:

A valid Google Cloud credentials with GenAI access

Python venv support (python3 -m venv)

🚀 Setup & Installation
1. Clone the repository
git clone https://github.com/your-username/FASTAPI_AI_CHATBOT.git
cd FASTAPI_AI_CHATBOT

2. Create & activate virtual environment

Linux / macOS:

python3 -m venv venv
source venv/bin/activate


Windows:

python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

⚙ Environment Configuration

Create a .env in the project root:

GEMINI_API_KEY=your_google_genai_api_key_here


Your .env should only contain:

GEMINI_API_KEY=…


Make sure to add .env to your .gitignore to avoid committing secrets.

📦 Requirements (requirements.txt)
fastapi
uvicorn
python-dotenv
google-genai
python-multipart

🧠 Backend Explained — app/chatbot.py
🧩 CORS Support

You enabled CORS so frontend can call API from any origin:

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

📂 Static Files

Your backend serves images and other static assets:

app.mount("/static", StaticFiles(directory=ROOT_DIR), name="static")


This makes images accessible like:

http://localhost:8000/static/images.jpg

🆓 Frontend Endpoint

The root route serves the UI:

@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(ROOT_DIR, "index.html"))

🧠 Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


This uses your key to authenticate with the Gemini model.

📌 Diet Keyword Logic

Only replies if the message contains at least one nutrition/diet related keyword:

if not any(keyword in message for keyword in diet_keywords):
    return {"reply": "I’m your Diet Assistant, so I only answer nutrition and diet-related questions ..."}


This prevents unrelated queries from being answered.

🗨️ API Endpoints
✅ POST /chat

Purpose: Send user message → receive AI reply

📌 Body:

{
  "message": "Tell me a low-calorie dinner plan"
}


📌 Response:

{
  "reply": "Here’s a diet plan for dinner that’s rich in protein and low in calories…"
}

✅ POST /dietTips

Purpose: Get general diet tips.

📌 Response:

{
  "tips": "1. Eat whole foods…\n2. Drink water…\n3. Include fiber…"
}

🧪 Example Requests

You can test via terminal:

curl -X POST "http://localhost:8000/chat" \
-H "Content-Type: application/json" \
-d '{"message": "What should I eat if I have high cholesterol?"}'


Or for diet tips:

curl -X POST "http://localhost:8000/dietTips" \
-H "Content-Type: application/json"

📡 Frontend Integration

Your index.html makes relative API calls:

fetch("/chat", { ... })


This lets the same server host both frontend + backend — no separate host needed.

Frontend elements:

✔ User message input
✔ Send button
✔ Status display
✔ Services list
✔ Message thread UI

📌 Deployment Options
📦 With Uvicorn (production)
uvicorn app.chatbot:app --host 0.0.0.0 --port 8000