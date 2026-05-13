from backend.services.scenario_engine import (
    simulate_restock,
    simulate_overstock_risk,
    simulate_profit_change
)


def calculate_business_metrics(
    trends,
    inventory_data
):

    print("BUSINESS METRICS STARTED")

    metrics = {

        "top_trend_momentum": 0,

        "total_revenue_opportunity": 0,

        "total_inventory_risk": 0,

        "average_confidence": 0,

        "trend_insights": [],

        "inventory_alerts": [],

        "simulation_results": []
    }

    total_revenue = 0

    total_risk = 0

    total_confidence = 0

    # -----------------------------------
    # PROCESS TRENDS
    # -----------------------------------

    for trend in trends:

        trend_name = trend["trend"]

        category = trend["category"]

        momentum = trend["momentum"]

        confidence = trend.get(
            "confidence",
            0
        )

        total_confidence += confidence

        matched_items = []

        for item in inventory_data:

            if (

                item["category"]
                .lower()

                ==

                category.lower()
            ):

                matched_items.append(item)

        # -----------------------------------
        # PROCESS MATCHED ITEMS
        # -----------------------------------

        for item in matched_items:

            stock = item["stock"]

            unit_price = item["unit_price"]

            product_name = item["product_name"]

            # -----------------------------------
            # RESTOCK
            # -----------------------------------

            restock_result = simulate_restock(
                trend,
                item
            )

            # -----------------------------------
            # OVERSTOCK
            # -----------------------------------

            overstock_result = (
                simulate_overstock_risk(
                    trend,
                    item
                )
            )

            # -----------------------------------
            # PROFIT
            # -----------------------------------

            profit_result = (
                simulate_profit_change(
                    restock_result[
                        "estimated_revenue_gain"
                    ]
                )
            )

            metrics[
                "simulation_results"
            ].append({

                "product": product_name,

                "trend": trend_name,

                "restock": restock_result,

                "overstock": overstock_result,

                "profit": profit_result
            })

            recommended_stock = (
                restock_result[
                    "recommended_restock"
                ]
            )

            # -----------------------------------
            # UNDERSTOCK
            # -----------------------------------

            if stock < recommended_stock:

                missing_units = (
                    recommended_stock - stock
                )

                revenue_opportunity = (
                    missing_units * unit_price
                )

                total_revenue += (
                    revenue_opportunity
                )

                metrics[
                    "inventory_alerts"
                ].append({

                    "type": "UNDERSTOCK",

                    "product": product_name,

                    "current_stock": stock,

                    "recommended_stock":
                    recommended_stock,

                    "missing_units":
                    missing_units,

                    "revenue_opportunity":
                    round(
                        revenue_opportunity,
                        2
                    ),

                    "priority":
                    restock_result[
                        "stockout_risk"
                    ]
                })

            # -----------------------------------
            # OVERSTOCK
            # -----------------------------------

            elif stock > recommended_stock * 2:

                excess_units = (
                    stock - recommended_stock
                )

                overstock_cost = (
                    excess_units * unit_price
                )

                total_risk += overstock_cost

                metrics[
                    "inventory_alerts"
                ].append({

                    "type": "OVERSTOCK",

                    "product": product_name,

                    "current_stock": stock,

                    "recommended_stock":
                    recommended_stock,

                    "excess_units":
                    excess_units,

                    "overstock_cost":
                    round(
                        overstock_cost,
                        2
                    ),

                    "priority": "MEDIUM"
                })

        # -----------------------------------
        # TREND INSIGHTS
        # -----------------------------------

        metrics[
            "trend_insights"
        ].append({

            "trend": trend_name,

            "momentum": momentum,

            "confidence": confidence,

            "volatility_score": round(
                (1 - confidence) * 100,
                2
            ),

            "peak_prediction_days":
            trend.get(
                "peak_prediction_days",
                14
            )
        })

    metrics[
        "top_trend_momentum"
    ] = max(

        [t["momentum"] for t in trends]
    )

    metrics[
        "average_confidence"
    ] = round(

        total_confidence / len(trends),

        2
    )

    metrics[
        "total_revenue_opportunity"
    ] = round(
        total_revenue,
        2
    )

    metrics[
        "total_inventory_risk"
    ] = round(
        total_risk,
        2
    )

    print("BUSINESS METRICS FINISHED")

    return metrics