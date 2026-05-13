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
# MONITORING API HELPERS
# ===================================

def fetch_monitoring_status():
    try:
        response = requests.get(
            f"{BACKEND_URL}/monitoring/status"
        )
        if response.status_code == 200:
            return response.json()
    except:
        return {}
    return {}


def fetch_monitoring_alerts():
    try:
        response = requests.get(
            f"{BACKEND_URL}/monitoring/alerts"
        )
        if response.status_code == 200:
            return response.json()
    except:
        return []
    return []


def fetch_executive_summaries():
    try:
        response = requests.get(
            f"{BACKEND_URL}/monitoring/summaries"
        )
        if response.status_code == 200:
            return response.json()
    except:
        return []
    return []


# ===================================
# HELPER FUNCTIONS
# ===================================

def render_bullet_list(items):

    if not items:
        return "<p>No insights available.</p>"

    html = "<ul>"

    for item in items:
        html += f"<li>{item}</li>"

    html += "</ul>"

    return html


def safe_percentage(value):

    try:
        return f"{float(value) * 100:.0f}%"
    except:
        return str(value)


def render_decision_explanation(data):

    if not isinstance(data, dict):
        return f"<p>{data}</p>"

    recommendation = data.get(
        "recommendation",
        "No recommendation available"
    )

    why = data.get("why", [])

    html = f"""

    <div class="explainability-card">

    <h3>WHY THIS DECISION?</h3>

    <p>
    <b>Recommendation:</b>
    {recommendation}
    </p>

    <p><b>Strategic Rationale:</b></p>

    {render_bullet_list(why)}

    </div>

    """

    return html


def render_confidence_explanation(data):

    if not isinstance(data, dict):
        return f"<p>{data}</p>"

    score = data.get(
        "confidence",
        "N/A"
    )

    factors = data.get(
        "confidence_factors",
        []
    )

    html = f"""

    <div class="confidence-card">

    <h3>Confidence Intelligence</h3>

    <p>
    <b>Confidence Score:</b>
    {safe_percentage(score)}
    </p>

    <p>
    <b>Confidence Drivers:</b>
    </p>

    {render_bullet_list(factors)}

    </div>

    """

    return html


def render_financial_rationale(data, restock):

    if not isinstance(data, dict):
        return f"<p>{data}</p>"

    roi = data.get(
        "estimated_roi",
        "N/A"
    )

    financial_reasoning = data.get(
        "financial_reasoning",
        []
    )

    html = f"""

    <div class="financial-card">

    <h3>Financial Rationale</h3>

    <p>
    <b>ROI Logic:</b>
    </p>

    <p>{roi}</p>

    <hr>

    <p>
    <b>Financial Reasoning:</b>
    </p>

    {render_bullet_list(financial_reasoning)}

    <hr>

    <p>
    <b>Projected Demand:</b>
    {restock.get('projected_demand', 'N/A')}
    </p>

    <p>
    <b>Target Inventory:</b>
    {restock.get('target_inventory', 'N/A')}
    </p>

    <p>
    <b>Estimated Profit:</b>
    ${restock.get('estimated_profit', 0):,.0f}
    </p>

    </div>

    """

    return html


def render_risk_rationale(data, restock):

    if not isinstance(data, dict):
        return f"<p>{data}</p>"

    risk_level = data.get(
        "risk_level",
        "UNKNOWN"
    )

    reasons = data.get(
        "risk_reasons",
        []
    )

    volatility = data.get(
        "volatility_reasoning",
        "No volatility analysis available."
    )

    html = f"""

    <div class="risk-card">

    <h3>Risk Intelligence</h3>

    <p>
    <b>Risk Level:</b>
    {risk_level}
    </p>

    <p>
    <b>Primary Risk Factors:</b>
    </p>

    {render_bullet_list(reasons)}

    <p>
    <b>Volatility Analysis:</b>
    </p>

    <p>{volatility}</p>

    <hr>

    <p>
    <b>Sellout Probability:</b>
    {safe_percentage(restock.get('sellout_probability', 0))}
    </p>

    <p>
    <b>Overstock Probability:</b>
    {safe_percentage(restock.get('overstock_probability', 0))}
    </p>

    </div>

    """

    return html


