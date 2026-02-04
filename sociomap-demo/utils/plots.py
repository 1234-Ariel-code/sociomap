import numpy as np
import pandas as pd
import plotly.express as px

def plot_prevalence_overall(df: pd.DataFrame, disease_cols: list[str]):
    prev = []
    for d in disease_cols:
        x = df[d].dropna()
        if len(x) == 0:
            continue
        prev.append({"disease": d, "prevalence": float(x.mean())})
    prev = pd.DataFrame(prev).sort_values("prevalence", ascending=False)
    fig = px.bar(prev, x="disease", y="prevalence", title="Overall disease prevalence")
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_prevalence_by_group(df: pd.DataFrame, disease: str, group_var: str, top_k: int = 25):
    dff = df[[group_var, disease]].dropna()
    # top-k groups by size
    sizes = dff[group_var].value_counts()
    keep = sizes.head(top_k).index
    dff = dff[dff[group_var].isin(keep)]
    out = dff.groupby(group_var)[disease].agg(["mean", "count"]).reset_index()
    out = out.rename(columns={"mean": "prevalence", "count": "n"}).sort_values("prevalence", ascending=False)
    fig = px.bar(out, x=group_var, y="prevalence", hover_data=["n"], title=f"{disease} prevalence by {group_var}")
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_chi2_manhattan(dff: pd.DataFrame, title: str = ""):
    if len(dff) == 0:
        return px.scatter(title="No χ² results after filtering.")
    q = dff["q"].replace(0, np.nan)
    dff = dff.assign(neglog10q=-np.log10(q))
    dff = dff.sort_values("neglog10q", ascending=False)
    fig = px.bar(dff, x="group", y="neglog10q", hover_data=["p", "q", "n_group"], title=title)
    fig.update_layout(xaxis_tickangle=-45, yaxis_title="−log10(q)")
    return fig

def plot_chi2_heatmap(df_chi2: pd.DataFrame, title: str = ""):
    # pivot: disease x group_var using mean -log10(q)
    tmp = df_chi2.copy()
    tmp["q2"] = tmp["q"].replace(0, np.nan)
    tmp["score"] = -np.log10(tmp["q2"])
    piv = tmp.groupby(["disease", "group_var"])["score"].mean().reset_index()
    mat = piv.pivot(index="disease", columns="group_var", values="score").fillna(0.0)
    fig = px.imshow(mat, aspect="auto", title=title, labels=dict(color="mean −log10(q)"))
    return fig

def plot_shap_bar(df_shap: pd.DataFrame, disease: str, top_k: int = 15):
    dff = df_shap[df_shap["disease"] == disease].copy()
    dff = dff.sort_values("mean_abs_shap", ascending=False).head(top_k)
    fig = px.bar(dff, x="feature", y="mean_abs_shap", title=f"Top {top_k} SHAP features: {disease}")
    fig.update_layout(xaxis_tickangle=-45, yaxis_title="Mean(|SHAP|)")
    return fig

def plot_umap_scatter(df_umap: pd.DataFrame, color_by: str = "cluster"):
    fig = px.scatter(
        df_umap, x="umap1", y="umap2",
        color=color_by,
        hover_data=[c for c in ["pid", "tribe", "religion", "income", "education", "cluster"] if c in df_umap.columns],
        title=f"UMAP embedding colored by {color_by}"
    )
    fig.update_traces(marker=dict(size=5, opacity=0.7))
    return fig

def plot_simulation_boxplot(df_sim: pd.DataFrame, metric: str):
    dff = df_sim[["scenario", metric]].dropna()
    fig = px.box(dff, x="scenario", y=metric, title=f"Simulation boxplot: {metric}")
    fig.update_layout(xaxis_tickangle=-45)
    return fig
