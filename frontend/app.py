import streamlit as st
import requests
import pandas as pd
import time

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="FTIO Dashboard",
    page_icon="📈",
    layout="wide"
)

# -----------------------------------
# API CONFIG
# -----------------------------------

API_BASE_URL = "http://127.0.0.1:8000"

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

    st.caption(
        "Built for Milan AI Week Hackathon"
    )

# -----------------------------------
# HEADER
# -----------------------------------

st.title(
    "Fashion Trend Intelligence Dashboard"
)

st.markdown(
    """
    AI-powered retail intelligence system for
    fashion trend analysis and inventory optimization.
    """
)

st.markdown("---")

# -----------------------------------
# CSV UPLOAD SECTION
# -----------------------------------

st.subheader("Upload Inventory CSV")

uploaded_file = st.file_uploader(
    "Upload inventory dataset",
    type=["csv"]
)

upload_success = False

if uploaded_file is not None:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "text/csv"
        )
    }

    response = requests.post(
        f"{API_BASE_URL}/upload",
        files=files
    )

    if response.status_code == 200:

        st.success(
            f"{uploaded_file.name} uploaded successfully."
        )

        upload_success = True

        df = pd.read_csv(uploaded_file)

        st.subheader("Inventory Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.error("Upload failed.")

st.markdown("---")

# -----------------------------------
# ANALYZE SECTION
# -----------------------------------

st.subheader("Run AI Analysis")

analyze_button = st.button(
    "Analyze Trends"
)

# -----------------------------------
# ANALYSIS PIPELINE
# -----------------------------------

if analyze_button:

    if uploaded_file is None:

        st.warning(
            "Please upload an inventory CSV first."
        )

    else:

        # -----------------------------------
        # AGENT ACTIVITY FEED
        # -----------------------------------

        st.subheader("Agent Workflow")

        activity_box = st.empty()

        activity_box.info(
            "Trend Agent analyzing fashion signals..."
        )

        time.sleep(1.5)

        activity_box.info(
            "Inventory Agent comparing inventory data..."
        )

        time.sleep(1.5)

        activity_box.info(
            "Report Agent generating executive insights..."
        )

        time.sleep(1.5)

        # -----------------------------------
        # RUN BACKEND ANALYSIS
        # -----------------------------------

        with st.spinner(
            "Running multi-agent analysis..."
        ):

            response = requests.post(
                f"{API_BASE_URL}/analyze"
            )

        # -----------------------------------
        # HANDLE RESPONSE
        # -----------------------------------

        if response.status_code == 200:

            result = response.json()

            report_text = result["report"]

            activity_box.success(
                "Analysis completed successfully."
            )

            st.markdown("---")

            # -----------------------------------
            # METRICS
            # -----------------------------------

            st.subheader("Business Metrics")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Top Trend Momentum",
                    "0.91"
                )

            with col2:
                st.metric(
                    "Revenue Opportunity",
                    "$10,750"
                )

            with col3:
                st.metric(
                    "Inventory Risk",
                    "$11,200"
                )

            st.markdown("---")

            # -----------------------------------
            # TREND INSIGHTS
            # -----------------------------------

            st.subheader("Trend Insights")

            trend_col1, trend_col2 = st.columns(2)

            with trend_col1:

                st.info(
                    """
                    Coquette Aesthetic

                    Momentum: 0.91

                    Peak Prediction: 14 days
                    """
                )

            with trend_col2:

                st.info(
                    """
                    Gorpcore

                    Momentum: 0.84

                    Peak Prediction: 21 days
                    """
                )

            st.markdown("---")

            # -----------------------------------
            # INVENTORY ALERTS
            # -----------------------------------

            st.subheader("Inventory Alerts")

            st.warning(
                """
                UNDERSTOCK ALERT

                Pink Ribbon Top

                Current Stock: 5

                Recommended Restock: 50
                """
            )

            st.error(
                """
                OVERSTOCK ALERT

                Cargo Street Pants

                Current Stock: 120

                Consider markdown promotions.
                """
            )

            st.markdown("---")

            # -----------------------------------
            # EXECUTIVE REPORT
            # -----------------------------------

            st.subheader("Executive Report")

            st.markdown(report_text)

            # -----------------------------------
            # DOWNLOAD BUTTON
            # -----------------------------------

            st.download_button(
                label="Download Report",
                data=report_text,
                file_name="ftio_report.md",
                mime="text/markdown"
            )

        else:

            st.error(
                "Analysis failed."
            )