def transport_savings_tips(distance_km, transport_cost):
    """
    Generate simple transport-saving suggestions.
    Handles cases where distance_km or cost is None.
    """

    # If distance is missing → give generic advice
    if distance_km is None:
        return [
            "Ask local transporters about shared delivery options.",
            "Compare buyer prices early in the morning.",
            "Choose the closest main market to reduce cost."
        ]

    tips = []

    # Short distance
    if distance_km <= 5:
        tips.append("Short distance — consider walking or using a motorbike to reduce cost.")
    else:
        tips.append("Share transport with neighbors to reduce per-km charges.")

    # Medium distance
    if 5 < distance_km <= 20:
        tips.append("Travel early in the morning to find better prices and less traffic.")

    # Long distance
    if distance_km > 20:
        tips.append("Compare transporters before choosing one; prices vary widely.")

    # If transport cost exists
    if transport_cost is not None:
        if transport_cost > 800:
            tips.append("High transport cost — sell in a closer market if possible.")
        else:
            tips.append("Transport cost is moderate — evaluate profit before selling.")

    # Ensure at least one tip
    if not tips:
        tips.append("Consider distance and transport cost before choosing a market.")

    return tips