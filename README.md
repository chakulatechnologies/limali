FarmSmart AI
Market Intelligence and Responsible AI for Smallholder Farmers in Kenya

FarmSmart AI is a decision-support system designed to help smallholder farmers understand where and when to sell their crops for the best possible return.
It translates raw market data into actionable guidance that farmers can understand and trust, regardless of language, literacy level, or access to technology.

The goal is not only to provide information, but to bridge the gap between farmers and the markets that determine their livelihood.

1. User Story

Mary is a smallholder farmer in Kajiado County.
She grows maize and beans on her one-acre plot. Mary has always depended on neighbours, brokers, and local traders to know:

When to harvest

When prices might go up or down

Where to sell for a fair return

Whether transporting produce to a distant market is worth the cost

Her decisions are often influenced by incomplete or unreliable information. As a result, Mary sometimes sells too early, travels too far, or earns less than she could.

FarmSmart AI supports Mary by providing:

A prediction of how crop prices are likely to move

A comparison of nearby markets based on price, distance, and transport costs

A clear recommendation of the best market to sell in

A simple explanation in the language she understands

A suggested selling window when the market price will likely be highest

Mary does not need to understand algorithms or forecasting models.
She simply enters her crop and county, and FarmSmart AI returns advice she can use immediately.

2. What the System Does

FarmSmart AI provides four core capabilities:

Market Price Forecasting

Using historical retail and wholesale prices, the system predicts short-term future price trends for each crop in each market.

Market Comparison and Ranking

It calculates the effective profit a farmer can make after subtracting transport costs, then ranks markets accordingly.

Best Selling Window

The system identifies the period where prices are predicted to be highest, helping farmers make timely decisions.

Human-Centred AI Explanation

Using a language-aware model, the system produces simplified explanations that farmers can understand.
The guidance emphasises transparency: why a market was chosen, what assumptions were made, and how the model reached its conclusion.

3. AI Model for Overcoming Language Barriers

FarmSmart AI uses a language model (Gemini) to ensure that insights are communicated effectively across diverse farmer populations.
This model is used only for explanation and translation, not for price prediction.

The language model addresses:

Simplification

The system converts technical output from forecasting and ranking algorithms into accessible responses that avoid jargon.

Local Language Support

The model generates explanations in Swahili and can be adapted for local languages such as Kikuyu, Kalenjin, or Maasai.

Cultural Context

Phrasing and examples are chosen to be relevant to Kenyan rural contexts, ensuring that advice aligns with how farmers think and make decisions.

Transparency

The explanation always includes:

Why a specific market was recommended

What the predicted prices are

What assumptions were used

What factors influenced the decision
This helps prevent the “black box” problem where users cannot understand or trust AI decisions.

4. Ethical Principles

FarmSmart AI is built with responsibility in mind:

Uses only open, ethically sourced data

Does not require sensitive or personally identifiable information

Provides explanation for every decision

Supports fairness by ensuring underserved regions are not excluded due to data gaps

Works in low-bandwidth settings

Respects user consent and privacy

5. High-Level Architecture

The system is organised into four primary modules:

1. Data Ingestion

Market prices are uploaded in CSV format.
The system validates and cleans the data before storing it.

2. Forecasting

Each crop–market pair is used to train a lightweight Prophet model that predicts future prices.

3. Recommendation Engine

Using forecast output, distance to markets, and transport costs, the system identifies the best market and selling window.

4. AI Explanation Layer

The final recommendation is translated into farmer-friendly language and culturally relevant guidance.

6. Project Structure (Simplified)
market_ai/
│
├── ai/                     # Language model integration and AI explanations
├── ingestion/              # CSV upload and preprocessing
├── forecasting/            # Price prediction and model training
├── recommendations/        # Market ranking and selling window logic
├── prices/                 # Market price database models
├── markets/                # Market metadata and location data
├── farms/                  # Farmer crop and location information
├── users/                  # User profiles and consent tracking
│
├── models/prophet/         # Trained forecasting model files
└── data/                   # Uploaded and cleaned CSV datasets


This structure keeps data, logic, and AI processing clearly separated.
It ensures that each part of the system can be improved or replaced independently.

7. Running the System
1. Install dependencies
pip install -r requirements.txt

2. Run migrations
python manage.py migrate

3. Upload market price data (CSV)
POST /api/market/upload-csv/

4. Train forecasting models
python forecasting/train_models.py

5. Get forecasted prices
POST /api/market/forecast/

6. Get ranked market recommendations
POST /api/market/recommend/

7. Get final farmer-friendly advice
POST /api/market/advice/

8. Intended Impact

FarmSmart AI has been designed to:

Improve farmers’ ability to negotiate fair prices

Reduce losses caused by poor timing or limited information

Help farmers make informed decisions in a simple, accessible way

Promote equitable access to AI tools regardless of language or literacy

The system is meant to be a companion for farmers, not a replacement for their judgment or experience.
It aims to strengthen their autonomy and economic resilience.
