import os
import json
import google.generativeai as genai
from forecasting.models import ForecastResult
from ai.models import AIAuditLog

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def build_prompt(context):
    """
    Create system + user prompt for Gemini.
    """
    system_prompt = (
        "You are FarmSmart AI, a responsible agricultural assistant for Kenyan farmers. "
        "Your job is to explain market recommendations clearly, ethically, and transparently. "
        "Use simple language. Do not use technical jargon. "
        "Always explain WHY a market was chosen, referencing prices, distance, and transport cost. "
        "Be concise, friendly, and helpful."
    )

    user_prompt = (
        f"Here is the market recommendation context in JSON:\n\n"
        f"{json.dumps(context, indent=2)}\n\n"
        "Generate a clear explanation for a farmer. Include:\n"
        "- Best market and why\n"
        "- Expected price\n"
        "- Transport cost implications\n"
        "- Best selling window (start→end)\n"
        "- Confidence notes (if effective profit differences are small)\n"
        "- Mention data sources briefly\n"
        "Respond in clean, simple Swahili."
    )

    return system_prompt, user_prompt


def generate_explanation(context):
    """
    Generate AI explanation using Gemini.
    """
    system_prompt, user_prompt = build_prompt(context)

    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    explanation = response.text.strip()

    return explanation


def save_ai_audit(forecast_result, context, explanation):
    """
    Save audit trail for transparency.
    """
    AIAuditLog.objects.create(
        forecast=forecast_result,
        model_name="gemini-pro",
        data_sources=context.get("data_sources", []),
        prompt_snippet=json.dumps(context)[:500]
    )

