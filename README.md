Limali — AI Market Assistant for Kenyan Farmers
Smart, Local, Multilingual Market Insights for Better Farming Decisions

Overview

Limali is an AI-powered assistant that helps Kenyan farmers know where to sell their produce for the best price, based on their county, crop, and preferred language.
It provides simple, human advice, translated into the languages farmers use every day  English, Swahili, Kikuyu, Maasai, Luo, Luhya, Kamba, Meru, Somali, and more.

This project demonstrates how lightweight data and modern AI can meaningfully improve farmers’ earnings and decision-making, without requiring complex apps or heavy infrastructure.

Why Limali Matters

Farmers often make decisions with limited, outdated, or inaccessible market information.
Limali solves these real challenges:

Difficulty knowing which nearby market pays the best

Lack of localized, farmer-friendly guidance

Language barriers

No access to real market intelligence tools

Uncertainty around price stability

By combining simple CSV data, region-based logic, and Google Gemini AI, Limali transforms raw information into useful, clear, actionable advice.

 How Limali Works (Simple Flow)
 
Farmer → Enters name, county, crop, language
          ↓
Limali Backend → Reads markets.csv + ranks top 3 markets
          ↓
Gemini AI → Creates multilingual explanation + advice
          ↓
Farmer → Receives clear guidance in chosen language


Limali evaluates markets using:

Crop type

County and regional clusters

Retail price

Median price stability

Distance scoring (when available)

Gemini then:

Explains the recommendation

Speaks in the farmer’s chosen language

Gives practical selling advice

Key Features

🌐 Multilingual Support

Farmers choose from:
English, Kiswahili, Kikuyu, Maasai, Luo, Luhya, Kamba, Meru, Somali

📊 Top 3 Market Recommendations

Filtered and ranked by:

Market price

Regional proximity

Price stability

Smart fallback logic

💬 AI-Generated Advice

Gemini responds with:

Why the chosen market is best

How the farmer should plan selling time

Contextual tips (transport, timing, negotiation)

💻 Fast, Lightweight, Reliable

Uses:

A single CSV file

A simple FastAPI backend

No heavy databases

No complex infrastructure

🧪 Demo Experience (CLI)

Limali includes a WhatsApp-style CLI demo where the farmer is asked:

“Enter your name”

“Enter your county or town”

“Enter your crop”

“Choose your language”

Limali then replies with:

📊 Top 3 Market Recommendations
🤖 AI Explanation (in chosen language)


Fast, clear, and perfect for hackathon presentations.

🏗️ Project Structure
limali/
├── main.py                  # FastAPI server
├── gemini_client.py         # AI prompt builder + response handler
├── profit_model.py          # Market ranking logic (regional clustering + price median)
├── profit_tips.py           # Practical transport / timing advice
├── profit_forecast.py       # Simple price-trend insights
├── locations.py             # County/town mapping & fallbacks
├── markets.csv              # Market price dataset
├── demo_cli.py              # Interactive CLI demo (WhatsApp-style)
├── requirements.txt         # Dependencies
└── README.md                # Documentation

⚙️ Setup Instructions
1️⃣ Clone the Project
git clone <repo-url>
cd limali

2️⃣ Create a virtual environment
python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add Gemini API key

Create .env:

GEMINI_API_KEY=your_key_here

5️⃣ Run the backend
uvicorn main:app --reload

6️⃣ Run the CLI demo
python3 demo_cli.py

📡 Example API Request
POST /advise

Request:

{
  "name": "Mary",
  "county": "Kajiado",
  "crop": "maize",
  "language": "sw"
}


Response (simplified):

{
  "best_markets": [
    { "market": "Ngong", "retail_price": 5200 },
    { "market": "Kiserian", "retail_price": 5100 },
    { "market": "Nkoroi", "retail_price": 5050 }
  ],
  "explanation": "Mary, soko bora lililo karibu zaidi ni..."
}

🔮 What Limali Could Become

Limali is designed to grow into a real, national tool. Future updates might include:

Real-time price data APIs

GPS-based distance scoring

Weather alerts

Soil and crop recommendations

WhatsApp Business / Twilio deployment

Farmer profile + history tracking

❤️ The Heart Behind Limali

Limali is built around one mission:

Give every Kenyan farmer simple, reliable, and culturally familiar guidance that helps them earn more.

It respects language, culture, and local market knowledge while using AI to empower decision-making.
