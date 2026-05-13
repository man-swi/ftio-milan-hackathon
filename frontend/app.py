import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from io import StringIO

# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(

    page_title="FTIO Executive Dashboard",

    page_icon="📈",

    layout="wide",

    initial_sidebar_state="expanded"
)

# ===================================
# SESSION STATE
# ===================================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []

if "analysis_data" not in st.session_state:

    st.session_state.analysis_data = None

# ===================================
# BACKEND URL
# ===================================

BACKEND_URL = "http://127.0.0.1:8000"

# ===================================
# CUSTOM CSS
# ===================================

st.markdown("""

<style>

html, body, [class*="css"] {

    font-family: Inter, sans-serif;
}

.main {

    background-color: #0B1120;
}

section[data-testid="stSidebar"] {

    background-color: #111827;
    border-right: 1px solid #1F2937;
}

.block-container {

    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1500px;
}

h1 {

    color: white;
    font-size: 3rem;
    font-weight: 700;
}

h2 {

    color: white;
    font-size: 2rem;
    font-weight: 600;
    margin-top: 1rem;
}

h3 {

    color: white;
}

.metric-card {

    background: linear-gradient(
        135deg,
        #111827,
        #1F2937
    );

    padding: 24px;

    border-radius: 18px;

    border: 1px solid #374151;

    box-shadow:
    0px 4px 25px rgba(0,0,0,0.35);

    margin-bottom: 1rem;
}

.trend-card {

    background: linear-gradient(
        135deg,
        #172554,
        #1E3A8A
    );

    padding: 22px;

    border-radius: 18px;

    border: 1px solid #3B82F6;

    margin-bottom: 18px;

    box-shadow:
    0px 4px 20px rgba(59,130,246,0.15);
}

.alert-understock {

    background: linear-gradient(
        135deg,
        #14532D,
        #166534
    );

    padding: 22px;

    border-radius: 18px;

    border: 1px solid #22C55E;

    margin-bottom: 18px;
}

.alert-overstock {

    background: linear-gradient(
        135deg,
        #450A0A,
        #7F1D1D
    );

    padding: 22px;

    border-radius: 18px;

    border: 1px solid #EF4444;

    margin-bottom: 18px;
}

.executive-panel {

    background: linear-gradient(
        135deg,
        #111827,
        #1E293B
    );

    border-radius: 20px;

    padding: 30px;

    border: 1px solid #334155;

    margin-bottom: 2rem;
}

.section-spacing {

    margin-top: 3rem;
}

.big-number {

    font-size: 2.3rem;

    font-weight: 700;

    color: white;
}

.small-label {

    color: #9CA3AF;

    font-size: 0.95rem;
}

.chat-panel {

    background-color: #111827;

    border-radius: 18px;

    padding: 20px;

    border: 1px solid #374151;
}

.stButton > button {

    width: 100%;

    border-radius: 12px;

    height: 3rem;

    border: none;

    font-weight: 600;

    background: linear-gradient(
        135deg,
        #2563EB,
        #1D4ED8
    );

    color: white;
}

.stTextInput > div > div > input {

    border-radius: 12px;
}

</style>

""", unsafe_allow_html=True)

# ===================================
# SIDEBAR
# ===================================

with st.sidebar:

    st.title("FTIO")

    st.caption(
        "Retail Decision Intelligence Platform"
    )

    st.markdown("---")

    st.subheader("System Status")

    st.success("Backend API Active")

    st.success("CrewAI Operational")

    st.success("Groq Connected")

    st.success("Memory Engine Online")

    st.success("RAG Intelligence Loaded")

    st.markdown("---")

    st.subheader("Capabilities")

    st.markdown("""

    - Trend Forecasting

    - Inventory Intelligence

    - Executive Copilot

    - Temporal Analysis

    - Multi-Agent Reasoning

    - Simulation Engine

    - Retail Knowledge Retrieval

    """)

    st.markdown("---")

    st.caption(
        "Built for Milan AI Week Hackathon"
    )

# ===================================
# HEADER
# ===================================

st.title(
    "FTIO Executive Intelligence Platform"
)

st.markdown("""

AI-powered fashion retail operating system
for inventory optimization,
trend forecasting,
risk analysis,
and executive decision intelligence.

""")

st.markdown("---")

# ===================================
# UPLOAD SECTION
# ===================================

st.header("Inventory Intelligence Input")