def render_decision_trace(trace):

    if not isinstance(trace, list):

        return """
        <div class="timeline-card">
        No timeline available.
        </div>
        """

    html = ""

    for step in trace:

        if isinstance(step, dict):

            agent = step.get(
                "agent",
                "Unknown Agent"
            )

            decision = step.get(
                "decision",
                "No decision available."
            )

            evidence = step.get(
                "evidence",
                "No evidence available."
            )

            html += f"""

            <div class="timeline-card">

            <h4>{agent}</h4>

            <p>
            <b>Decision:</b>
            {decision}
            </p>

            <p>
            <b>Evidence:</b>
            </p>

            <p>{evidence}</p>

            </div>

            """

        else:

            html += f"""

            <div class="timeline-card">

            <p>{step}</p>

            </div>

            """

    return html


def render_consensus_panel(data):

    if not isinstance(data, dict):

        return """
        <div class="consensus-card">
        No consensus intelligence available.
        </div>
        """

    final_decision = data.get(
        "final_decision",
        "No decision available."
    )

    consensus_score = data.get(
        "consensus_score",
        0
    )

    evidence_chain = data.get(
        "evidence_chain",
        []
    )

    conflicts = data.get(
        "conflicting_agents",
        []
    )

    risk_override = data.get(
        "risk_override",
        {}
    )

    override_active = risk_override.get(
        "override",
        False
    )

    override_reason = risk_override.get(
        "reason",
        "No override reason."
    )

    supporting_agents = data.get(
        "supporting_agents",
        []
    )

    html = f"""

    <div class="consensus-card">

    <h3>Consensus Intelligence</h3>

    <p>
    <b>Final Executive Decision:</b>
    </p>

    <p>{final_decision}</p>

    <hr>

    <p>
    <b>Consensus Score:</b>
    {safe_percentage(consensus_score)}
    </p>

    <p>
    <b>Supporting Systems:</b>
    </p>

    {render_bullet_list(supporting_agents)}

    <hr>

    <p>
    <b>Consensus Evidence:</b>
    </p>

    {render_bullet_list(evidence_chain)}

    """

    # ===================================
    # CONFLICTS
    # ===================================

    if conflicts:

        html += f"""

        <hr>

        <div class="conflict-box">

        <h4>Conflict Detection</h4>

        {render_bullet_list(conflicts)}

        </div>

        """

    # ===================================
    # RISK OVERRIDE
    # ===================================

    if override_active:

        html += f"""

        <hr>

        <div class="override-box">

        <h4>Executive Review Required</h4>

        <p>{override_reason}</p>

        </div>

        """

    html += "</div>"

    return html

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

.explainability-card {
    background: linear-gradient(
        135deg,
        #0F172A,
        #1E293B
    );

    border: 1px solid #475569;

    border-radius: 18px;

    padding: 22px;

    margin-top: 1rem;
    margin-bottom: 1rem;
}

.confidence-card {
    background: linear-gradient(
        135deg,
        #1E293B,
        #0F172A
    );

    border: 1px solid #38BDF8;

    border-radius: 16px;

    padding: 20px;

    margin-top: 1rem;
}

.financial-card {
    background: linear-gradient(
        135deg,
        #052E16,
        #14532D
    );

    border: 1px solid #22C55E;

    border-radius: 16px;

    padding: 20px;

    margin-top: 1rem;
}

.risk-card {
    background: linear-gradient(
        135deg,
        #3F0D12,
        #641220
    );

    border: 1px solid #EF4444;

    border-radius: 16px;

    padding: 20px;

    margin-top: 1rem;
}

