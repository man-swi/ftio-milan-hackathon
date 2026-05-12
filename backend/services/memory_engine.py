from backend.services.database import (
    save_historical_trends,
    save_analysis_history,
    save_inventory_snapshots,
    save_recommendation_history,
    get_previous_trend,
    get_latest_analysis
)


# -----------------------------------
# SAVE COMPLETE ANALYSIS MEMORY
# -----------------------------------

def persist_analysis_memory(
    trends,
    metrics,
    strategy_output,
    reflection_output
):

    save_historical_trends(trends)

    save_analysis_history(metrics)

    save_inventory_snapshots(
        metrics["inventory_alerts"]
    )

    save_recommendation_history(
        strategy_output,
        reflection_output
    )


# -----------------------------------
# GET HISTORICAL TREND DATA
# -----------------------------------

def retrieve_previous_trend_data(
    trend_name
):

    return get_previous_trend(
        trend_name
    )


# -----------------------------------
# GET LATEST ANALYSIS
# -----------------------------------

def retrieve_latest_analysis():

    return get_latest_analysis()