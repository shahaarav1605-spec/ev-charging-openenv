def optimize_charging(battery_level, target_level, hours, prices, solar):
    if hours <= 0:
        return {"error": "Hours must be greater than 0"}

    if len(prices) != hours or len(solar) != hours:
        return {"error": "Invalid input lengths"}

    if battery_level >= target_level:
        return {
            "message": "Battery already sufficient",
            "final_battery": battery_level,
            "total_cost": 0,
            "charging_plan": []
        }

    charging_plan = []
    current_battery = battery_level
    battery_needed = target_level - battery_level
    charge_per_hour = battery_needed / hours
    total_cost = 0

    hour_scores = []
    for i in range(hours):
        score = prices[i] - (solar[i] * 5)
        hour_scores.append((i, score))

    hour_scores.sort(key=lambda x: x[1])
    selected_hours = [h[0] for h in hour_scores]

    for h in selected_hours:
        if current_battery >= target_level:
            break

        energy_added = charge_per_hour
        effective_price = prices[h] * (1 - solar[h])
        cost = energy_added * effective_price

        current_battery += energy_added
        total_cost += cost

        charging_plan.append({
            "hour": h,
            "energy_added": round(energy_added, 2),
            "cost": round(cost, 2)
        })

    return {
        "final_battery": round(current_battery, 2),
        "total_cost": round(total_cost, 2),
        "charging_plan": charging_plan
    }