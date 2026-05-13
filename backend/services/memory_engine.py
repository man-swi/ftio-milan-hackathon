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
    metrics,
    strategy_output,
    reflection_output
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

    # -----------------------------------
    # OPTIONAL:
    # STORE STRATEGY OUTPUTS
    # -----------------------------------

    if strategy_output:

        cursor.execute(
            """
            INSERT INTO strategy_memory (
                strategy_text,
                recorded_at
            )
            VALUES (?, ?)
            """,
            (
                strategy_output,
                datetime.now()
                .strftime("%Y-%m-%d %H:%M:%S")
            )
        )

    # -----------------------------------
    # OPTIONAL:
    # STORE REFLECTION OUTPUTS
    # -----------------------------------

    if reflection_output:

        cursor.execute(
            """
            INSERT INTO reflection_memory (
                reflection_text,
                recorded_at
            )
            VALUES (?, ?)
            """,
            (
                reflection_output,
                datetime.now()
                .strftime("%Y-%m-%d %H:%M:%S")
            )
        )

    connection.commit()

    connection.close()

    print("MEMORY SAVED")


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


# -----------------------------------
# GET STRATEGY MEMORY
# -----------------------------------

def get_strategy_memory():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            strategy_text,
            recorded_at
        FROM strategy_memory
        ORDER BY recorded_at DESC
        LIMIT 5
        """
    )

    rows = cursor.fetchall()

    connection.close()

    strategy_history = []

    for row in rows:

        strategy_history.append({

            "strategy_text": row[0],

            "recorded_at": row[1]
        })

    return strategy_history


# -----------------------------------
# GET REFLECTION MEMORY
# -----------------------------------

def get_reflection_memory():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            reflection_text,
            recorded_at
        FROM reflection_memory
        ORDER BY recorded_at DESC
        LIMIT 5
        """
    )

    rows = cursor.fetchall()

    connection.close()

    reflection_history = []

    for row in rows:

        reflection_history.append({

            "reflection_text": row[0],

            "recorded_at": row[1]
        })

    return reflection_history


# -----------------------------------
# CLEAR MEMORY TABLES
# -----------------------------------

def clear_memory():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM historical_trends"
    )

    cursor.execute(
        "DELETE FROM strategy_memory"
    )

    cursor.execute(
        "DELETE FROM reflection_memory"
    )

    connection.commit()

    connection.close()

    print("MEMORY CLEARED")