import streamlit as st
import pandas as pd

from utils.io import load_all
from utils.plots import (
    plot_prevalence_overall,
    plot_prevalence_by_group,
    plot_chi2_heatmap,
    plot_chi2_manhattan,
    plot_shap_bar,
    plot_umap_scatter,
    plot_simulation_boxplot
)

st.set_page_config(page_title="SOCIOMAP Demo", layout="wide")

st.title("SOCIOMAP Demo: Sociogenomic Inequities Explorer (Nigeria)")
st.caption(
    "Interactive companion tool for the SOCIOMAP manuscript. "
    "Explore stratified prevalence, χ² heterogeneity, SHAP explanations, and latent subgroups."
)

# -------------------
# Sidebar
# -------------------
st.sidebar.header("Data")
use_toy = st.sidebar.toggle("Use simulated toy data (public demo)", value=True)

if use_toy:
    N = st.sidebar.slider("Toy cohort size (N)", 2000, 20000, 8000, step=1000)
    seed = st.sidebar.number_input("Random seed", value=7, step=1)
    with st.spinner("Generating toy cohort + running pipeline..."):
        data = build_toy_outputs(N=N, seed=seed)
else:
    data_dir = st.sidebar.text_input("Data folder", value="data")
    from utils.io import load_all
    with st.spinner("Loading data..."):
        data = load_all(data_dir)

df_pheno = data.get("phenotype")
df_chi2  = data.get("chi2")
df_shap  = data.get("shap")
df_umap  = data.get("umap")
df_sim   = data.get("sim_metrics")
auc_df   = data.get("auc")

if df_pheno is None:
    st.error("Missing data/phenotype.csv. Please add it (see README).")
    st.stop()

# infer disease columns (binary flags)
non_disease_cols = set(["pid", "tribe", "religion", "income", "education", "region", "urban"])
disease_cols = [c for c in df_pheno.columns if c not in non_disease_cols and df_pheno[c].dropna().isin([0,1]).all()]
disease_cols = sorted(disease_cols)

st.sidebar.header("Filters")
selected_disease = st.sidebar.selectbox("Disease", options=disease_cols if disease_cols else df_pheno.columns, index=0)

group_var_options = [c for c in ["tribe", "religion", "income", "education", "region", "urban"] if c in df_pheno.columns]
selected_group_var = st.sidebar.selectbox("Group variable", options=group_var_options, index=0)

# -------------------
# Tabs
# -------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview",
    "Stratified prevalence",
    "χ² heterogeneity",
    "SHAP explanations",
    "Latent subgroups (UMAP)",
    "Simulation validation"
])

# ===================
# Tab 1: Overview
# ===================
with tab1:
    c1, c2, c3 = st.columns(3)
    c1.metric("Individuals (N)", f"{len(df_pheno):,}")
    c2.metric("Diseases (D)", f"{len(disease_cols):,}")
    miss_rate = float(df_pheno.isna().mean().mean())
    c3.metric("Overall missingness", f"{miss_rate:.2%}")

    st.subheader("Preview")
    st.dataframe(df_pheno.head(25), use_container_width=True)

    st.subheader("Overall prevalence")
    fig_prev = plot_prevalence_overall(df_pheno, disease_cols)
    st.plotly_chart(fig_prev, use_container_width=True)

# ===================
# Tab 2: Stratified prevalence
# ===================
with tab2:
    st.subheader(f"Prevalence of **{selected_disease}** by **{selected_group_var}**")
    fig = plot_prevalence_by_group(df_pheno, selected_disease, selected_group_var, top_k=25)
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Tip: For high-cardinality groups (e.g., tribe), this view shows the top groups by sample size "
        "to avoid small-cell instability. You can adjust top_k in the code if needed."
    )

# ===================
# Tab 3: Chi-square heterogeneity
# ===================
with tab3:
    st.subheader("χ² association testing (with BH-FDR correction)")
    if df_chi2 is None:
        st.warning("Missing data/chi2_results.csv — χ² plots will not display.")
    else:
        # Filters
        c1, c2, c3 = st.columns(3)
        gv = c1.selectbox("group_var", sorted(df_chi2["group_var"].unique()))
        dz = c2.selectbox("disease", sorted(df_chi2["disease"].unique()))
        only_valid = c3.checkbox("Only valid expected counts", value=True)

        dff = df_chi2[(df_chi2["group_var"] == gv) & (df_chi2["disease"] == dz)]
        if only_valid and "valid_expected_counts" in dff.columns:
            dff = dff[dff["valid_expected_counts"] == True]

        cA, cB = st.columns(2)
        cA.plotly_chart(plot_chi2_manhattan(dff, title=f"{dz} ~ {gv} (−log10 q)"), use_container_width=True)
        cB.plotly_chart(plot_chi2_heatmap(df_chi2, title="Significance map (−log10 q)"), use_container_width=True)

        st.caption("q = BH-FDR adjusted p-value. Smaller q indicates stronger evidence of group-wise heterogeneity.")
        st.dataframe(dff.sort_values("q").head(50), use_container_width=True)

# ===================
# Tab 4: SHAP explanations (global)
# ===================
with tab4:
    st.subheader("Model explanations (global SHAP summaries)")
    if df_shap is None:
        st.warning("Missing data/shap_global.csv — SHAP plots will not display.")
    else:
        diseases_in_shap = sorted(df_shap["disease"].unique())
        disease_for_shap = st.selectbox("Disease (SHAP)", diseases_in_shap, index=0)
        topk = st.slider("Top-K features", min_value=5, max_value=50, value=15, step=1)
        fig = plot_shap_bar(df_shap, disease_for_shap, top_k=topk)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Mean(|SHAP|) indicates average absolute contribution of each feature to the model output.")

# ===================
# Tab 5: UMAP + clustering
# ===================
with tab5:
    st.subheader("Latent population structure (UMAP + clustering)")
    if df_umap is None:
        st.warning("Missing data/umap_clusters.csv — UMAP view will not display.")
    else:
        color_by = st.selectbox(
            "Color by",
            options=[c for c in ["cluster", "tribe", "religion", "income", "education"] if c in df_umap.columns],
            index=0
        )
        fig = plot_umap_scatter(df_umap, color_by=color_by)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("UMAP embedding computed from encoded features; clusters from KMeans in the embedded space.")

# ===================
# Tab 6: Simulation validation
# ===================
with tab6:
    st.subheader("Simulation validation")
    if df_sim is None:
        st.warning("Missing data/simulation_metrics.csv — simulation plots will not display.")
    else:
        metric = st.selectbox(
            "Simulation metric",
            options=[c for c in df_sim.columns if c not in ["scenario", "rep", "split"]],
            index=0
        )
        fig = plot_simulation_boxplot(df_sim, metric=metric)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Boxplots summarize metric variability across simulation replicates per scenario.")
