# profit_tips.py

def transport_savings_tips(distance_km: float, transport_cost: float):
    tips = []

    # Shared transport recommendation
    if distance_km > 5:
        tips.append(
            "Consider sharing transport with another farmer to reduce the per-km cost."
        )

    # Early morning efficiency
    if distance_km > 10:
        tips.append(
            "Leaving early in the morning reduces fuel consumption due to cooler temperatures and less traffic."
        )

    # Local market alternative
    if distance_km > 15:
        tips.append(
            "If transport cost is high, check if there is a nearby local market day that might offer competitive prices."
        )

    # Short distance tips
    if distance_km <= 5:
        tips.append(
            "Because the market is close, you can deliver quickly and keep produce fresh for better bargaining power."
        )

    # Universal advice
    tips.append(
        "Transporting produce in bulk or combining deliveries often lowers cost per kilogram."
    )

    return tips[:3]   # return the best 3 tips only
