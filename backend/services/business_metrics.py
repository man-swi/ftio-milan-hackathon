def calculate_business_metrics(trends, inventory_df):

    metrics = {
        "top_trend_momentum": 0,
        "total_revenue_opportunity": 0,
        "total_inventory_risk": 0,
        "trend_insights": [],
        "inventory_alerts": []
    }

    total_revenue = 0
    total_risk = 0

    for trend in trends:

        trend_name = trend["trend"]
        category = trend["category"]
        momentum = trend["momentum"]
        confidence = trend.get("confidence", 0)

        matched_items = inventory_df[
            inventory_df["category"].str.lower() == category.lower()
        ]

        for _, item in matched_items.iterrows():

            stock = int(item["stock"])
            unit_price = float(item["unit_price"])
            product_name = item["product_name"]

            recommended_stock = int(momentum * 50)

            # UNDERSTOCK
            if stock < recommended_stock:

                missing_units = recommended_stock - stock

                revenue_opportunity = missing_units * unit_price

                opportunity_score = momentum * missing_units

                if opportunity_score >= 30:
                    priority = "HIGH"
                elif opportunity_score >= 15:
                    priority = "MEDIUM"
                else:
                    priority = "LOW"

                total_revenue += revenue_opportunity

                metrics["inventory_alerts"].append({
                    "type": "UNDERSTOCK",
                    "product": product_name,
                    "current_stock": stock,
                    "recommended_stock": recommended_stock,
                    "missing_units": missing_units,
                    "revenue_opportunity": round(revenue_opportunity, 2),
                    "priority": priority
                })

            # OVERSTOCK
            elif stock > recommended_stock * 2:

                excess_units = stock - recommended_stock

                overstock_cost = excess_units * unit_price

                total_risk += overstock_cost

                metrics["inventory_alerts"].append({
                    "type": "OVERSTOCK",
                    "product": product_name,
                    "current_stock": stock,
                    "recommended_stock": recommended_stock,
                    "excess_units": excess_units,
                    "overstock_cost": round(overstock_cost, 2),
                    "priority": "MEDIUM"
                })

        metrics["trend_insights"].append({
            "trend": trend_name,
            "momentum": momentum,
            "confidence": confidence,
            "peak_prediction_days": trend.get("peak_prediction_days", 14)
        })

    metrics["top_trend_momentum"] = max(
        [t["momentum"] for t in trends]
    )

    metrics["total_revenue_opportunity"] = round(total_revenue, 2)

    metrics["total_inventory_risk"] = round(total_risk, 2)

    return metrics