import streamlit as st
import requests
import pandas as pd
from io import StringIO

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="FTIO Dashboard",
    layout="wide"
)

# -----------------------------------
# BACKEND URL
# -----------------------------------

BACKEND_URL = "http://127.0.0.1:8000"

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.metric-card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #2f3542;
}

.trend-card {
    background-color: #172a45;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
}

.alert-understock {
    background-color: #4b5320;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
}

.alert-overstock {
    background-color: #4a2323;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.title("FTIO Dashboard")

    st.markdown("---")

    st.subheader("System Status")

    st.success("Backend API: Active")
    st.success("CrewAI: Running")
    st.success("Groq API: Connected")
    st.success("Database: Online")

    st.markdown("---")

    st.caption("Built for Milan AI Week Hackathon")

# -----------------------------------
# HEADER
# -----------------------------------

st.title("Fashion Trend Intelligence Dashboard")

st.write(
    "AI-powered retail intelligence system "
    "for fashion trend analysis and "
    "inventory optimization."
)

st.markdown("---")

# -----------------------------------
# CSV UPLOAD SECTION
# -----------------------------------

st.header("Upload Inventory CSV")

uploaded_file = st.file_uploader(
    "Upload inventory dataset",
    type=["csv"]
)

if uploaded_file is not None:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "text/csv"
        )
    }

    response = requests.post(
        f"{BACKEND_URL}/upload",
        files=files
    )

    if response.status_code == 200:

        st.success(
            f"{uploaded_file.name} uploaded successfully."
        )

        # Preview CSV

        dataframe = pd.read_csv(uploaded_file)

        st.subheader("Inventory Preview")

        st.dataframe(
            dataframe,
            use_container_width=True
        )

    else:

        st.error("Upload failed.")

st.markdown("---")

# -----------------------------------
# ANALYZE SECTION
# -----------------------------------

st.header("Run AI Analysis")

analyze_button = st.button("Analyze Trends")

