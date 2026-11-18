import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="EcoNano AI | Water Innovation Lab",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------------------
# EcoNano AI — educational computational prototype.
# All scores are illustrative heuristics, not measured or validated data.
# -------------------------------------------------------------------
MATERIALS = {
    "ZnO": {
        "fit": ["Dye", "Pharmaceutical"],
        "mechanism": "Photocatalysis: light-generated reactive species may degrade selected organic pollutants.",
        "base": 72, "ph": 7.0, "time": 55, "green": 3.5, "reuse": 3, "cost": 4,
        "caution": "Depends on light source, catalyst loading, water matrix and pollutant chemistry.",
        "tag": "Photocatalyst", "icon": "☀️",
    },
    "TiO₂": {
        "fit": ["Dye", "Pharmaceutical"],
        "mechanism": "Photocatalysis under suitable UV or modified visible-light conditions.",
        "base": 76, "ph": 7.0, "time": 60, "green": 4.0, "reuse": 4, "cost": 3,
        "caution": "Many formulations require UV; reactor and illumination strongly affect performance.",
        "tag": "Photocatalyst", "icon": "✨",
    },
    "Fe₃O₄": {
        "fit": ["Heavy metal ion", "Dye"],
        "mechanism": "Adsorption and magnetic separation; surface modification changes selectivity.",
        "base": 68, "ph": 6.5, "time": 45, "green": 3.5, "reuse": 4, "cost": 3,
        "caution": "Uptake depends on ion identity, surface chemistry, competing ions and pH.",
        "tag": "Magnetic adsorbent", "icon": "🧲",
    },
    "Biochar composite": {
        "fit": ["Heavy metal ion", "Dye", "Pharmaceutical"],
        "mechanism": "Adsorption through porous structure and surface functional groups.",
        "base": 70, "ph": 6.5, "time": 50, "green": 4.5, "reuse": 3, "cost": 4,
        "caution": "Properties vary with feedstock and production conditions; spent adsorbent needs safe handling.",
        "tag": "Bio-based composite", "icon": "🌿",
    },
}
POLLUTANTS = ["Dye", "Heavy metal ion", "Pharmaceutical"]