uploaded_file = st.file_uploader(

    "Upload inventory CSV",

    type=["csv"]
)

if uploaded_file is not None:

    st.success(
        f"{uploaded_file.name} uploaded"
    )

    preview_df = pd.read_csv(

        StringIO(
            uploaded_file.getvalue()
            .decode("utf-8")
        )
    )

    st.dataframe(

        preview_df,

        width="stretch",

        height=240
    )

    if st.button(
        "Upload Inventory Dataset"
    ):

        files = {

            "file": (

                uploaded_file.name,

                uploaded_file.getvalue(),

                "text/csv"
            )
        }

        try:

            response = requests.post(

                f"{BACKEND_URL}/upload",

                files=files
            )

            if response.status_code == 200:

                st.success(
                    "Inventory uploaded successfully."
                )

            else:

                st.error(
                    "Upload failed."
                )

        except Exception as error:

            st.error(
                f"Backend Error: {error}"
            )

st.markdown("---")

# ===================================
# RUN ANALYSIS
# ===================================

st.header("Retail Intelligence Analysis")

if st.button(
    "Run FTIO Analysis"
):

    with st.spinner(

        "FTIO multi-agent system analyzing retail intelligence..."

    ):

        response = requests.post(
            f"{BACKEND_URL}/analyze"
        )

    if response.status_code == 200:

        st.session_state.analysis_data = (
            response.json()
        )

        st.success(
            "Analysis completed successfully."
        )

    else:

        st.error(
            "Analysis failed."
        )

# ===================================
# DISPLAY ANALYSIS
# ===================================

