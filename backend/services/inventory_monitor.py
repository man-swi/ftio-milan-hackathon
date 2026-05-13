import pandas as pd

from datetime import datetime

from backend.services.scenario_engine import (
    simulate_restock
)



# ===================================
# LOAD INVENTORY
# ===================================

def load_inventory():

    return pd.read_csv(
        "backend/data/current_inventory.csv"
    )


# ===================================
# LOAD TRENDS
# ===================================

def load_trends():

    return pd.read_json(
        "backend/data/mock_trends.json"
    )


# ===================================
# INVENTORY ANOMALY DETECTION
# ===================================

def detect_inventory_anomalies():

    inventory = load_inventory()

    trends = load_trends()

    alerts = []

    # ===================================
    # PROCESS INVENTORY
    # ===================================

    for _, item in inventory.iterrows():

        category = str(
            item.get(
                "category",
                ""
            )
        ).lower()

        stock = int(
            item.get(
                "stock",
                0
            )
        )

        product_name = item.get(
            "product_name",
            "Unknown Product"
        )

        unit_price = float(
            item.get(
                "unit_price",
                0
            )
        )

        # ===================================
        # MATCH TREND
        # ===================================

        matched_trends = trends[
            trends["category"]
            .str.lower() == category
        ]

        if matched_trends.empty:

            continue

        trend = (
            matched_trends
            .iloc[0]
            .to_dict()
        )

        # ===================================
        # SCENARIO ANALYSIS
        # ===================================

        simulation = simulate_restock(
            trend,
            item.to_dict()
        )

        sellout_probability = (
            simulation.get(
                "sellout_probability",
                0
            )
        )

        recommended_restock = (
            simulation.get(
                "recommended_restock",
                0
            )
        )

        inventory_risk = (
            simulation.get(
                "inventory_risk",
                "LOW"
            )
        )

        # ===================================
        # STOCKOUT ALERT
        # ===================================

        if (

            stock < recommended_restock

            and

            sellout_probability >= 0.7
        ):

            alerts.append({

                "timestamp":
                str(datetime.now()),

                "type":
                "STOCKOUT_RISK",

                "severity":
                "HIGH",

                "product":
                product_name,

                "message":

                f"{product_name} inventory "

                f"critically low. "

                f"Sellout probability "

                f"reached "

                f"{round(sellout_probability*100,2)}%.",

                "risk":
                inventory_risk
            })

        # ===================================
        # OVERSTOCK ALERT
        # ===================================

        elif stock > recommended_restock * 2:

            alerts.append({

                "timestamp":
                str(datetime.now()),

                "type":
                "OVERSTOCK_RISK",

                "severity":
                "MEDIUM",

                "product":
                product_name,

                "message":

                f"{product_name} inventory "

                f"significantly exceeds "

                f"projected demand.",

                "risk":
                inventory_risk
            })

    return alerts