.timeline-card {
    background: linear-gradient(
        135deg,
        #111827,
        #1F2937
    );

    border-left: 4px solid #3B82F6;

    padding: 18px;

    border-radius: 12px;

    margin-bottom: 14px;
}

.consensus-card {
    background: linear-gradient(
        135deg,
        #111827,
        #1E293B
    );

    border: 1px solid #8B5CF6;

    border-radius: 18px;

    padding: 24px;

    margin-top: 1.5rem;
    margin-bottom: 1.5rem;

    box-shadow:
    0px 4px 20px rgba(139,92,246,0.2);
}

.conflict-box {
    background-color: rgba(239,68,68,0.12);

    border: 1px solid #EF4444;

    border-radius: 12px;

    padding: 16px;

    margin-top: 1rem;
}

.override-box {
    background-color: rgba(245,158,11,0.12);

    border: 1px solid #F59E0B;

    border-radius: 12px;

    padding: 16px;

    margin-top: 1rem;
}

.monitoring-card {
    background: linear-gradient(
        135deg,
        #0F172A,
        #111827
    );
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 1rem;
}

.alert-card-high {
    background: linear-gradient(
        135deg,
        #450A0A,
        #7F1D1D
    );
    border: 1px solid #EF4444;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 14px;
}

.alert-card-medium {
    background: linear-gradient(
        135deg,
        #78350F,
        #92400E
    );
    border: 1px solid #F59E0B;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 14px;
}

.alert-card-low {
    background: linear-gradient(
        135deg,
        #1E3A8A,
        #1D4ED8
    );
    border: 1px solid #3B82F6;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 14px;
}

.summary-card {
    background: linear-gradient(
        135deg,
        #111827,
        #1E293B
    );
    border: 1px solid #10B981;
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 1rem;
}

.badge {
    display: inline-block;

    padding: 8px 14px;

    border-radius: 999px;

    margin-right: 8px;
    margin-top: 8px;

    font-size: 0.85rem;

    font-weight: 600;

    color: white;
}

.badge-green {
    background-color: #166534;
}

.badge-red {
    background-color: #991B1B;
}

.badge-blue {
    background-color: #1D4ED8;
}

