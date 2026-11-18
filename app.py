import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

st.set_page_config(page_title="EcoNano AI", page_icon="🌱", layout="wide")

st.title("🌱 EcoNano AI")
st.subheader("Decision support for nanomaterial-assisted water remediation")
st.warning(
    "Research prototype: the built-in model uses simulated demonstration data, not "
    "laboratory measurements. Its outputs are illustrative and must not be used to "
    "select a real water-treatment process or claim environmental safety."
)

@st.cache_data
def make_demo_data(n=1200, seed=17):
    """Create explicitly synthetic data for testing the app workflow."""
    rng = np.random.default_rng(seed)
    materials = np.array(["ZnO", "TiO2", "Fe3O4", "Biochar-composite"])
    material = rng.choice(materials, n)
    concentration = rng.uniform(0.1, 2.0, n)       # g/L
    pH = rng.uniform(4.0, 10.0, n)
    time = rng.uniform(15, 180, n)                  # minutes
    pollutant = rng.choice(["Dye", "Pharmaceutical", "Metal ion"], n)
    base = pd.Series(material).map({
        "ZnO": 68, "TiO2": 73, "Fe3O4": 55, "Biochar-composite": 62
    }).to_numpy()
    pollutant_adj = pd.Series(pollutant).map({
        "Dye": 8, "Pharmaceutical": -5, "Metal ion": -12
    }).to_numpy()
    pH_penalty = np.abs(pH - 7.0) * 2.0
    conc_effect = 13 * (1 - np.exp(-concentration))
    time_effect = 12 * (1 - np.exp(-time / 65))
    noise = rng.normal(0, 5, n)
    removal = np.clip(base + pollutant_adj + conc_effect + time_effect - pH_penalty + noise, 3, 98)
    return pd.DataFrame({
        "material": material, "concentration_g_L": concentration, "pH": pH,
        "contact_time_min": time, "pollutant_group": pollutant,
        "removal_efficiency_pct": removal
    })

df = make_demo_data()
features = ["material", "concentration_g_L", "pH", "contact_time_min", "pollutant_group"]
X = pd.get_dummies(df[features], columns=["material", "pollutant_group"])
y = df["removal_efficiency_pct"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=180, min_samples_leaf=2, random_state=42)
model.fit(X_train, y_train)
pred_test = model.predict(X_test)
mae = mean_absolute_error(y_test, pred_test)
r2 = r2_score(y_test, pred_test)

with st.sidebar:
    st.header("Scenario inputs")
    material = st.selectbox("Candidate material", ["ZnO", "TiO2", "Fe3O4", "Biochar-composite"])
    pollutant = st.selectbox("Pollutant group", ["Dye", "Pharmaceutical", "Metal ion"])
    concentration = st.slider("Material concentration (g/L)", 0.1, 2.0, 0.8, 0.1)
    pH = st.slider("Water pH", 4.0, 10.0, 7.0, 0.1)
    contact_time = st.slider("Contact time (minutes)", 15, 180, 90, 5)

scenario = pd.DataFrame([{
    "material": material, "concentration_g_L": concentration, "pH": pH,
    "contact_time_min": contact_time, "pollutant_group": pollutant
}])
scenario_enc = pd.get_dummies(scenario, columns=["material", "pollutant_group"]).reindex(columns=X.columns, fill_value=0)
pred = float(model.predict(scenario_enc)[0])

c1, c2, c3 = st.columns(3)
c1.metric("Illustrative predicted removal", f"{pred:.1f}%")
c2.metric("Demo-model MAE", f"{mae:.1f} percentage points")
c3.metric("Demo-model R²", f"{r2:.2f}")

st.caption("Metrics are calculated against held-out rows from the same synthetic dataset. They do not measure real-world predictive validity.")

st.markdown("### Scenario interpretation")
st.write(
    f"For the selected **{material}** / **{pollutant.lower()}** scenario, the demonstration model "
    f"estimates **{pred:.1f}%** removal under the entered conditions. This is a software-workflow "
    "demonstration only, not an experimentally supported estimate."
)

st.markdown("### Compare candidate materials")
compare_rows = []
for m in ["ZnO", "TiO2", "Fe3O4", "Biochar-composite"]:
    row = pd.DataFrame([{
        "material": m, "concentration_g_L": concentration, "pH": pH,
        "contact_time_min": contact_time, "pollutant_group": pollutant
    }])
    row = pd.get_dummies(row, columns=["material", "pollutant_group"]).reindex(columns=X.columns, fill_value=0)
    compare_rows.append({"Material": m, "Illustrative removal (%)": float(model.predict(row)[0])})
comparison = pd.DataFrame(compare_rows).sort_values("Illustrative removal (%)", ascending=False)
fig = px.bar(comparison, x="Material", y="Illustrative removal (%)", range_y=[0, 100],
             title="Synthetic demonstration scenario — not measured performance")
st.plotly_chart(fig, use_container_width=True)

st.markdown("### What the model learned in this demo")
importance = pd.DataFrame({"Feature": X.columns, "Importance": model.feature_importances_})
importance = importance.sort_values("Importance", ascending=False).head(10)
fig2 = px.bar(importance.sort_values("Importance"), x="Importance", y="Feature", orientation="h",
              title="Random Forest feature importance (synthetic data)")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("### Environmental safeguards checklist")
st.write("A high predicted removal percentage is not enough to recommend a material. Before any real deployment, assess:")
st.markdown("""
- Nanoparticle release and persistence after treatment.
- Aquatic ecotoxicity and effects on beneficial microorganisms.
- Recovery, regeneration and safe disposal of spent material.
- Energy, chemical and water demand across the treatment lifecycle.
- Performance using replicated experiments and independent validation data.
""")

st.markdown("### Download the demo dataset")
st.download_button("Download synthetic demo data (CSV)", df.to_csv(index=False).encode("utf-8"),
                   file_name="econano_synthetic_demo_data.csv", mime="text/csv")

with st.expander("Methodology and limitations"):
    st.markdown("""
    **Model:** Random Forest regression trained on generated demonstration records.

    **Purpose:** Demonstrate an end-to-end interactive workflow, feature encoding,
    model evaluation, scenario prediction and visual comparison.

    **Not established:** Real pollutant-removal performance, material safety,
    generalization to real water matrices, or suitability for treatment design.

    **Next research step:** Replace the synthetic dataset with a traceable,
    publication-derived dataset. Record DOI/source, experimental conditions,
    units, replicates and uncertainty. Evaluate generalization by holding out
    entire source studies rather than randomly splitting individual rows.
    """)
