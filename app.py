import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="EcoNano AI",
    page_icon="🌿",
    layout="wide"
)

# =========================
# COLORFUL WEBSITE DESIGN
# =========================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #e0fff1,
        #e3f4ff,
        #f0e7ff
    );
    color: #173c35;
}

.main-title {
    font-size: 52px;
    font-weight: 900;
    color: #00875a;
}

.subtitle {
    font-size: 19px;
    color: #24647a;
}

div[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        #b9f6d3,
        #b9e8ff
    );
    padding: 24px;
    border-radius: 18px;
    border: 2px solid #65cba0;
    box-shadow: 0 5px 15px rgba(0,100,80,0.12);
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #075b46 !important;
}

h1, h2, h3 {
    color: #075b46 !important;
}

.stButton button {
    background: linear-gradient(
        90deg,
        #00a86b,
        #008acb
    );
    color: white !important;
    border-radius: 12px;
    font-weight: bold;
    border: none;
    padding: 12px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #b9f6d3,
        #c5e8ff,
        #e5d6ff
    );
}

div[data-testid="stExpander"] {
    background: #d9fff0;
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================

st.markdown(
    '<div class="main-title">🌿 EcoNano AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Intelligent Nanotechnology for Sustainable Water Remediation</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================
# NAVIGATION
# =========================

st.sidebar.title("🌱 EcoNano AI")

page = st.sidebar.radio(
    "Explore Platform",
    [
        "🏠 Home",
        "💧 Water Analyzer",
        "🧬 Material Explorer",
        "📊 AI Comparison",
        "🌍 Sustainability",
        "ℹ️ About Us"
    ]
)


materials = {
    "ZnO Nanoparticles": 0.78,
    "Titanium Dioxide": 0.82,
    "Magnetite": 0.73,
    "Biochar Composite": 0.85
}


# =========================
# HOME PAGE
# =========================

if page == "🏠 Home":

    st.header("Welcome to EcoNano AI 🌎")

    st.write(
        "An interactive research platform exploring "
        "nanomaterials and artificial intelligence "
        "for sustainable water treatment."
    )

    a, b, c = st.columns(3)

    a.metric("🧬 Materials", "4", "Candidates explored")
    b.metric("💧 Pollutant Groups", "3", "Research categories")
    c.metric("🌱 Research Focus", "Sustainability")

    st.divider()

    st.subheader("Explore Our Technology")

    col1, col2 = st.columns(2)

    with col1:

        st.info("""
        💧 WATER ANALYSIS

        Explore hypothetical water-treatment scenarios.
        """)

        st.success("""
        🧬 NANOMATERIAL EXPLORER

        Discover candidate nanomaterials.
        """)

    with col2:

        st.warning("""
        🤖 AI PREDICTIONS

        Explore illustrative model calculations.
        """)

        st.info("""
        🌍 ENVIRONMENTAL IMPACT

        Explore sustainability and safety considerations.
        """)

    st.divider()

    st.subheader("Our Mission 🌿")

    st.write(
        "Connecting environmental chemistry, "
        "nanotechnology and computational research "
        "to support sustainable water remediation."
    )

    st.image(
        "https://images.unsplash.com/photo-1437482078695-73f5ca6c96e2?w=1200",
        use_container_width=True
    )


# =========================
# WATER ANALYZER
# =========================

elif page == "💧 Water Analyzer":

    st.header("💧 Water Quality Analyzer")

    st.write(
        "Configure a hypothetical treatment scenario."
    )

    with st.form("analysis_form"):

        pollutant = st.selectbox(
            "Pollutant Category",
            ["Dye", "Heavy Metal Ion", "Pharmaceutical"]
        )

        concentration = st.slider(
            "Initial Concentration (mg/L)",
            1, 100, 25
        )

        ph = st.slider(
            "Water pH",
            2.0, 12.0, 7.0
        )

        time = st.slider(
            "Contact Time (minutes)",
            10, 240, 60
        )

        material = st.selectbox(
            "Select Nanomaterial",
            list(materials.keys())
        )

        analyze = st.form_submit_button(
            "🚀 Analyze Water Sample"
        )

    if analyze:

        ph_factor = max(
            0.55,
            1 - abs(ph - 7) * 0.045
        )

        time_factor = min(time / 100, 1)

        concentration_factor = max(
            0.65,
            1 - concentration / 250
        )

        pollutant_factor = {
            "Dye": 1.0,
            "Heavy Metal Ion": 0.90,
            "Pharmaceutical": 0.85
        }[pollutant]

        estimate = (
            materials[material]
            * ph_factor
            * time_factor
            * concentration_factor
            * pollutant_factor
            * 100
        )

        estimate = min(95, max(0, estimate))

        remaining = concentration * (
            1 - estimate / 100
        )

        st.success("Scenario analysis completed!")

        x, y, z = st.columns(3)

        x.metric(
            "Illustrative Removal Estimate",
            f"{estimate:.1f}%"
        )

        y.metric(
            "Initial Concentration",
            f"{concentration} mg/L"
        )

        z.metric(
            "Remaining Concentration",
            f"{remaining:.2f} mg/L"
        )

        chart = pd.DataFrame({
            "Stage": ["Initial", "Illustrative Remaining"],
            "Concentration": [concentration, remaining]
        })

        fig = px.bar(
            chart,
            x="Stage",
            y="Concentration",
            color="Stage",
            title="Illustrative Concentration Comparison",
            color_discrete_sequence=["#00b894", "#0984e3"]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.warning(
            "This is an illustrative demonstration calculation, "
            "not an experimentally validated AI prediction. "
            "It cannot establish real treatment performance "
            "or drinking-water safety."
        )


# =========================
# MATERIAL EXPLORER
# =========================

elif page == "🧬 Material Explorer":

    st.header("🧬 Nanomaterial Explorer")

    descriptions = {
        "ZnO Nanoparticles":
            "Investigated for photocatalysis and optical sensing.",

        "Titanium Dioxide":
            "Studied for photocatalytic pollutant degradation.",

        "Magnetite":
            "Magnetic iron oxide investigated for separation applications.",

        "Biochar Composite":
            "Carbon-based material investigated for adsorption."
    }

    for name, description in descriptions.items():

        with st.expander("🔬 " + name):

            st.write(description)

            st.info(
                "Research candidate — experimental performance "
                "must be independently established."
            )


# =========================
# AI COMPARISON
# =========================

elif page == "📊 AI Comparison":

    st.header("📊 Material Comparison Dashboard")

    comparison = pd.DataFrame({
        "Material": list(materials.keys()),
        "Illustrative Score": [
            value * 100
            for value in materials.values()
        ]
    })

    fig = px.bar(
        comparison,
        x="Material",
        y="Illustrative Score",
        color="Material",
        title="Illustrative Material Scores",
        text_auto=".1f",
        color_discrete_sequence=[
            "#00b894",
            "#0984e3",
            "#6c5ce7",
            "#e17055"
        ]
    )

    fig.update_layout(
        yaxis_title="Demonstration score (not measured efficiency)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Scores are illustrative demonstration values, "
        "not measured material performance."
    )


# =========================
# SUSTAINABILITY
# =========================

elif page == "🌍 Sustainability":

    st.header("🌍 Sustainability Center")

    st.write(
        "Evaluate important environmental considerations "
        "when researching nanomaterial-based water treatment."
    )

    factors = [
        "Nanoparticle toxicity assessment",
        "Material recovery and reuse",
        "Energy consumption",
        "Chemical waste generation",
        "Lifecycle environmental impact",
        "Secondary pollution risk"
    ]

    st.subheader("Environmental Research Checklist")

    for factor in factors:

        st.checkbox(
            factor,
            key=factor
        )

    st.info(
        "This checklist supports research planning. "
        "It is not an environmental safety certification."
    )


# =========================
# ABOUT
# =========================

elif page == "ℹ️ About Us":

    st.header("About EcoNano AI 🌿")

    st.write("""
    EcoNano AI is a computational research prototype
    connecting four interdisciplinary areas:

    🧪 Environmental Chemistry

    🧬 Nanomaterials Science

    🤖 Artificial Intelligence

    🌍 Sustainable Water Remediation

    The platform explores computational approaches
    to early-stage environmental research.
    """)

    st.subheader("Technology Stack")

    st.success(
        "Python | Streamlit | Pandas | Plotly | NumPy | Scikit-learn"
    )

    st.subheader("Scientific Limitations")

    st.warning(
        "The current demonstration uses illustrative assumptions "
        "and synthetic data. It is not experimentally validated."
    )


# =========================
# FOOTER
# =========================

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:20px;">
        <h3>🌿 EcoNano AI</h3>
        <p>Science • Innovation • Sustainability</p>
        <p>Building a cleaner future through research.</p>
    </div>
    """,
    unsafe_allow_html=True
)