.badge-yellow {
    background-color: #92400E;
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
    st.success("Explainability Engine Active")
    st.success("Temporal Intelligence Online")

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
    - Explainability Intelligence
    - Decision Traceability

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

    data = st.session_state.analysis_data

    if "error" in data:

        st.error(
            f"Backend Analysis Error:\n\n{data['error']}"
        )

        st.stop()

    metrics = data.get("metrics", {})
    report = data.get("report", "")
    temporal_insights = data.get(
        "temporal_insights",
        []
    )

    # ===================================
    # EXECUTIVE METRICS
    # ===================================

    st.header("Executive Metrics")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:

        st.markdown(f"""

        <div class="metric-card">

        <div class="small-label">
        Revenue Opportunity
        </div>

        <div class="big-number">
        ${metrics.get('total_revenue_opportunity',0):,.0f}
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
        ${metrics.get('total_inventory_risk',0):,.0f}
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
        {metrics.get('top_trend_momentum','N/A')}
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
        {metrics.get('average_confidence','N/A')}
        </div>

        </div>

        """, unsafe_allow_html=True)

    with col5:

        st.markdown(f"""

        <div class="metric-card">

        <div class="small-label">
        Avg Consensus
        </div>

        <div class="big-number">
        {safe_percentage(metrics.get('average_consensus_score',0))}
        </div>

        </div>

        """, unsafe_allow_html=True)

    with col6:

        st.markdown(f"""

        <div class="metric-card">

        <div class="small-label">
        Risk Overrides
        </div>

        <div class="big-number">
        {metrics.get('total_consensus_overrides',0)}
        </div>

        </div>

        """, unsafe_allow_html=True)

    # ===================================
    # VISUAL ANALYTICS
    # ===================================

    trend_df = pd.DataFrame(
        metrics.get("trend_insights", [])
    )

    if not trend_df.empty:

        st.header("Visual Intelligence")

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
    # SIMULATIONS
    # ===================================

    st.header("Scenario Simulations")

    for simulation in metrics.get(
        "simulation_results",
        []
    ):

        restock = simulation.get(
            "restock",
            {}
        )

        st.markdown(f"""

        <div class="executive-panel">

        <h2>{simulation.get('product','Unknown Product')}</h2>

        <p>
        <b>Trend:</b>
        {simulation.get('trend','N/A')}
        </p>

        <hr>

        <p>
        <b>Recommended Restock:</b>
        {restock.get('recommended_restock','N/A')}
        </p>

        <p>
        <b>Revenue Forecast:</b>
        ${restock.get('estimated_revenue_gain',0):,.0f}
        </p>

        <p>
        <b>Estimated ROI:</b>
        {restock.get('estimated_roi','N/A')}%
        </p>

        <p>
        <b>Inventory Health Score:</b>
        {restock.get('inventory_health_score','N/A')}
        </p>

        <p>
        <b>Demand Label:</b>
        {restock.get('demand_label','N/A')}
        </p>

        </div>

        """, unsafe_allow_html=True)

        # ===================================
        # BADGES
        # ===================================

        badge_html = ""

        if restock.get("stockout_risk") in [
            "HIGH",
            "CRITICAL"
        ]:

            badge_html += """
            <span class="badge badge-red">
            HIGH SELLOUT RISK
            </span>
            """

        if restock.get("inventory_risk") == "LOW":

            badge_html += """
            <span class="badge badge-green">
            LOW INVENTORY RISK
            </span>
            """

        if restock.get("trend_strength",0) >= 0.7:

            badge_html += """
            <span class="badge badge-blue">
            STRONG DEMAND
            </span>
            """

        if restock.get("overstock_probability",1) <= 0.2:

            badge_html += """
            <span class="badge badge-yellow">
            LOW OVERSTOCK RISK
            </span>
            """

        st.markdown(
            badge_html,
            unsafe_allow_html=True
        )

        # ===================================
        # RECOMMENDATION EXPLANATION
        # ===================================

        decision_explanation = restock.get(
            "decision_explanation",
            {}
        )

        st.markdown(
            render_decision_explanation(
                decision_explanation
            ),
            unsafe_allow_html=True
        )

        # ===================================
        # CONFIDENCE INSIGHTS
        # ===================================

        confidence_explanation = restock.get(
            "confidence_explanation",
            {}
        )

        st.markdown(
            render_confidence_explanation(
                confidence_explanation
            ),
            unsafe_allow_html=True
        )

        # ===================================
        # FINANCIAL RATIONALE
        # ===================================

        financial_rationale = restock.get(
            "financial_rationale",
            {}
        )

        st.markdown(
            render_financial_rationale(
                financial_rationale,
                restock
            ),
            unsafe_allow_html=True
        )

        # ===================================
        # RISK RATIONALE
        # ===================================

        risk_rationale = restock.get(
            "risk_rationale",
            {}
        )

        st.markdown(
            render_risk_rationale(
                risk_rationale,
                restock
            ),
            unsafe_allow_html=True
        )

        # ===================================
        # CONSENSUS INTELLIGENCE
        # ===================================

        st.subheader(
            "Executive Consensus Intelligence"
        )

        consensus_data = simulation.get(
            "consensus",
            {}
        )

        st.markdown(
            render_consensus_panel(
                consensus_data
            ),
            unsafe_allow_html=True
        )

        # ===================================
        # DECISION TRACE
        # ===================================

        st.subheader(
            "Agent Decision Timeline"
        )

        decision_trace = restock.get(
            "decision_trace",
            []
        )

        st.markdown(
            render_decision_trace(
                decision_trace
            ),
            unsafe_allow_html=True
        )

    # ===================================
    # DOWNLOAD REPORT
    # ===================================

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