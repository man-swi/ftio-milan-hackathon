from backend.services.database import (
    get_connection
)

from datetime import datetime


# -----------------------------------
# SAVE TREND HISTORY
# -----------------------------------

def save_trend_history(
    trend_name,
    momentum
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO historical_trends (
            trend_name,
            momentum,
            recorded_at
        )
        VALUES (?, ?, ?)
        """,
        (
            trend_name,
            momentum,
            datetime.now()
            .strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    connection.commit()

    connection.close()

# -----------------------------------
# PERSIST ANALYSIS MEMORY
# -----------------------------------

def persist_analysis_memory(
    trend_data,
    inventory_data,
    recommendations
):

    connection = get_connection()

    cursor = connection.cursor()

    # -----------------------------------
    # STORE TREND SNAPSHOTS
    # -----------------------------------

    for trend in trend_data:

        cursor.execute(
            """
            INSERT INTO historical_trends (
                trend_name,
                momentum,
                recorded_at
            )
            VALUES (?, ?, ?)
            """,
            (
                trend["trend"],
                trend["momentum"],
                datetime.now()
                .strftime("%Y-%m-%d %H:%M:%S")
            )
        )

    connection.commit()

    connection.close()

# -----------------------------------
# GET PREVIOUS MOMENTUM
# -----------------------------------

def get_previous_momentum(
    trend_name
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT momentum
        FROM historical_trends
        WHERE trend_name = ?
        ORDER BY recorded_at DESC
        LIMIT 1
        """,
        (trend_name,)
    )

    result = cursor.fetchone()

    connection.close()

    if result:

        return result[0]

    return None


# -----------------------------------
# CALCULATE MOMENTUM ACCELERATION
# -----------------------------------

def calculate_momentum_acceleration(
    trend_name,
    current_momentum
):

    previous_momentum = (
        get_previous_momentum(
            trend_name
        )
    )

    if previous_momentum is None:

        save_trend_history(
            trend_name,
            current_momentum
        )

        return {

            "previous_momentum": None,

            "current_momentum":
            current_momentum,

            "momentum_change": None,

            "acceleration_label":
            "NEW TREND"
        }

    momentum_change = round(

        (
            current_momentum
            - previous_momentum
        ) * 100,

        2
    )

    if momentum_change > 15:

        acceleration_label = (
            "HIGH ACCELERATION"
        )

    elif momentum_change > 5:

        acceleration_label = (
            "RISING"
        )

    elif momentum_change < -5:

        acceleration_label = (
            "DECLINING"
        )

    else:

        acceleration_label = (
            "STABLE"
        )

    save_trend_history(
        trend_name,
        current_momentum
    )

    return {

        "previous_momentum":
        previous_momentum,

        "current_momentum":
        current_momentum,

        "momentum_change":
        momentum_change,

        "acceleration_label":
        acceleration_label
    }


# -----------------------------------
# GET HISTORICAL TRENDS
# -----------------------------------

def get_historical_trends():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            trend_name,
            momentum,
            recorded_at
        FROM historical_trends
        ORDER BY recorded_at DESC
        LIMIT 10
        """
    )

    rows = cursor.fetchall()

    connection.close()

    historical_data = []

    for row in rows:

        historical_data.append({

            "trend_name": row[0],

            "momentum": row[1],

            "recorded_at": row[2]
        })

    return historical_data

# -----------------------------------
# RETRIEVE PREVIOUS TREND DATA
# -----------------------------------

def retrieve_previous_trend_data(
    trend_name
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            momentum,
            recorded_at
        FROM historical_trends
        WHERE trend_name = ?
        ORDER BY recorded_at DESC
        LIMIT 1
        """,
        (trend_name,)
    )

    result = cursor.fetchone()

    connection.close()

    if result:

        return {

            "momentum": result[0],

            "recorded_at": result[1]
        }

    return None