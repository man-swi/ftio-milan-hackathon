from backend.services.scenario_engine import (
    simulate_restock,
    simulate_overstock_risk,
    simulate_profit_change
)

from backend.services.temporal_analysis import (
    calculate_momentum_acceleration
)

from backend.services.consensus_engine import (
    generate_consensus_decision
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

        "simulation_results": [],

        # ===================================
        # PHASE 14
        # EXECUTIVE EXPLAINABILITY
        # ===================================

        "executive_explanations": [],

        "confidence_insights": [],

        "risk_insights": [],

        "decision_traces": [],

        # ===================================
        # PHASE 14.5
        # CONSENSUS INTELLIGENCE
        # ===================================

        "consensus_decisions": [],

        "consensus_conflicts": [],

        "consensus_overrides": [],

        "consensus_scores": []
    }

    total_revenue = 0

    total_risk = 0

    total_confidence = 0

    consensus_score_total = 0

    # ===================================
    # PROCESS TRENDS
    # ===================================

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

        # ===================================
        # PROCESS INVENTORY ITEMS
        # ===================================

        for item in matched_items[:1]:

            stock = item["stock"]

            unit_price = item["unit_price"]

            product_name = item["product_name"]

            # ===================================
            # SCENARIO SIMULATION
            # ===================================

            restock_result = simulate_restock(
                trend,
                item
            )

            overstock_result = (
                simulate_overstock_risk(
                    trend,
                    item
                )
            )

            profit_result = (
                simulate_profit_change(
                    restock_result[
                        "estimated_revenue_gain"
                    ]
                )
            )

            # ===================================
            # TEMPORAL INTELLIGENCE
            # ===================================

            temporal_data = (
                calculate_momentum_acceleration(

                    trend_name,
                    momentum
                )
            )

            # ===================================
            # CONSENSUS ENGINE
            # ===================================

            consensus_result = (
                generate_consensus_decision(

                    restock_result,
                    temporal_data
                )
            )

            consensus_score_total += (
                consensus_result[
                    "consensus_score"
                ]
            )

            # ===================================
            # STORE SIMULATION
            # ===================================

            simulation_object = {

                "product": product_name,

                "trend": trend_name,

                "restock": restock_result,

                "overstock": overstock_result,

                "profit": profit_result,

                # ===================================
                # CONSENSUS INTELLIGENCE
                # ===================================

                "consensus":
                consensus_result
            }

            metrics[
                "simulation_results"
            ].append(
                simulation_object
            )

            # ===================================
            # EXECUTIVE EXPLAINABILITY
            # ===================================

            if (
                "decision_explanation"
                in restock_result
            ):

                metrics[
                    "executive_explanations"
                ].append({

                    "product":
                    product_name,

                    "trend":
                    trend_name,

                    "explanation":
                    restock_result[
                        "decision_explanation"
                    ]
                })

            if (
                "confidence_explanation"
                in restock_result
            ):

                metrics[
                    "confidence_insights"
                ].append({

                    "product":
                    product_name,

                    "trend":
                    trend_name,

                    "confidence":
                    restock_result[
                        "confidence_explanation"
                    ]
                })

            if (
                "risk_rationale"
                in restock_result
            ):

                metrics[
                    "risk_insights"
                ].append({

                    "product":
                    product_name,

                    "trend":
                    trend_name,

                    "risk":
                    restock_result[
                        "risk_rationale"
                    ]
                })

            if (
                "decision_trace"
                in restock_result
            ):

                metrics[
                    "decision_traces"
                ].append({

                    "product":
                    product_name,

                    "trend":
                    trend_name,

                    "trace":
                    restock_result[
                        "decision_trace"
                    ]
                })

            # ===================================
            # CONSENSUS AGGREGATION
            # ===================================

            metrics[
                "consensus_decisions"
            ].append({

                "product":
                product_name,

                "trend":
                trend_name,

                "decision":
                consensus_result[
                    "final_decision"
                ],

                "score":
                consensus_result[
                    "consensus_score"
                ]
            })

            if consensus_result[
                "conflicting_agents"
            ]:

                metrics[
                    "consensus_conflicts"
                ].append({

                    "product":
                    product_name,

                    "trend":
                    trend_name,

                    "conflicts":
                    consensus_result[
                        "conflicting_agents"
                    ]
                })

            if consensus_result[
                "risk_override"
            ][
                "override"
            ]:

                metrics[
                    "consensus_overrides"
                ].append({

                    "product":
                    product_name,

                    "trend":
                    trend_name,

                    "reason":
                    consensus_result[
                        "risk_override"
                    ][
                        "reason"
                    ]
                })

            metrics[
                "consensus_scores"
            ].append({

                "product":
                product_name,

                "trend":
                trend_name,

                "score":
                consensus_result[
                    "consensus_score"
                ]
            })

            recommended_stock = (
                restock_result[
                    "recommended_restock"
                ]
            )

            # ===================================
            # UNDERSTOCK ALERT
            # ===================================

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

            # ===================================
            # OVERSTOCK ALERT
            # ===================================

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

        # ===================================
        # TREND INSIGHTS
        # ===================================

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

    # ===================================
    # GLOBAL KPI AGGREGATION
    # ===================================

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

    # ===================================
    # CONSENSUS KPI
    # ===================================

    if metrics["consensus_scores"]:

        metrics[
            "average_consensus_score"
        ] = round(

            consensus_score_total /

            len(
                metrics[
                    "consensus_scores"
                ]
            ),

            2
        )

    else:

        metrics[
            "average_consensus_score"
        ] = 0

    # ===================================
    # EXECUTIVE SUMMARY COUNTERS
    # ===================================

    metrics[
        "total_executive_explanations"
    ] = len(

        metrics[
            "executive_explanations"
        ]
    )

    metrics[
        "total_confidence_insights"
    ] = len(

        metrics[
            "confidence_insights"
        ]
    )

    metrics[
        "total_risk_insights"
    ] = len(

        metrics[
            "risk_insights"
        ]
    )

    metrics[
        "total_decision_traces"
    ] = len(

        metrics[
            "decision_traces"
        ]
    )

    metrics[
        "total_consensus_decisions"
    ] = len(

        metrics[
            "consensus_decisions"
        ]
    )

    metrics[
        "total_consensus_conflicts"
    ] = len(

        metrics[
            "consensus_conflicts"
        ]
    )

    metrics[
        "total_consensus_overrides"
    ] = len(

        metrics[
            "consensus_overrides"
        ]
    )

    print("BUSINESS METRICS FINISHED")

    return metrics