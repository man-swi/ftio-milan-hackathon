from datetime import datetime


# ===================================
# GENERATE EXECUTIVE SUMMARY
# ===================================

def generate_executive_summary(
    alerts
):

    if not alerts:

        return {

            "timestamp":
            str(datetime.now()),

            "summary":

            "No operational anomalies detected.",

            "critical_alerts": [],

            "recommendations": []
        }

    # ===================================
    # CRITICAL ALERTS
    # ===================================

    critical_alerts = [

        alert

        for alert in alerts

        if alert.get(
            "severity"
        ) == "HIGH"
    ]

    # ===================================
    # RECOMMENDATIONS
    # ===================================

    recommendations = []

    for alert in critical_alerts:

        message = alert.get(
            "message",
            ""
        )

        if "critically low" in message:

            recommendations.append(

                "Immediate inventory replenishment recommended."

            )

        elif "exceeds projected demand" in message:

            recommendations.append(

                "Reduce inventory exposure to avoid overstock losses."

            )

    # ===================================
    # SUMMARY TEXT
    # ===================================

    summary_text = (

        f"FTIO detected "

        f"{len(alerts)} "

        f"active operational alerts, "

        f"including "

        f"{len(critical_alerts)} "

        f"high-severity risks."
    )

    return {

        "timestamp":
        str(datetime.now()),

        "summary":
        summary_text,

        "critical_alerts":
        critical_alerts[:5],

        "recommendations":
        list(set(recommendations))
    }