# ------------------------------- THEME ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@600;700;800&display=swap');
:root {
  --ink:#163b3a; --muted:#587573; --teal:#087f75; --mint:#dff7ed;
  --blue:#e5f3ff; --violet:#f0eaff; --line:#d8ebe5;
}
.stApp {
  background:
    radial-gradient(ellipse at 8% 0%, rgba(172,239,213,.42), transparent 32%),
    radial-gradient(ellipse at 95% 10%, rgba(185,218,255,.42), transparent 30%),
    linear-gradient(135deg,#f7fffb 0%,#f4faff 52%,#fbf8ff 100%);
  color:var(--ink); font-family:'DM Sans',sans-serif;
}
.block-container {max-width:1450px;padding-top:1.5rem;padding-bottom:3rem}
h1,h2,h3 {font-family:'Manrope','DM Sans',sans-serif!important;color:#124b46!important;letter-spacing:-.025em}
p,li,label,.stMarkdown {color:#294c49}
[data-testid="stSidebar"] {
  background:linear-gradient(180deg,#e1f8ed 0%,#e8f4ff 58%,#f0eaff 100%);
  border-right:1px solid #d5e9e3;
}
[data-testid="stSidebar"] * {color:#183f3a}
[data-testid="stSidebar"] [data-testid="stRadio"] label {font-weight:600}
.hero {
  position:relative; overflow:hidden; padding:2.2rem 2.3rem; border-radius:28px;
  background:linear-gradient(115deg,#c9f5df 0%,#d8f0ff 57%,#e9ddff 100%);
  border:1px solid #c6e9df; box-shadow:0 14px 40px rgba(35,105,91,.09);
}
.hero:after {content:'💧';position:absolute;right:5%;top:8%;font-size:6rem;opacity:.16}
.hero-kicker {font-size:.76rem;text-transform:uppercase;letter-spacing:.18em;font-weight:800;color:#087f68}
.hero h1 {font-size:clamp(2.4rem,5vw,4rem);margin:.25rem 0;color:#103f3b!important}
.hero p {font-size:1.08rem;max-width:780px;color:#315c57;margin-bottom:.2rem}
.section-kicker {font-size:.75rem;text-transform:uppercase;letter-spacing:.16em;font-weight:800;color:#07836f}
.feature-card {
  min-height:155px;padding:1.25rem;border-radius:20px;color:#fff!important;
  background:linear-gradient(145deg,#123f42,#126b70 65%,#267e91);
  border:1px solid rgba(255,255,255,.18);box-shadow:0 10px 26px rgba(16,75,75,.13);
}
.feature-card h3,.feature-card p,.feature-card span {color:#fff!important}
.feature-card h3 {font-size:1.08rem!important;margin:.25rem 0}
.feature-card p {font-size:.9rem;opacity:.9}
.info-card {
  background:rgba(255,255,255,.84);border:1px solid var(--line);border-radius:18px;
  padding:1.15rem 1.25rem;box-shadow:0 8px 22px rgba(31,91,79,.055);
}
.callout {
  background:linear-gradient(90deg,#fff8df,#fffdf4);border:1px solid #f0dfaa;
  border-left:5px solid #e2b83f;border-radius:13px;padding:.9rem 1.05rem;color:#66531e;
}
.success-panel {
  background:linear-gradient(110deg,#dff8eb,#e5f5ff);border:1px solid #c7e9dc;
  border-radius:18px;padding:1.1rem 1.3rem;
}
div[data-testid="stMetric"] {
  background:rgba(255,255,255,.9);border:1px solid #d8ebe5;border-radius:17px;
  padding:15px 16px;box-shadow:0 7px 20px rgba(28,87,75,.05);
}
div[data-testid="stMetric"] label {color:#5b7772!important;font-weight:700}
div[data-testid="stMetricValue"] {color:#087b67!important;font-weight:800}
.stButton>button,.stDownloadButton>button {
  background:linear-gradient(100deg,#07876d,#087fa5);color:white;border:0;
  border-radius:13px;font-weight:800;min-height:2.8rem;box-shadow:0 7px 17px rgba(8,127,117,.16);
}
.stButton>button:hover,.stDownloadButton>button:hover {
  color:white;border:0;filter:brightness(1.06);transform:translateY(-1px);
}
div[data-baseweb="select"]>div, .stSlider, [data-testid="stNumberInput"] {
  border-radius:12px;
}
hr {border-color:#dcece7}
.stTabs [data-baseweb="tab"] {font-weight:700}
.stTabs [aria-selected="true"] {color:#087b67!important}
[data-testid="stDataFrame"] {border:1px solid #dcece7;border-radius:14px;overflow:hidden}
small {color:#617b76}
</style>
""", unsafe_allow_html=True)

# ------------------------------ HELPERS -----------------------------
def score(material, pollutant, concentration, ph, minutes):
    """Transparent demonstration heuristic; not a physical model."""
    d = MATERIALS[material]
    compatibility = 1.0 if pollutant in d["fit"] else 0.82
    ph_factor = max(0.55, 1 - abs(ph - d["ph"]) * 0.055)
    time_factor = 1 - np.exp(-max(minutes, 1) / d["time"])
    concentration_factor = 1 / (1 + 0.12 * max(concentration, 0))
    value = d["base"] * compatibility * ph_factor * (0.35 + 0.75 * time_factor) * concentration_factor
    return float(np.clip(value, 5, 95))

def compare(pollutant, concentration, ph, minutes):
    rows = []
    for name, details in MATERIALS.items():
        rows.append({
            "Material": name,
            "Illustrative score (%)": round(score(name, pollutant, concentration, ph, minutes), 1),
            "Pollutant fit": "Good research fit" if pollutant in details["fit"] else "Needs validation",
            "Green profile (1–5)": details["green"],
            "Reusability (1–5)": details["reuse"],
            "Relative cost score (1–5)": details["cost"],
        })
    return pd.DataFrame(rows).sort_values("Illustrative score (%)", ascending=False).reset_index(drop=True)

def plot_layout(fig, height=390):
    fig.update_layout(
        height=height, paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,.78)",
        font=dict(family="DM Sans, sans-serif", color="#315550"),
        title_font=dict(size=18, color="#164b45"),
        margin=dict(l=18, r=18, t=58, b=22),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(gridcolor="#e4efeb", zeroline=False),
        legend_title_text="",
    )
    return fig

def report_html(inputs, ranked):
    rows = "".join(
        f"<tr><td>{r['Material']}</td><td>{r['Illustrative score (%)']}</td><td>{r['Pollutant fit']}</td></tr>"
        for _, r in ranked.iterrows()
    )
    return f"""<!doctype html><html><meta charset="utf-8"><title>EcoNano AI scenario report</title>
    <body style="font-family:Arial,sans-serif;margin:40px;color:#173b36;background:#f6fffb">
    <div style="background:linear-gradient(110deg,#d9f8e8,#e1f1ff);padding:28px;border-radius:18px">
    <h1>💧 EcoNano AI — Scenario Report</h1><p>Computational water-remediation exploration</p></div>
    <p>Generated: {datetime.now():%Y-%m-%d %H:%M}</p>
    <h2>Scenario inputs</h2><p>Pollutant: {inputs['pollutant']} | Concentration: {inputs['concentration']} mg/L |
    pH: {inputs['ph']} | Contact time: {inputs['minutes']} min</p>
    <h2>Candidate comparison</h2><table style="border-collapse:collapse" border="1" cellpadding="10">
    <tr style="background:#dff5eb"><th>Material</th><th>Illustrative score</th><th>Fit</th></tr>{rows}</table>
    <p style="background:#fff4d6;padding:14px;border-radius:8px"><b>Important limitation:</b>
    Scores are demonstration heuristic outputs, not experimental data or validated AI predictions.
    They do not establish actual removal efficiency or drinking-water safety.</p></body></html>""".encode("utf-8")

def show_science_note(text="Scores are illustrative heuristic outputs, not measured removal efficiencies or validated predictions."):
    st.markdown(f'<div class="callout">🔎 <b>Scientific note:</b> {text}</div>', unsafe_allow_html=True)

def material_cards():
    cols = st.columns(4)
    for col, (name, d) in zip(cols, MATERIALS.items()):
        with col:
            st.markdown(
                f'<div class="feature-card"><div style="font-size:1.7rem">{d["icon"]}</div>'
                f'<h3>{name}</h3><p>{d["tag"]}</p></div>',
                unsafe_allow_html=True,
            )

# ------------------------------- SIDEBAR ----------------------------
st.sidebar.markdown("## 💧 EcoNano AI")
st.sidebar.caption("NANOTECHNOLOGY • WATER INNOVATION")
page = st.sidebar.radio(
    "EXPLORE THE PLATFORM",
    ["Home", "Water Analyzer", "What-if Simulator", "Material Explorer",
     "AI Comparison", "Sustainability", "Research Library", "About & Limitations"],
)
st.sidebar.divider()
st.sidebar.markdown("**Prototype status**")
st.sidebar.success("Computational demo")
st.sidebar.caption("No live sensor or laboratory data is connected.")
st.sidebar.markdown("---")
st.sidebar.caption("Built around green chemistry, nanomaterials and responsible innovation.")

# -------------------------------- HOME ------------------------------
if page == "Home":
    st.markdown("""
    <div class="hero">
      <div class="hero-kicker">Green chemistry • Nanotechnology • Water innovation</div>
      <h1>EcoNano AI</h1>
      <p>Explore candidate nanomaterials for water remediation, compare hypothetical treatment
      conditions and discover the science behind responsible water-treatment research.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    cols = st.columns(4)
    home_cards = [
        ("🧪", "Water Analyzer", "Explore a pollutant scenario and compare candidate materials."),
        ("⚙️", "What-if Simulator", "See how the illustrative score changes with pH and contact time."),
        ("🔬", "Material Explorer", "Discover four candidate nanomaterials and their mechanisms."),
        ("🌱", "Sustainability", "Compare indicative green-profile and reuse considerations."),
    ]
    for col, (icon, title, desc) in zip(cols, home_cards):
        with col:
            st.markdown(
                f'<div class="feature-card"><div style="font-size:1.8rem">{icon}</div>'
                f'<h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True
            )
    st.write("")
    st.markdown('<div class="section-kicker">THE CHALLENGE</div>', unsafe_allow_html=True)
    st.subheader("Cleaner water needs smarter material choices.")
    st.write(
        "Different contaminants behave differently. No single nanomaterial is universally best. "
        "EcoNano AI is an educational interface for exploring research candidates—not a treatment "
        "control system or a substitute for experimental validation."
    )
    st.markdown("### 🧬 Candidate material landscape")
    material_cards()
    st.write("")
    show_science_note("Current scores are generated by a transparent demonstration formula. "
                      "They are not trained-model predictions, experimental findings or certified treatment results.")

# --------------------------- WATER ANALYZER -------------------------
elif page == "Water Analyzer":
    st.markdown('<div class="section-kicker">SCENARIO WORKSPACE</div>', unsafe_allow_html=True)
    st.title("🧪 Water Analyzer")
    st.write("Set up a hypothetical contaminated-water scenario to explore candidate materials.")
    with st.form("water_analysis_form"):
        left, right = st.columns(2)
        with left:
            pollutant = st.selectbox("Pollutant category", POLLUTANTS, key="wa_pollutant")
            concentration = st.slider("Initial concentration (mg/L)", 1, 200, 50, key="wa_concentration")
        with right:
            ph = st.slider("Water pH", 2.0, 12.0, 7.0, 0.1, key="wa_ph")
            minutes = st.slider("Contact time (minutes)", 5, 240, 60, 5, key="wa_minutes")
        run = st.form_submit_button("✨ Analyze scenario", use_container_width=True)
    if run:
        ranked = compare(pollutant, concentration, ph, minutes)
        st.session_state["analysis_result"] = {
            "pollutant": pollutant, "concentration": concentration,
            "ph": ph, "minutes": minutes, "ranked": ranked,
        }
    if "analysis_result" in st.session_state:
        data = st.session_state["analysis_result"]
        ranked = data["ranked"]
        best = ranked.iloc[0]
        st.divider()
        st.markdown('<div class="section-kicker">YOUR SCENARIO RESULTS</div>', unsafe_allow_html=True)
        st.subheader("Candidate screening overview")
        m1, m2, m3 = st.columns(3)
        m1.metric("🏆 Top heuristic candidate", best["Material"])
        m2.metric("Illustrative score", f"{best['Illustrative score (%)']}%")
        m3.metric("Contact time", f"{data['minutes']} min")
        chart = px.bar(
            ranked, x="Material", y="Illustrative score (%)", color="Material",
            text="Illustrative score (%)", title="Candidate comparison • illustrative score",
            color_discrete_sequence=["#0b8f78", "#3199bd", "#8b75c9", "#e0a64b"],
        )
        chart.update_traces(textposition="outside", marker_line_width=0)
        chart.update_yaxes(range=[0, 108], title="Illustrative score (%)")
        st.plotly_chart(plot_layout(chart, 410), use_container_width=True)
        st.subheader("📊 Detailed comparison")
        st.dataframe(ranked, use_container_width=True, hide_index=True)
        st.markdown(
            f'<div class="success-panel"><b>Leading candidate in this scenario: {best["Material"]}</b><br>'
            f'{MATERIALS[best["Material"]]["mechanism"]}</div>', unsafe_allow_html=True
        )
        st.write("")
        show_science_note("A higher score only means the candidate ranks higher under this app's assumptions. "
                          "It does not prove real-world removal efficiency or drinking-water safety.")
        st.download_button(
            "⬇️ Download scenario report (HTML)",
            report_html(data, ranked), "econano_scenario_report.html", "text/html",
            use_container_width=True,
        )
    else:
        st.info("👆 Enter scenario conditions above and select **Analyze scenario** to generate your comparison.")

# ------------------------- WHAT-IF SIMULATOR ------------------------
elif page == "What-if Simulator":
    st.markdown('<div class="section-kicker">PARAMETER EXPLORER</div>', unsafe_allow_html=True)
    st.title("⚙️ What-if Treatment Simulator")
    st.write("Explore how the demonstration score responds to selected scenario inputs.")
    c1, c2, c3 = st.columns(3)
    material = c1.selectbox("Nanomaterial", list(MATERIALS), key="sim_material")
    pollutant = c1.selectbox("Pollutant category", POLLUTANTS, key="sim_pollutant")
    concentration = c2.slider("Concentration (mg/L)", 1, 200, 50, key="sim_concentration")
    ph = c2.slider("Water pH", 2.0, 12.0, 7.0, 0.1, key="sim_ph")
    minutes = c3.slider("Contact time (min)", 5, 240, 60, 5, key="sim_minutes")
    current = score(material, pollutant, concentration, ph, minutes)
    st.metric("Illustrative screening score", f"{current:.1f}%")
    time_values = np.arange(5, 241, 5)
    fig_time = go.Figure(go.Scatter(
        x=time_values, y=[score(material, pollutant, concentration, ph, t) for t in time_values],
        mode="lines", line=dict(width=4, color="#078b78"), fill="tozeroy",
        fillcolor="rgba(7,139,120,.10)", name="Illustrative score",
    ))
    fig_time.add_vline(x=minutes, line_dash="dash", line_color="#8b75c9",
                       annotation_text="Selected time")
    fig_time.update_layout(title="Illustrative score versus contact time",
                           xaxis_title="Contact time (minutes)", yaxis_title="Illustrative score (%)",
                           yaxis_range=[0, 100])
    st.plotly_chart(plot_layout(fig_time), use_container_width=True)
    ph_values = np.round(np.arange(2, 12.1, .2), 1)
    fig_ph = px.line(
        x=ph_values, y=[score(material, pollutant, concentration, p, minutes) for p in ph_values],
        labels={"x": "Water pH", "y": "Illustrative score (%)"},
        title="Illustrative score versus pH",
    )
    fig_ph.update_traces(line=dict(width=4, color="#7d69bd"))
    fig_ph.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(plot_layout(fig_ph), use_container_width=True)
    show_science_note("These curves are produced by a demonstration heuristic, not fitted adsorption or kinetic data.")

# --------------------------- MATERIAL EXPLORER ----------------------
elif page == "Material Explorer":
    st.markdown('<div class="section-kicker">NANOMATERIAL KNOWLEDGE BASE</div>', unsafe_allow_html=True)
    st.title("🔬 Nanomaterial Explorer")
    material_name = st.selectbox("Choose a candidate material", list(MATERIALS), key="explorer_material")
    details = MATERIALS[material_name]
    st.markdown(
        f'<div class="hero"><div class="hero-kicker">{details["tag"]}</div>'
        f'<h1>{details["icon"]} {material_name}</h1>'
        f'<p>Potential research fit: {", ".join(details["fit"])}</p></div>',
        unsafe_allow_html=True,
    )
    st.write("")
    st.subheader("⚗️ Potential mechanism")
    st.markdown(f'<div class="info-card">{details["mechanism"]}</div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    a.metric("🌱 Indicative green profile", f'{details["green"]}/5')
    b.metric("♻️ Indicative reusability", f'{details["reuse"]}/5')
    c.metric("💰 Relative cost score", f'{details["cost"]}/5')
    st.warning(f'**Research caution:** {details["caution"]}')
    st.subheader("Compare all candidate materials")
    comparison = pd.DataFrame([
        {"Material": n, "Potential fit": ", ".join(d["fit"]),
         "Green profile": d["green"], "Reusability": d["reuse"], "Relative cost": d["cost"]}
        for n, d in MATERIALS.items()
    ])
    st.dataframe(comparison, use_container_width=True, hide_index=True)
    show_science_note("The material ratings are indicative discussion values, not standardized measurements.")

# ----------------------------- AI COMPARISON -----------------------
elif page == "AI Comparison":
    st.markdown('<div class="section-kicker">TRANSPARENT DECISION SUPPORT DEMO</div>', unsafe_allow_html=True)
    st.title("🤖 Material Recommendation & Comparison")
    st.write("This prototype uses a transparent rule-based heuristic, not a trained machine-learning model.")
    a, b, c = st.columns(3)
    pollutant = a.selectbox("Pollutant category", POLLUTANTS, key="ai_pollutant")
    concentration = b.slider("Concentration (mg/L)", 1, 200, 50, key="ai_concentration")
    ph = c.slider("Water pH", 2.0, 12.0, 7.0, .1, key="ai_ph")
    minutes = st.slider("Contact time (min)", 5, 240, 60, 5, key="ai_minutes")
    ranked = compare(pollutant, concentration, ph, minutes)
    best = ranked.iloc[0]
    st.markdown(
        f'<div class="success-panel"><div class="section-kicker">TOP HEURISTIC CANDIDATE</div>'
        f'<h2>{MATERIALS[best["Material"]]["icon"]} {best["Material"]}</h2>'
        f'<p>{MATERIALS[best["Material"]]["mechanism"]}</p></div>', unsafe_allow_html=True
    )
    st.subheader("Ranking and comparison")
    st.dataframe(ranked, use_container_width=True, hide_index=True)
    fig = px.bar(ranked, x="Material", y="Illustrative score (%)", color="Material",
                 title="Rule-based candidate ranking",
                 color_discrete_sequence=["#0b8f78", "#3199bd", "#8b75c9", "#e0a64b"])
    fig.update_traces(textposition="outside")
    fig.update_layout(yaxis_range=[0, 108])
    st.plotly_chart(plot_layout(fig), use_container_width=True)
    st.warning("Do not use this ranking to select a real treatment process without literature review, laboratory validation and safety assessment.")

# ---------------------------- SUSTAINABILITY ------------------------
elif page == "Sustainability":
    st.markdown('<div class="section-kicker">RESPONSIBLE MATERIAL THINKING</div>', unsafe_allow_html=True)
    st.title("🌱 Sustainability Dashboard")
    st.write("Indicative discussion scores only; these are not life-cycle assessment (LCA) results.")
    sustainability = pd.DataFrame([
        {"Material": n, "Green profile": d["green"], "Reusability": d["reuse"], "Relative cost": d["cost"]}
        for n, d in MATERIALS.items()
    ])
    melted = sustainability.melt(id_vars="Material", var_name="Dimension", value_name="Indicative score")
    fig = px.bar(melted, x="Material", y="Indicative score", color="Dimension", barmode="group",
                 title="Indicative sustainability discussion scores (1–5)",
                 color_discrete_sequence=["#078b78", "#5d9fca", "#9b83ca"])
    fig.update_layout(yaxis_range=[0, 5.5], yaxis_dtick=1)
    st.plotly_chart(plot_layout(fig, 430), use_container_width=True)
    st.subheader("🌍 Questions for a real sustainability assessment")
    questions = [
        ("⚡ Energy", "How much energy is needed for synthesis, illumination and treatment?"),
        ("🧪 Precursors", "Are the starting materials hazardous, scarce or resource-intensive?"),
        ("♻️ Recovery", "Can the material be recovered and reused without major performance loss?"),
        ("🐟 Ecotoxicity", "Could nanoparticles leach or affect aquatic organisms?"),
        ("🗑️ End of life", "How will regeneration waste and spent material be safely managed?"),
        ("🔄 Life cycle", "What are the impacts across synthesis, use, recovery and disposal?"),
    ]
    cols = st.columns(2)
    for i, (heading, body) in enumerate(questions):
        with cols[i % 2]:
            st.markdown(f'<div class="info-card"><b>{heading}</b><br>{body}</div>', unsafe_allow_html=True)
            st.write("")
    st.info("A material described as green is not automatically safe. Environmental performance needs evidence across its full life cycle.")

# ---------------------------- RESEARCH LIBRARY ---------------------
elif page == "Research Library":
    st.markdown('<div class="section-kicker">LEARN THE SCIENCE</div>', unsafe_allow_html=True)
    st.title("📚 Research Library")
    st.write("Short topic guides to help structure a literature review.")
    topics = {
        "☀️ Photocatalysis": "ZnO and TiO₂ are studied for light-assisted degradation of selected organic pollutants. Consider wavelength, intensity, catalyst loading, pH and water composition.",
        "🧲 Adsorption": "Biochar and functionalized magnetic materials are studied for uptake of contaminants. Surface area, pore structure, functional groups and competing ions matter.",
        "🧭 Magnetic separation": "Fe₃O₄ composites may offer magnetic recovery; recovery efficiency, particle stability and nanoparticle leaching need testing.",
        "🌿 Green synthesis": "Biological routes are researched as alternatives for nanoparticle synthesis. Extract composition, reproducibility, purification and waste generation matter.",
        "🐟 Environmental safety": "Assess residual nanoparticles, transformation products, regeneration waste and ecotoxicity, not just pollutant removal.",
    }
    for heading, body in topics.items():
        with st.expander(heading):
            st.write(body)
            st.caption("Literature-review prompt: identify the material composition, experimental conditions, analytical method, controls and limitations in primary studies.")
    st.markdown("### 📑 Build a credible reference list")
    st.write("For each primary paper, record the pollutant, nanomaterial, synthesis route, pH, dose, contact time, light conditions (if relevant), measured removal, reuse cycles and DOI.")
    st.warning("Add verified primary papers and DOI links before treating this page as a formal bibliography. The app's scores are not published experimental findings.")

# ------------------------- ABOUT & LIMITATIONS ---------------------
else:
    st.markdown('<div class="section-kicker">PROJECT TRANSPARENCY</div>', unsafe_allow_html=True)
    st.title("ℹ️ About EcoNano AI")
    st.markdown(
        '<div class="hero"><div class="hero-kicker">Computational educational prototype</div>'
        '<h1>Research exploration, responsibly presented.</h1>'
        '<p>EcoNano AI explores nanomaterial-assisted water remediation through hypothetical scenarios, '
        'transparent heuristic comparisons and educational explanations.</p></div>', unsafe_allow_html=True
    )
    st.subheader("What the prototype currently does")
    st.markdown(
        "- Accepts hypothetical pollutant and treatment-condition inputs\n"
        "- Compares four candidate material categories using an illustrative formula\n"
        "- Visualizes parameter sensitivity for pH and contact time\n"
        "- Provides material mechanisms and sustainability discussion prompts\n"
        "- Generates a downloadable HTML scenario report"
    )
    st.subheader("What it does not do")
    st.markdown(
        "- Does not analyze a real water sample or connect to a sensor\n"
        "- Does not contain a trained or validated machine-learning model\n"
        "- Does not predict certified pollutant removal efficiency\n"
        "- Does not determine drinking-water safety\n"
        "- Does not replace laboratory testing, peer-reviewed evidence or regulatory guidance"
    )
    st.subheader("How the illustrative score is constructed")
    st.write(
        "The heuristic combines a material-specific base value, pollutant-category compatibility, "
        "a hypothetical pH response, a contact-time response and a concentration penalty. "
        "Coefficients are demonstration assumptions, not fitted experimental parameters."
    )
    st.error("Never use this prototype as the sole basis for real water-treatment decisions.")
    st.caption(f"EcoNano AI • Educational prototype • Report timestamp: {datetime.now():%d %b %Y}")
