def optimize_charging(battery_level, target_level, hours, prices, solar):
    """
    EV Charging Optimization Logic

    Parameters:
    - battery_level: current battery percentage (0–100)
    - target_level: desired battery percentage (0–100)
    - hours: total hours available for charging
    - prices: list of electricity prices per hour
    - solar: list of solar availability (0 to 1)

    Returns:
    - optimized charging plan
    """

    # -----------------------------
    # Input Validation
    # -----------------------------
    if hours <= 0:
        return {"error": "Hours must be greater than 0"}

    if len(prices) != hours or len(solar) != hours:
        return {
            "error": "Length of price_per_hour and solar_available must match hours_available"
        }

    if battery_level >= target_level:
        return {
            "message": "Battery already sufficient",
            "final_battery": battery_level,
            "total_cost": 0,
            "charging_plan": []
        }

    # -----------------------------
    # Initialization
    # -----------------------------
    charging_plan = []
    current_battery = battery_level
    battery_needed = target_level - battery_level

    # Assume equal distribution of charge
    charge_per_hour = battery_needed / hours
    total_cost = 0

    # -----------------------------
    # Scoring Logic
    # Lower score = better hour
    # -----------------------------
    hour_scores = []

    for i in range(hours):
        # Solar reduces effective cost impact
        score = prices[i] - (solar[i] * 5)
        hour_scores.append((i, score))

    # Sort hours by best score
    hour_scores.sort(key=lambda x: x[1])

    # Select best hours
    selected_hours = [h[0] for h in hour_scores]

    # -----------------------------
    # Charging Simulation
    # -----------------------------
    for h in selected_hours:
        if current_battery >= target_level:
            break

        energy_added = charge_per_hour

        # Effective price reduced by solar
        effective_price = prices[h] * (1 - solar[h])

        cost = energy_added * effective_price
        total_cost += cost

        current_battery += energy_added

        charging_plan.append({
            "hour": int(h),
            "energy_added": round(energy_added, 2),
            "cost": round(cost, 2),
            "price": prices[h],
            "solar_used": solar[h],
            "effective_price": round(effective_price, 2)
        })

    # -----------------------------
    # Final Output
    # -----------------------------
    return {
        "initial_battery": round(battery_level, 2),
        "target_battery": round(target_level, 2),
        "final_battery": round(min(current_battery, target_level), 2),
        "total_cost": round(total_cost, 2),
        "hours_used": len(charging_plan),
        "charging_plan": charging_plan
    }