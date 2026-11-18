import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="EcoNano AI", page_icon="💧", layout="wide")

# Educational prototype: heuristic scores are illustrative, not validated predictions.
MATERIALS = {
    "ZnO": {"fit":["Dye","Pharmaceutical"],"mechanism":"Photocatalysis: light-generated reactive species may degrade selected organic pollutants.","base":72,"ph":7.0,"time":55,"green":3.5,"reuse":3,"cost":4,"caution":"Depends on light source, catalyst loading, water matrix and pollutant chemistry."},
    "TiO₂": {"fit":["Dye","Pharmaceutical"],"mechanism":"Photocatalysis under suitable UV or modified visible-light conditions.","base":76,"ph":7.0,"time":60,"green":4.0,"reuse":4,"cost":3,"caution":"Many formulations require UV; reactor and illumination strongly affect performance."},
    "Fe₃O₄": {"fit":["Heavy metal ion","Dye"],"mechanism":"Adsorption and magnetic separation; surface modification changes selectivity.","base":68,"ph":6.5,"time":45,"green":3.5,"reuse":4,"cost":3,"caution":"Uptake depends on ion identity, surface chemistry, competing ions and pH."},
    "Biochar composite": {"fit":["Heavy metal ion","Dye","Pharmaceutical"],"mechanism":"Adsorption through porous structure and surface functional groups.","base":70,"ph":6.5,"time":50,"green":4.5,"reuse":3,"cost":4,"caution":"Properties vary with feedstock and production conditions; spent adsorbent needs safe handling."}
}
POLLUTANTS = ["Dye", "Heavy metal ion", "Pharmaceutical"]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
:root{--ink:#173b36;--muted:#496861;--teal:#087f68;--line:#c9e5da}
.stApp{background:linear-gradient(135deg,#f1fff7 0%,#eff8ff 55%,#f7f1ff 100%);font-family:'DM Sans',sans-serif;color:var(--ink)}
.block-container{max-width:1400px;padding-top:1.6rem;padding-bottom:3rem}
h1,h2,h3,h4{color:#124b3e!important}
p,li,label,.stMarkdown{color:#243f3a}
.hero{position:relative;overflow:hidden;padding:2.5rem 2.4rem;border-radius:26px;background:linear-gradient(120deg,#c9f5df,#d5efff 62%,#e9ddff);border:1px solid #b8e3d2;box-shadow:0 14px 36px rgba(22,105,83,.12);animation:heroIn .8s ease-out both}
.hero:after{content:'💧';position:absolute;right:7%;top:14%;font-size:5rem;opacity:.18;animation:floatDrop 3.8s ease-in-out infinite}
.hero h1{font-size:3.3rem;line-height:1.08;margin:.35rem 0}
.hero p{font-size:1.1rem;color:#315f57;max-width:850px}
.eyebrow{letter-spacing:.16em;text-transform:uppercase;color:#087f5b;font-weight:800;font-size:.82rem}
.dark-card{background:linear-gradient(145deg,#123d3b,#175c70);border:1px solid #398b85;border-radius:18px;padding:1.25rem;min-height:150px;color:#fff!important;box-shadow:0 8px 22px rgba(12,67,69,.14);transition:transform .25s ease,box-shadow .25s ease;animation:cardIn .65s ease both}
.dark-card:hover{transform:translateY(-5px);box-shadow:0 14px 28px rgba(12,67,69,.22)}
.dark-card h3,.dark-card p,.dark-card span,.dark-card div{color:#fff!important}
.dark-card h3{font-size:1.12rem}
.dark-card p{line-height:1.5;color:#e8fffa!important}
.feature-strip{margin-top:1.3rem;padding:1rem 1.2rem;border-radius:16px;background:rgba(255,255,255,.78);border:1px solid #d5eae2;color:#315f57}
.note{background:#fff8df;border:1px solid #f0dfa4;border-left:4px solid #d9a91d;border-radius:10px;padding:.8rem 1rem;color:#624d16}
div[data-testid="stMetric"]{background:#fff;border:1px solid #cfe7dc;border-radius:15px;padding:14px;box-shadow:0 5px 16px rgba(20,80,65,.06)}
div[data-testid="stMetric"] label{color:#496861!important}
div[data-testid="stMetricValue"],div[data-testid="stMetricDelta"]{color:#075b46!important}
.stButton>button,.stDownloadButton>button{background:linear-gradient(90deg,#07875f,#087fa8);color:#fff!important;border:0;border-radius:12px;font-weight:700;transition:transform .2s ease,filter .2s ease}
.stButton>button:hover,.stDownloadButton>button:hover{transform:translateY(-2px);filter:brightness(1.07)}
/* Make form controls readable on every page */
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div,div[data-baseweb="textarea"]>div{background:#fff!important;border:1px solid #b9d9cd!important;color:#173b36!important}
div[data-baseweb="select"] *,div[data-baseweb="input"] input,div[data-baseweb="textarea"] textarea{color:#173b36!important;-webkit-text-fill-color:#173b36!important}
ul[role="listbox"]{background:#fff!important}
li[role="option"]{color:#173b36!important}
.stSlider [data-baseweb="slider"]{color:#087f68}
div[data-testid="stAlert"]{border-radius:13px}
div[data-testid="stAlert"] p{color:#243f3a!important}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#e1f8ec,#e5f2ff)}
section[data-testid="stSidebar"] *{color:#173b36}
section[data-testid="stSidebar"] hr{border-color:#b8d9ce}
@keyframes heroIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@keyframes cardIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
@keyframes floatDrop{0%,100%{transform:translateY(0) rotate(-8deg)}50%{transform:translateY(-13px) rotate(8deg)}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important}}
</style>
""", unsafe_allow_html=True)

def score(material, pollutant, concentration, ph, minutes):
    d=MATERIALS[material]
    compatibility=1.0 if pollutant in d["fit"] else 0.82
    ph_factor=max(0.55,1-abs(ph-d["ph"])*0.055)
    time_factor=1-np.exp(-max(minutes,1)/d["time"])
    concentration_factor=1/(1+0.12*max(concentration,0))
    return float(np.clip(d["base"]*compatibility*ph_factor*(0.35+0.75*time_factor)*concentration_factor,5,95))

def compare(pollutant, concentration, ph, minutes):
    rows=[]
    for name,d in MATERIALS.items():
        rows.append({"Material":name,"Illustrative score (%)":round(score(name,pollutant,concentration,ph,minutes),1),
                     "Pollutant fit":"Good research fit" if pollutant in d["fit"] else "Needs validation",
                     "Green profile (1–5)":d["green"],"Reusability (1–5)":d["reuse"],"Relative cost score (1–5)":d["cost"]})
    return pd.DataFrame(rows).sort_values("Illustrative score (%)",ascending=False)

def report_html(inputs, ranked):
    rows="".join(f"<tr><td>{r['Material']}</td><td>{r['Illustrative score (%)']}</td><td>{r['Pollutant fit']}</td></tr>" for _,r in ranked.iterrows())
    return f"""<html><meta charset="utf-8"><title>EcoNano AI report</title><body style="font-family:Arial;margin:40px;color:#173b36">
    <h1>EcoNano AI — Scenario Report</h1><p>Generated: {datetime.now():%Y-%m-%d %H:%M}</p>
    <h2>Inputs</h2><p>Pollutant: {inputs['pollutant']} | Concentration: {inputs['concentration']} mg/L | pH: {inputs['ph']} | Contact time: {inputs['minutes']} min</p>
    <h2>Comparison</h2><table border="1" cellpadding="8" cellspacing="0"><tr><th>Material</th><th>Illustrative score</th><th>Fit</th></tr>{rows}</table>
    <p style="background:#fff4d6;padding:14px"><b>Limitation:</b> Scores come from a demonstration heuristic, not experimental data or a validated AI model. They do not establish actual removal efficiency or drinking-water safety.</p></body></html>""".encode()

st.sidebar.title("💧 EcoNano AI")
st.sidebar.caption("Nanomaterial-assisted water remediation")
page=st.sidebar.radio("Navigate",["Home","Water Analyzer","What-if Simulator","Material Explorer","AI Comparison","Sustainability","Research Library","About & Limitations"])
st.sidebar.caption("Computational educational prototype")

if page=="Home":
    st.markdown("""<div class="hero">
    <div class="eyebrow">Green chemistry&nbsp; • &nbsp;Nanotechnology&nbsp; • &nbsp;Water innovation</div>
    <h1>💧 EcoNano AI</h1>
    <p><b>Smarter exploration for cleaner water.</b><br>Discover nanomaterial research candidates, explore hypothetical treatment conditions and understand the science shaping sustainable water remediation.</p>
    </div>""",unsafe_allow_html=True)
    st.write("")
    st.markdown("<h2 style='text-align:center;margin-bottom:1rem'>Explore the platform</h2>",unsafe_allow_html=True)
    cols=st.columns(4)
    cards=[("🧪 Water Analyzer","Explore pollutant scenarios and compare candidate materials."),("⚙️ What-if Simulator","See how pH, concentration and contact time change the illustrative score."),("🔬 Material Explorer","Discover mechanisms and research considerations for four materials."),("🌱 Sustainability","Compare indicative green profile, reuse and cost considerations.")]
    for i,(c,(title,desc)) in enumerate(zip(cols,cards)):
        with c: st.markdown(f'<div class="dark-card" style="animation-delay:{i*.12}s"><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
    st.markdown("""<div class="feature-strip"><b>🌊 From water challenge to research insight</b><br>
    Explore four candidate materials&nbsp; • &nbsp;Compare three pollutant categories&nbsp; • &nbsp;Visualize treatment scenarios&nbsp; • &nbsp;Export a scenario report</div>""",unsafe_allow_html=True)
    st.write("")
    left,right=st.columns([1.35,1])
    with left:
        st.subheader("Why EcoNano AI?")
        st.write("Different contaminants behave differently, and no single nanomaterial is universally best. EcoNano AI brings together nanotechnology concepts and a simple computational screening interface to help explore research questions.")
    with right:
        st.markdown('<div class="dark-card"><h3>🌍 Our focus</h3><p>Responsible materials research<br>Water remediation concepts<br>Green chemistry awareness<br>Evidence-led scientific exploration</p></div>',unsafe_allow_html=True)
    st.caption("Educational prototype • Scenario scores are illustrative heuristics, not experimental results or validated AI predictions.")

elif page=="Water Analyzer":
    st.title("🧪 Water Analyzer")
    st.write("Enter hypothetical treatment conditions.")
    with st.form("analysis"):
        a,b=st.columns(2)
        pollutant=a.selectbox("Pollutant category",POLLUTANTS)
        concentration=a.slider("Initial concentration (mg/L)",1,200,50)
        ph=b.slider("Water pH",2.0,12.0,7.0,0.1)
        minutes=b.slider("Contact time (minutes)",5,240,60,5)
        run=st.form_submit_button("Analyze scenario",use_container_width=True)
    if run:
        ranked=compare(pollutant,concentration,ph,minutes)
        st.session_state.analysis={"pollutant":pollutant,"concentration":concentration,"ph":ph,"minutes":minutes,"ranked":ranked}
    if "analysis" in st.session_state:
        d=st.session_state.analysis; ranked=d["ranked"]; best=ranked.iloc[0]
        x,y,z=st.columns(3); x.metric("Top candidate",best["Material"]); y.metric("Illustrative score",f"{best['Illustrative score (%)']}%"); z.metric("Scenario pH",d["ph"])
        fig=px.bar(ranked,x="Material",y="Illustrative score (%)",color="Material",text="Illustrative score (%)",title="Illustrative screening scores — not measured removal")
        fig.update_layout(showlegend=False,yaxis_range=[0,100]); st.plotly_chart(fig,use_container_width=True)
        st.dataframe(ranked,use_container_width=True,hide_index=True)
        st.markdown('<div class="note">A higher score reflects this app’s assumptions only. It does not prove real-world removal efficiency or drinking-water safety.</div>',unsafe_allow_html=True)
        st.download_button("⬇️ Download scenario report (HTML)",report_html(d,ranked),"econano_scenario_report.html","text/html",use_container_width=True)

elif page=="What-if Simulator":
    st.title("⚙️ What-if Treatment Simulator")
    a,b,c=st.columns(3)
    material=a.selectbox("Nanomaterial",list(MATERIALS))
    pollutant=a.selectbox("Pollutant",POLLUTANTS)
    concentration=b.slider("Concentration (mg/L)",1,200,50)
    ph=b.slider("pH",2.0,12.0,7.0,0.1)
    minutes=c.slider("Contact time (min)",5,240,60,5)
    st.metric("Illustrative screening score",f"{score(material,pollutant,concentration,ph,minutes):.1f}%")
    ts=np.arange(5,241,5)
    fig=go.Figure(go.Scatter(x=ts,y=[score(material,pollutant,concentration,ph,t) for t in ts],mode="lines",line=dict(width=4)))
    fig.add_vline(x=minutes,line_dash="dash",annotation_text="Selected time")
    fig.update_layout(title="Illustrative score versus contact time",xaxis_title="Minutes",yaxis_title="Illustrative score (%)",yaxis_range=[0,100])
    st.plotly_chart(fig,use_container_width=True)
    ps=np.round(np.arange(2,12.1,.2),1)
    fig2=px.line(x=ps,y=[score(material,pollutant,concentration,p,minutes) for p in ps],labels={"x":"pH","y":"Illustrative score (%)"},title="Illustrative score versus pH")
    fig2.update_layout(yaxis_range=[0,100]); st.plotly_chart(fig2,use_container_width=True)
    st.caption("These curves are produced by a demonstration heuristic, not fitted adsorption or kinetic data.")

elif page=="Material Explorer":
    st.title("🔬 Nanomaterial Explorer")
    name=st.selectbox("Choose a material",list(MATERIALS))
    d=MATERIALS[name]
    st.markdown(f'<div class="dark-card"><h3>{name}</h3><p>Research fit: {", ".join(d["fit"])}</p></div>',unsafe_allow_html=True)
    st.subheader("Potential mechanism"); st.write(d["mechanism"])
    x,y,z=st.columns(3); x.metric("Indicative green profile",f"{d['green']}/5"); y.metric("Indicative reusability",f"{d['reuse']}/5"); z.metric("Relative cost score",f"{d['cost']}/5")
    st.warning(d["caution"])
    st.subheader("Material comparison")
    st.dataframe(pd.DataFrame([{"Material":n,"Potential fit":", ".join(v["fit"]),"Green profile":v["green"],"Reusability":v["reuse"],"Relative cost":v["cost"]} for n,v in MATERIALS.items()]),use_container_width=True,hide_index=True)

elif page=="AI Comparison":
    st.title("🤖 Material Recommendation & Comparison")
    st.write("This prototype uses a transparent rule-based heuristic, not a trained machine-learning model.")
    a,b,c=st.columns(3)
    pollutant=a.selectbox("Pollutant",POLLUTANTS)
    concentration=b.slider("Concentration (mg/L)",1,200,50)
    ph=c.slider("pH",2.0,12.0,7.0,.1)
    minutes=st.slider("Contact time (min)",5,240,60,5)
    ranked=compare(pollutant,concentration,ph,minutes); best=ranked.iloc[0]
    st.success(f"Top heuristic candidate for this scenario: {best['Material']}")
    st.dataframe(ranked,use_container_width=True,hide_index=True)
    st.write(MATERIALS[best["Material"]]["mechanism"])
    st.warning("Do not use this ranking to select a real treatment process without literature review, laboratory validation and safety assessment.")

elif page=="Sustainability":
    st.title("🌱 Sustainability Dashboard")
    st.write("Indicative discussion scores only; these are not life-cycle assessment results.")
    df=pd.DataFrame([{"Material":n,"Green profile":d["green"],"Reusability":d["reuse"],"Relative cost":d["cost"]} for n,d in MATERIALS.items()])
    fig=px.bar(df.melt(id_vars="Material",var_name="Dimension",value_name="Indicative score"),x="Material",y="Indicative score",color="Dimension",barmode="group",title="Indicative comparison (1–5)")
    fig.update_layout(yaxis_range=[0,5]); st.plotly_chart(fig,use_container_width=True)
    st.subheader("Questions for a real sustainability assessment")
    st.markdown("- Energy needed for synthesis and treatment\n- Hazard and scarcity of precursors\n- Recovery and reuse without performance loss\n- Nanoparticle leaching and ecotoxicity\n- Regeneration and disposal of spent material\n- Full life-cycle impacts")
    st.info("A material described as green is not automatically safe.")

elif page=="Research Library":
    st.title("📚 Research Library")
    topics={
      "Photocatalysis":"ZnO and TiO₂ are studied for light-assisted degradation of selected organic pollutants. Consider wavelength, intensity, catalyst loading, pH and water composition.",
      "Adsorption":"Biochar and functionalized magnetic materials are studied for uptake of contaminants. Surface area, pore structure, functional groups and competing ions matter.",
      "Magnetic separation":"Fe₃O₄ composites may offer magnetic recovery; recovery efficiency and nanoparticle leaching need testing.",
      "Green synthesis":"Biological routes are researched as alternatives for nanoparticle synthesis. Extract composition, reproducibility, purification and waste generation matter.",
      "Environmental safety":"Assess residual nanoparticles, transformation products, regeneration waste and ecotoxicity, not just pollutant removal."
    }
    for title,body in topics.items():
        with st.expander(title): st.write(body)
    st.warning("Add verified primary papers and DOI links before treating this as a formal bibliography. The app’s scores are not published experimental findings.")

else:
    st.title("ℹ️ About EcoNano AI")
    st.write("EcoNano AI is a computational educational prototype exploring nanomaterial-assisted water remediation.")
    st.subheader("Current capabilities")
    st.markdown("- Hypothetical pollutant and treatment-condition inputs\n- Illustrative candidate-material scoring\n- Parameter sensitivity visualizations\n- Material comparison and educational notes\n- Downloadable HTML scenario report")
    st.subheader("Limitations")
    st.markdown("- Does not analyze a real water sample\n- Does not contain a trained or validated ML model\n- Does not predict certified removal efficiency\n- Does not determine drinking-water safety\n- Does not replace laboratory testing or regulatory guidance")
    st.subheader("Scoring transparency")
    st.write("The heuristic combines a material-specific base value, pollutant-category compatibility, hypothetical pH response, contact-time response and concentration penalty. Coefficients are demonstration assumptions, not fitted experimental parameters.")
    st.error("Never use this prototype as the sole basis for real water-treatment decisions.")
