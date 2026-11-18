
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="EcoNano AI",
    page_icon="🌿",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f1f8f3, #ffffff);
}
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #14532d;
}
.subtitle {
    color: #52705d;
    font-size: 17px;
}
div[data-testid="stMetric"] {
    background: #e8f5e9;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #c8e6c9;
}
.stButton button {
    background-color: #16834a;
    color: white;
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<div class="main-title">🌿 EcoNano AI</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Intelligent Nanotechnology for Sustainable Water Remediation</div>',
    unsafe_allow_html=True
)

st.divider()

# Sidebar navigation
st.sidebar.title("🌱 EcoNano Navigation")

page = st.sidebar.radio(
    "Explore Platform",
    [
        "🏠 Dashboard",
        "💧 Water Analyzer",
        "🧬 Material Explorer",
        "📊 Performance Comparison",
        "🌍 Sustainability Center",
        "ℹ️ About Project"
    ]
)

materials = {
    "ZnO Nanoparticles": 0.78,
    "Titanium Dioxide (TiO₂)": 0.82,
    "Magnetite (Fe₃O₄)": 0.73,
    "Biochar Composite": 0.85
}

if page == "🏠 Dashboard":

    st.subheader("Welcome to EcoNano AI")

    st.write(
        "An interactive computational platform exploring "
        "nanomaterial-assisted approaches to water remediation."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Material Candidates", "4")
    c2.metric("Pollutant Categories", "3")
    c3.metric("Research Focus", "Sustainable Water")

    st.subheader("Explore Our Technology")

    col1, col2 = st.columns(2)

    with col1:
        st.info("💧 **Water Analysis**\n\nExplore water-treatment scenarios.")

        st.success("🧬 **Nanomaterial Explorer**\n\nCompare potential materials.")

    with col2:
        st.warning("📊 **AI Predictions**\n\nExplore illustrative model outputs.")

        st.info("🌍 **Environmental Impact**\n\nConsider sustainability and safety.")

    st.divider()

    st.subheader("Our Mission")

    st.write(
        "To connect environmental chemistry, nanotechnology, "
        "and artificial intelligence to support sustainable "
        "water-treatment research."
    )

elif page == "💧 Water Analyzer":

    st.subheader("💧 Interactive Water Quality Analyzer")

    st.write(
        "Configure a hypothetical water-treatment scenario "
        "and explore illustrative predictions."
    )

    with st.form("water_form"):

        pollutant = st.selectbox(
            "Select pollutant",
            ["Dye", "Heavy Metal Ion", "Pharmaceutical"]
        )

        concentration = st.slider(
            "Initial pollutant concentration (mg/L)",
            1, 100, 25
        )

        ph = st.slider(
            "Water pH",
            2.0, 12.0, 7.0, 0.1
        )

        time = st.slider(
            "Contact time (minutes)",
            10, 240, 60
        )

        selected_material = st.selectbox(
            "Select nanomaterial",
            list(materials.keys())
        )

        submitted = st.form_submit_button(
            "🚀 Analyze Water Sample"
        )

    if submitted:

        base = materials[selected_material]

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
            base
            * ph_factor
            * time_factor
            * concentration_factor
            * pollutant_factor
            * 100
        )

        estimate = min(95, max(0, estimate))

        st.success("Scenario analysis completed!")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Illustrative Removal Estimate",
            f"{estimate:.1f}%"
        )

        c2.metric(
            "Initial Concentration",
            f"{concentration} mg/L"
        )

        c3.metric(
            "Selected Material",
            selected_material
        )

        remaining = concentration * (1 - estimate / 100)

        st.subheader("Concentration Scenario")

        chart = pd.DataFrame({
            "Stage": ["Initial", "Illustrative remaining"],
            "Concentration (mg/L)": [
                concentration,
                remaining
            ]
        })

        fig = px.bar(
            chart,
            x="Stage",
            y="Concentration (mg/L)",
            color="Stage",
            title="Illustrative Pollutant Concentration"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.warning(
            "Research disclaimer: This is a demonstration "
            "calculation using illustrative assumptions, not "
            "an experimentally validated prediction. It must "
            "not be used to determine real drinking-water safety."
        )

elif page == "🧬 Material Explorer":

    st.subheader("🧬 Nanomaterial Explorer")

    descriptions = {
        "ZnO Nanoparticles":
            "Zinc oxide nanoparticles are investigated for "
            "photocatalytic and environmental applications.",

        "Titanium Dioxide (TiO₂)":
            "Titanium dioxide is widely researched for "
            "photocatalytic degradation of pollutants.",

        "Magnetite (Fe₃O₄)":
            "Magnetite is a magnetic iron oxide with potential "
            "applications in separation and remediation.",

        "Biochar Composite":
            "Biochar-based materials are investigated for "
            "adsorption and sustainable pollutant management."
    }

    for name, description in descriptions.items():

        with st.expander("🔬 " + name):
            st.write(description)

            if name == "ZnO Nanoparticles":
                st.write("Research focus: photocatalysis and sensing.")

            elif name == "Titanium Dioxide (TiO₂)":
                st.write("Research focus: photocatalytic treatment.")

            elif name == "Magnetite (Fe₃O₄)":
                st.write("Research focus: magnetic separation.")

            else:
                st.write("Research focus: adsorption and waste valorization.")

elif page == "📊 Performance Comparison":

    st.subheader("📊 Compare Candidate Materials")

    st.write(
        "Explore illustrative material scores. "
        "These are demonstration values, not measured efficiencies."
    )

    comparison = pd.DataFrame({
        "Material": list(materials.keys()),
        "Illustrative Score": [
            value * 100 for value in materials.values()
        ]
    })

    fig = px.bar(
        comparison,
        x="Material",
        y="Illustrative Score",
        color="Material",
        title="Illustrative Material Comparison",
        text_auto=".1f"
    )

    fig.update_layout(
        yaxis_title="Demonstration score (not experimental %)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

elif page == "🌍 Sustainability Center":

    st.subheader("🌍 Environmental Sustainability Center")

    st.write(
        "Nanomaterial performance alone does not establish "
        "environmental sustainability."
    )

    factors = [
        "Nanoparticle toxicity assessment",
        "Material recovery and reuse",
        "Energy requirements",
        "Chemical waste generation",
        "Lifecycle environmental impact",
        "Potential secondary pollution"
    ]

    st.markdown("### Sustainability assessment checklist")

    for factor in factors:
        st.checkbox(factor, key=factor)

    st.info(
        "These checks are a research-planning aid, not a "
        "certification of environmental safety."
    )

elif page == "ℹ️ About Project":

    st.subheader("About EcoNano AI")

    st.write("""
    EcoNano AI is a student-developed computational research
    prototype combining:

    - Environmental Chemistry
    - Nanomaterials Science
    - Machine Learning
    - Sustainable Water Remediation

    The platform explores how computational tools can support
    early-stage research into nanomaterial-assisted treatment.

    **Current limitation:** The demonstration calculations use
    illustrative assumptions and synthetic data. They are not
    experimentally validated.
    """)

    st.markdown("### Technology Stack")

    st.write(
        "🐍 Python | 🎈 Streamlit | 📊 Plotly | "
        "🧮 Pandas | 🤖 Machine Learning"
    )

st.divider()

st.markdown(
    "<center>🌿 EcoNano AI | Building a Sustainable Future "
    "Through Science and Innovation</center>",
    unsafe_allow_html=True
)