if analyze_button:

    with st.spinner(
        "Running AI multi-agent analysis..."
    ):

        response = requests.post(
            f"{BACKEND_URL}/analyze"
        )

    if response.status_code == 200:

        data = response.json()

        report = data["report"]

        metrics = data["metrics"]

        st.success(
            "Analysis completed successfully."
        )

        # -----------------------------------
        # BUSINESS METRICS
        # -----------------------------------

        st.markdown("---")

        st.header("Business Metrics")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Top Trend Momentum",
                metrics["top_trend_momentum"]
            )

        with col2:

            st.metric(
                "Revenue Opportunity",
                f"${metrics['total_revenue_opportunity']:,.0f}"
            )

        with col3:

            st.metric(
                "Inventory Risk",
                f"${metrics['total_inventory_risk']:,.0f}"
            )

        # -----------------------------------
        # TREND INSIGHTS
        # -----------------------------------

        st.markdown("---")

        st.header("Trend Insights")

        trend_columns = st.columns(2)

        for index, trend in enumerate(
            metrics["trend_insights"]
        ):

            with trend_columns[index % 2]:

                st.markdown(
                    f"""
                    <div class="trend-card">

                    <h4>{trend['trend'].title()}</h4>

                    <p>
                    <b>Momentum:</b>
                    {trend['momentum']}
                    </p>

                    <p>
                    <b>Confidence:</b>
                    {int(trend['confidence'] * 100)}%
                    </p>

                    <p>
                    <b>Peak Prediction:</b>
                    {trend['peak_prediction_days']} days
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # -----------------------------------
        # INVENTORY ALERTS
        # -----------------------------------

        st.markdown("---")

        st.header("Inventory Alerts")

        for alert in metrics["inventory_alerts"]:

            # UNDERSTOCK

            if alert["type"] == "UNDERSTOCK":

                st.markdown(
                    f"""
                    <div class="alert-understock">

                    <h4>
                    UNDERSTOCK ALERT
                    </h4>

                    <p>
                    <b>Product:</b>
                    {alert['product']}
                    </p>

                    <p>
                    <b>Current Stock:</b>
                    {alert['current_stock']}
                    </p>

                    <p>
                    <b>Recommended Stock:</b>
                    {alert['recommended_stock']}
                    </p>

                    <p>
                    <b>Missing Units:</b>
                    {alert['missing_units']}
                    </p>

                    <p>
                    <b>Revenue Opportunity:</b>
                    ${alert['revenue_opportunity']:,.0f}
                    </p>

                    <p>
                    <b>Priority:</b>
                    {alert['priority']}
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # OVERSTOCK

            else:

                st.markdown(
                    f"""
                    <div class="alert-overstock">

                    <h4>
                    OVERSTOCK ALERT
                    </h4>

                    <p>
                    <b>Product:</b>
                    {alert['product']}
                    </p>

                    <p>
                    <b>Current Stock:</b>
                    {alert['current_stock']}
                    </p>

                    <p>
                    <b>Recommended Stock:</b>
                    {alert['recommended_stock']}
                    </p>

                    <p>
                    <b>Excess Units:</b>
                    {alert['excess_units']}
                    </p>

                    <p>
                    <b>Overstock Cost:</b>
                    ${alert['overstock_cost']:,.0f}
                    </p>

                    <p>
                    <b>Priority:</b>
                    {alert['priority']}
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # -----------------------------------
        # SCENARIO SIMULATIONS
        # -----------------------------------

        st.markdown("---")

        st.header("Scenario Simulations")

        for simulation in metrics["simulation_results"]:

            restock = simulation["restock"]

            st.markdown(
                f"""
                <div class="trend-card">

                <h4>{simulation['product']}</h4>

                <p>
                <b>Recommended Restock:</b>
                {restock['recommended_restock']}
                </p>

                <p>
                <b>Revenue Forecast:</b>
                ${restock['estimated_revenue_gain']:,.0f}
                </p>

                <p>
                <b>Estimated ROI:</b>
                {restock['estimated_roi']}%
                </p>

                <p>
                <b>Sellout Probability:</b>
                {int(restock['sellout_probability'] * 100)}%
                </p>

                <p>
                <b>Risk Level:</b>
                {restock['risk']}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        # -----------------------------------
        # TREND RISK INTELLIGENCE
        # -----------------------------------

        st.markdown("---")

        st.header("Trend Risk Intelligence")

        for trend in metrics["trend_insights"]:

            st.markdown(
                f"""
                <div class="alert-overstock">

                <h4>{trend['trend'].title()}</h4>

                <p>
                <b>Confidence:</b>
                {int(trend['confidence'] * 100)}%
                </p>

                <p>
                <b>Volatility Score:</b>
                {trend['volatility_score']}%
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        # -----------------------------------
        # TEMPORAL INTELLIGENCE
        # -----------------------------------

        st.markdown("---")

        st.header("Temporal Intelligence")

        temporal_insights = data.get(
            "temporal_insights",
            []
        )

        for insight in temporal_insights:

            st.markdown(
                f"""
                <div class="trend-card">

                <h4>{insight['trend'].title()}</h4>

                <p>
                <b>Previous Momentum:</b>
                {insight['previous_momentum']}
                </p>

                <p>
                <b>Current Momentum:</b>
                {insight['current_momentum']}
                </p>

                <p>
                <b>Momentum Change:</b>
                {insight['momentum_change']}%
                </p>

                <p>
                <b>Trend Status:</b>
                {insight['acceleration_label']}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        # -----------------------------------
        # EXECUTIVE REPORT
        # -----------------------------------

        st.markdown("---")

        st.header("Executive Report")

        st.markdown(report)

        # -----------------------------------
        # DOWNLOAD REPORT
        # -----------------------------------

        st.download_button(
            label="Download Report",
            data=report,
            file_name="ftio_report.md",
            mime="text/markdown"
        )

    else:

        st.error("Analysis failed.")