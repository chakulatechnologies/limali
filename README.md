Limali — Your Local Market Companion for Better Farming Decisions

Limali is a simple AI assistant built to help Kenyan farmers know where to sell their produce for the best price.
No heavy apps, no complicated systems — just clear, friendly advice available in the language the farmer feels most comfortable with.

We designed Limali to work the same way farmers already ask for help:
“Niuze wapi ili nipate bei mzuri?”
And Limali answers that question — instantly.

 Why We Built Limali

Farmers often struggle to know:

Which nearby market is paying the best price

Whether prices are stable, rising, or falling

How location affects their profit

Who to trust for accurate, timely information

Limali solves this by combining simple data with smart, culturally aware AI.

Farmers deserve transparent, local, and easy-to-understand market guidance — and Limali provides exactly that.

 How Limali Works

Here's the journey from the farmer’s question to the AI’s answer:

The farmer enters:

Their name

The county or town they are in

The crop they want to sell

The language they prefer (English, Swahili, Kikuyu, Maasai, Luo, Luhya, Kamba, Meru, Somali)

Limali reads real market data
A simple CSV file contains market names, counties, and prices.
Limali uses this to find the best three markets for that specific crop.

Limali looks at regional patterns
If the farmer is in Rift Valley, it prioritizes Rift Valley markets first.
If the farmer is in Central, it prioritizes Central markets.
This creates smart, human-like reasoning without GPS or complex systems.

Limali sends the information to Gemini AI
Gemini turns the numbers into meaningful guidance:

Which market is best

Why it’s best

What to consider before selling

Advice in the farmer’s chosen language

Limali returns a friendly, WhatsApp-style response
Simple. Local. Clear.

 What Makes Limali Special
✔ Made for all farmers — not just tech-savvy ones

The system works through a simple command line demo or WhatsApp-style UI.

✔ Speaks the farmer’s language

Whether it's Swahili, English, Kikuyu, Maasai, Luo, Luhya, Kamba, Meru, or Somali —
Limali adapts instantly.

✔ Fast and reliable

It uses lightweight logic with no big databases.
Everything runs off a single CSV and a small backend.

✔ Built around real challenges

Transport cost, distance, region, price stability — all considered.

✔ Hackathon-friendly

A full working prototype ready to demo in seconds.

 What’s Inside the Project

FastAPI backend that loads market data and ranks the best markets

Profit + region model for smart recommendations even without GPS

Gemini AI integration for natural, friendly advice

Multilingual system that adjusts to the farmer's preference

CLI demo that simulates a WhatsApp conversation

Simple file-based data that anyone can update

 How to Try It Out

Run the server:

uvicorn main:app --reload


Run the demo:

python3 demo_cli.py


You'll be asked:

Name

County

Crop

Preferred language

And Limali will guide you from there.

 Example of What Limali Says

“Ray, the best market near you is Njoro because prices are higher today,
and markets in your region are performing well.
You may earn better returns by selling early in the morning.”

Or in Swahili:

“Ray, soko bora lililo karibu zaidi ni Njoro.
Bei ni nzuri na unaweza kupata faida zaidi ikiwa utauza mapema.”

Or Kikuyu:

“Ray, thirikari yaku ya mbere nĩ Njoro tondũ wĩrahũrũo wendo mwega.”

Limali always speaks in the language the farmer understands best.

 The Heart of Limali

Limali is built on a simple idea:
Empower farmers with clear, local, trustworthy market knowledge.

No complexity.
No barriers.
Just practical, human advice accessible to anyone.
