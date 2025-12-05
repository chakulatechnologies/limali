import requests

API_URL = "http://127.0.0.1:8000/advise"   # Change only if hosted online


def divider():
    print("\n" + "="*55 + "\n")


def cli_demo():
    divider()
    print("🌾  FarmSmart AI — CLI DEMO")
    divider()

    # Farmer inputs
    name = input("👤 Enter your name: ").strip() or "Farmer"
    county = input("📍 Enter your county or town: ").strip()
    crop = input("🌽 Enter your crop: ").strip()
    language = "en"  # Optional: "both", "sw"

    divider()
    print("⏳ Sending your details to FarmSmart AI...\n")

    payload = {
        "name": name,
        "county": county,
        "crop": crop,
        "language": language
    }

    try:
        response = requests.post(API_URL, json=payload)
        data = response.json()

        # Server-side error
        if "detail" in data:
            print("❌ Error:", data["detail"])
            return

        # -------------------------------
        # MARKET RECOMMENDATIONS SECTION
        # -------------------------------
        divider()
        print("📊  TOP 3 MARKET RECOMMENDATIONS")

        markets = data["best_markets"]

        for i, m in enumerate(markets, start=1):
            market_name = m.get("market", "Unknown Market")
            county_name = m.get("county", "Unknown County")
            price = m.get("retail_price", "N/A")
            distance = m.get("distance_km", "N/A")
            profit = m.get("effective_profit", m.get("profit", "N/A"))

            print(f"\n{i}. {market_name} ({county_name})")
            print(f"   • Price: {price} KES")
            print(f"   • Distance: {distance} km")
            print(f"   • Profit: {profit} KES")

        # -------------------------------
        # GEMINI AI EXPLANATION
        # -------------------------------
        divider()
        print("🤖  AI EXPLANATION\n")
        print(data["explanation"])

        divider()
        print("🎉  END OF DEMO — THANK YOU!")

    except Exception as e:
        divider()
        print("❌ Failed to connect to backend:", e)
        divider()


if __name__ == "__main__":
    cli_demo()