if st.session_state.analysis_data:

    data = (
        st.session_state.analysis_data
    )

    # ===================================
    # ERROR HANDLING
    # ===================================

    if "error" in data:

        st.error(
            f"Backend Analysis Error:\n\n{data['error']}"
        )

        st.stop()

    # ===================================
    # SAFE DATA ACCESS
    # ===================================

    metrics = data.get("metrics", {})

    report = data.get("report", "")

    temporal_insights = data.get(
        "temporal_insights",
        []
    )


    # ===================================
    # EXECUTIVE METRICS
    # ===================================

    st.markdown(
        '<div class="section-spacing"></div>',
        unsafe_allow_html=True
    )

    st.header("Executive Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(f"""

        <div class="metric-card">

        <div class="small-label">
        Revenue Opportunity
        </div>

        <div class="big-number">
        ${metrics['total_revenue_opportunity']:,.0f}
        </div>

        </div>

        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""

        <div class="metric-card">

        <div class="small-label">
        Inventory Risk
        </div>

        <div class="big-number">
        ${metrics['total_inventory_risk']:,.0f}
        </div>

        </div>

        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""

        <div class="metric-card">

        <div class="small-label">
        Top Trend Momentum
        </div>

        <div class="big-number">
        {metrics['top_trend_momentum']}
        </div>

        </div>

        """, unsafe_allow_html=True)

    with col4:

        st.markdown(f"""

        <div class="metric-card">

        <div class="small-label">
        Avg Confidence
        </div>

        <div class="big-number">
        {metrics['average_confidence']}
        </div>

        </div>

        """, unsafe_allow_html=True)

    # ===================================
    # VISUAL ANALYTICS
    # ===================================

    st.markdown(
        '<div class="section-spacing"></div>',
        unsafe_allow_html=True
    )

    st.header("Visual Intelligence")

    trend_df = pd.DataFrame(
        metrics["trend_insights"]
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(

            trend_df,

            x="trend",

            y="momentum",

            color="confidence",

            title="Trend Momentum Analysis"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with col2:

        fig2 = px.scatter(

            trend_df,

            x="momentum",

            y="volatility_score",

            size="confidence",

            color="trend",

            title="Trend Volatility Mapping"
        )

        st.plotly_chart(
            fig2,
            width="stretch"
        )

    # ===================================
    # TREND INSIGHTS
    # ===================================

    st.markdown(
        '<div class="section-spacing"></div>',
        unsafe_allow_html=True
    )

    st.header("Trend Intelligence")

    trend_columns = st.columns(2)

    for index, trend in enumerate(
        metrics["trend_insights"]
    ):

        with trend_columns[index % 2]:

            st.markdown(f"""

            <div class="trend-card">

            <h3>{trend['trend']}</h3>

            <p>
            <b>Momentum:</b>
            {trend['momentum']}
            </p>

            <p>
            <b>Confidence:</b>
            {int(trend['confidence'] * 100)}%
            </p>

            <p>
            <b>Volatility:</b>
            {trend['volatility_score']}
            </p>

            <p>
            <b>Peak Window:</b>
            {trend['peak_prediction_days']} days
            </p>

            </div>

            """, unsafe_allow_html=True)

    # ===================================
    # INVENTORY ALERTS
    # ===================================

    st.markdown(
        '<div class="section-spacing"></div>',
        unsafe_allow_html=True
    )

    st.header("Inventory Risk Signals")

    for alert in metrics["inventory_alerts"]:

        if alert["type"] == "UNDERSTOCK":

            card_class = "alert-understock"

        else:

            card_class = "alert-overstock"

        st.markdown(f"""

        <div class="{card_class}">

        <h3>{alert['type']} ALERT</h3>

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

        </div>

        """, unsafe_allow_html=True)

    # ===================================
    # TEMPORAL INTELLIGENCE
    # ===================================

    st.markdown(
        '<div class="section-spacing"></div>',
        unsafe_allow_html=True
    )

    st.header("Temporal Intelligence")

    temporal_df = pd.DataFrame(
        temporal_insights
    )

    fig3 = px.line(

        temporal_df,

        x="trend",

        y="current_momentum",

        markers=True,

        title="Trend Momentum Evolution"
    )

    st.plotly_chart(
        fig3,
        width="stretch"
    )

    # ===================================
    # SIMULATIONS
    # ===================================

    st.markdown(
        '<div class="section-spacing"></div>',
        unsafe_allow_html=True
    )

    st.header("Scenario Simulations")

    for simulation in metrics[
        "simulation_results"
    ]:

        restock = simulation["restock"]

        st.markdown(f"""

        <div class="executive-panel">

        <h3>{simulation['product']}</h3>

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
        <b>Inventory Health Score:</b>
        {restock['inventory_health_score']}
        </p>

        <p>
        <b>Demand Label:</b>
        {restock['demand_label']}
        </p>

        </div>

        """, unsafe_allow_html=True)

    # ===================================
    # DOWNLOAD REPORT
    # ===================================

    st.markdown(
        '<div class="section-spacing"></div>',
        unsafe_allow_html=True
    )

    st.download_button(

        label="Download Executive Report",

        data=report,

        file_name="ftio_executive_report.md",

        mime="text/markdown"
    )

# ===================================
# EXECUTIVE COPILOT
# ===================================

st.markdown("---")

st.header("FTIO Executive Copilot")

st.caption(
    "AI retail strategy assistant"
)

suggested_prompts = [

    "What inventory should we prioritize for Q4?",

    "Which trends are accelerating fastest?",

    "Which products have highest inventory risk?",

    "What merchandising strategy should we use for Quiet Luxury?",

    "Which categories have highest revenue potential?"
]

cols = st.columns(5)

for index, prompt in enumerate(
    suggested_prompts
):

    with cols[index]:

        if st.button(prompt):

            st.session_state.user_prompt = (
                prompt
            )

user_input = st.text_input(

    "Ask FTIO",

    value=st.session_state.get(
        "user_prompt",
        ""
    ),

    placeholder=
    "Ask about trends, inventory, simulations, or strategy..."
)

if st.button("Send to FTIO"):

    if user_input.strip():

        with st.spinner(

            "FTIO generating executive intelligence..."

        ):

            try:

                response = requests.post(

                    f"{BACKEND_URL}/chat",

                    json={
                        "message": user_input
                    },

                    timeout=120
                )

                result = response.json()

                if "response" in result:

                    st.session_state.chat_history.append({

                        "question": user_input,

                        "answer":
                        result["response"]
                    })

                else:

                    st.error(

                        result.get(
                            "error",
                            "Unknown error"
                        )
                    )

            except Exception as error:

                st.error(str(error))

# ===================================
# CHAT HISTORY
# ===================================

st.markdown(
    '<div class="section-spacing"></div>',
    unsafe_allow_html=True
)

st.header("Executive Conversations")

for chat in reversed(
    st.session_state.chat_history
):

    with st.chat_message("user"):

        st.markdown(
            chat["question"]
        )

    with st.chat_message("assistant"):

        st.markdown(
            chat["answer"]
        )