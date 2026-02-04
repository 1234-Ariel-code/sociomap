# utils/toy_data.py
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

import umap

# Optional: SHAP can be heavy; for demo we produce a proxy "importance"
# using absolute correlation with model logit or feature gain-like score.
# If you want true SHAP later, we can swap this in.

def simulate_toy_cohort(N=8000, seed=7):
    rng = np.random.default_rng(seed)

    # High-cardinality tribes + imbalance
    tribes = [f"T{i:02d}" for i in range(1, 41)]  # 40 tribes
    probs = np.linspace(1.0, 0.1, len(tribes))
    probs = probs / probs.sum()
    tribe = rng.choice(tribes, size=N, p=probs)

    religions = ["Christian", "Muslim", "Other"]
    religion = rng.choice(religions, size=N, p=[0.55, 0.40, 0.05])

    income = rng.choice(["Low", "Mid", "High"], size=N, p=[0.45, 0.40, 0.15])
    education = rng.choice(["Primary", "Secondary", "University"], size=N, p=[0.35, 0.45, 0.20])
    region = rng.choice(["North", "South", "West"], size=N, p=[0.40, 0.35, 0.25])
    urban = rng.binomial(1, p=np.where(income == "High", 0.75, np.where(income == "Mid", 0.55, 0.35)))

    # latent SES driver induces correlation among social determinants
    tribe_shift = {t: rng.normal(0, 0.4) for t in tribes}
    religion_shift = {"Christian": 0.1, "Muslim": -0.05, "Other": 0.0}
    region_shift = {"North": -0.15, "South": 0.10, "West": 0.05}

    S = (
        np.array([tribe_shift[t] for t in tribe])
        + np.array([religion_shift[r] for r in religion])
        + np.array([region_shift[g] for g in region])
        + rng.normal(0, 1.0, size=N)
    )

    # Lifestyle/anthro
    pa = np.clip(rng.normal(0.0, 1.0, size=N) + 0.2*(urban==1) - 0.2*(income=="Low"), -3, 3)
    smoking = rng.binomial(1, p=np.clip(0.12 + 0.05*(urban==1) - 0.05*(education=="University"), 0.02, 0.35))

    bmi = (
        22
        + 1.2*(urban==1)
        + 1.0*(income=="High")
        + 0.4*(income=="Mid")
        - 0.8*pa
        + rng.normal(0, 2.0, size=N)
    )
    bmi = np.clip(bmi, 16, 45)

    oil = rng.choice(["Palm", "Vegetable", "Groundnut", "Other"], size=N,
                     p=[0.45, 0.35, 0.15, 0.05])
    fruitveg = np.clip(rng.normal(2.0, 1.0, size=N) + 0.5*(income=="High") - 0.3*(region=="North"), 0, 7)
    salt = np.clip(rng.normal(1.5, 0.6, size=N) + 0.3*(region=="North") + 0.2*(income=="Low"), 0, 4)

    # Shared multimorbidity driver
    H = 0.6*(bmi-22)/5 + 0.4*(income=="Low") - 0.3*pa + 0.2*smoking + 0.2*S + rng.normal(0, 0.5, size=N)

    # Diseases (toy): hypertension, t2d, hepatitis, epilepsy
    def sigmoid(x): return 1/(1+np.exp(-x))

    # interaction-driven risk: salt effect amplified in Low income & North
    int_hyp = 0.6*(salt-1.5)*(income=="Low")*(region=="North")

    p_hyp = sigmoid(-1.7 + 1.0*H + 0.5*(bmi>30) + int_hyp)
    p_t2d = sigmoid(-2.2 + 0.9*H + 0.6*(bmi-25)/5 + 0.2*(income=="High"))
    p_hep = sigmoid(-2.0 + 0.3*(region=="South") + 0.25*(oil=="Palm") + 0.2*(income=="Low") + rng.normal(0,0.15,N))
    p_epi = sigmoid(-2.4 + 0.35*(income=="Low") + 0.15*(region=="West") + rng.normal(0,0.2,N))

    y_hyp_true = rng.binomial(1, p_hyp)
    y_t2d_true = rng.binomial(1, p_t2d)
    y_hep_true = rng.binomial(1, p_hep)
    y_epi_true = rng.binomial(1, p_epi)

    # Access / underdiagnosis (creates realistic bias)
    p_access = sigmoid(-0.3 + 0.8*(income=="High") + 0.4*(education=="University") + 0.35*urban + 0.2*(region=="South"))
    access = rng.binomial(1, p_access)

    # ICD noise: sensitivity/specificity
    def observe(y_true, sens=0.85, spec=0.98):
        y_obs = y_true.copy()
        # false negatives when access=1
        fn = (access==1) & (y_true==1) & (rng.random(N) > sens)
        y_obs[fn] = 0
        # false positives when access=1
        fp = (access==1) & (y_true==0) & (rng.random(N) > spec)
        y_obs[fp] = 1
        # underdiagnosis: if access==0, mostly zeroed out
        y_obs[access==0] = 0
        return y_obs

    hypertension = observe(y_hyp_true, sens=0.86, spec=0.985)
    t2d = observe(y_t2d_true, sens=0.83, spec=0.99)
    hepatitis = observe(y_hep_true, sens=0.80, spec=0.98)
    epilepsy = observe(y_epi_true, sens=0.75, spec=0.99)

    df = pd.DataFrame({
        "pid": np.arange(N),
        "tribe": tribe,
        "religion": religion,
        "income": income,
        "education": education,
        "region": region,
        "urban": urban,
        "bmi": bmi,
        "physical_activity": pa,
        "smoking": smoking,
        "oil_type": oil,
        "fruitveg": fruitveg,
        "salt": salt,
        "hypertension": hypertension,
        "t2d": t2d,
        "hepatitis": hepatitis,
        "epilepsy": epilepsy,
    })

    # Some structured missingness
    miss_bmi = (income=="Low") & (rng.random(N) < 0.10)
    df.loc[miss_bmi, "bmi"] = np.nan

    miss_oil = (region=="North") & (rng.random(N) < 0.08)
    df.loc[miss_oil, "oil_type"] = np.nan

    return df


def chi2_group_tests(df, group_var, disease_cols, alpha=0.05):
    """
    Minimal χ² test per (group_var, disease), with BH-FDR across diseases for each group_var.
    For demo we implement a simple p-value computation using scipy if available; otherwise fallback.
    """
    try:
        from scipy.stats import chi2_contingency
    except Exception:
        chi2_contingency = None

    out = []
    for d in disease_cols:
        tmp = df[[group_var, d]].dropna()
        if tmp.empty:
            continue
        tab = pd.crosstab(tmp[group_var], tmp[d])
        if tab.shape[1] < 2:
            continue
        if chi2_contingency is None:
            # fallback: no p-value, skip
            continue
        chi2, p, dof, exp = chi2_contingency(tab.values)
        valid_expected = (exp >= 5).all()
        # store per-group info too (for manhattan-like bar chart)
        for g in tab.index:
            n_group = int(tab.loc[g].sum())
            out.append({
                "group_var": group_var,
                "group": str(g),
                "disease": d,
                "n_group": n_group,
                "p": float(p),
                "valid_expected_counts": bool(valid_expected),
            })

    res = pd.DataFrame(out)
    if res.empty:
        return res

    # BH-FDR within each (group_var, disease) set (here p same across groups; still ok for demo)
    res["q"] = bh_fdr(res["p"].values)
    res["rej_fdr"] = res["q"] < alpha
    return res


def bh_fdr(pvals):
    pvals = np.asarray(pvals, dtype=float)
    n = len(pvals)
    order = np.argsort(pvals)
    ranked = pvals[order]
    q = ranked * n / (np.arange(1, n+1))
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty_like(q)
    out[order] = np.clip(q, 0, 1)
    return out


def fit_simple_models_and_importance(df, disease_cols):
    """
    Train a simple logistic model (sklearn) for each disease and compute:
    - roc_auc
    - proxy importance: abs(coef) aggregated back to original features
    """
    from sklearn.linear_model import LogisticRegression

    feature_cols = ["tribe","religion","income","education","region","urban","bmi","physical_activity","smoking","oil_type","fruitveg","salt"]
    X = df[feature_cols].copy()
    # fill numeric missing
    for c in ["bmi","physical_activity","fruitveg","salt"]:
        X[c] = X[c].fillna(X[c].median())
    # fill categorical missing
    for c in ["tribe","religion","income","education","region","oil_type"]:
        X[c] = X[c].fillna("Missing")

    cat = ["tribe","religion","income","education","region","oil_type"]
    num = ["urban","bmi","physical_activity","smoking","fruitveg","salt"]

    pre = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat),
            ("num", "passthrough", num),
        ]
    )

    out_auc = []
    out_imp = []

    for d in disease_cols:
        y = df[d].astype(int).values
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=7, stratify=y)

        clf = LogisticRegression(max_iter=200, n_jobs=1)
        pipe = Pipeline([("pre", pre), ("clf", clf)])
        pipe.fit(Xtr, ytr)

        prob = pipe.predict_proba(Xte)[:,1]
        auc = roc_auc_score(yte, prob)
        out_auc.append({"disease": d, "roc_auc": float(auc)})

        # proxy "global shap": abs(coef)
        ohe = pipe.named_steps["pre"].named_transformers_["cat"]
        cat_names = list(ohe.get_feature_names_out(cat))
        feature_names = cat_names + num

        coef = pipe.named_steps["clf"].coef_.ravel()
        imp = np.abs(coef)

        # take top 30
        top_idx = np.argsort(imp)[::-1][:30]
        for idx in top_idx:
            out_imp.append({
                "disease": d,
                "feature": feature_names[idx],
                "mean_abs_shap": float(imp[idx]),
            })

    return pd.DataFrame(out_auc), pd.DataFrame(out_imp)


def make_umap_and_clusters(df):
    feature_cols = ["tribe","religion","income","education","region","urban","bmi","physical_activity","smoking","oil_type","fruitveg","salt"]
    X = df[feature_cols].copy()
    for c in ["bmi","physical_activity","fruitveg","salt"]:
        X[c] = X[c].fillna(X[c].median())
    for c in ["tribe","religion","income","education","region","oil_type"]:
        X[c] = X[c].fillna("Missing")

    cat = ["tribe","religion","income","education","region","oil_type"]
    num = ["urban","bmi","physical_activity","smoking","fruitveg","salt"]

    enc = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat),
            ("num", "passthrough", num),
        ]
    )
    X_enc = enc.fit_transform(X)

    reducer = umap.UMAP(n_neighbors=25, min_dist=0.15, random_state=7)
    Z = reducer.fit_transform(X_enc)

    km = KMeans(n_clusters=5, random_state=7, n_init="auto")
    labels = km.fit_predict(Z)

    out = pd.DataFrame({
        "pid": df["pid"].values,
        "umap1": Z[:,0],
        "umap2": Z[:,1],
        "cluster": labels,
    })
    for c in ["tribe","religion","income","education","region","urban"]:
        out[c] = df[c].values
    return out


def make_simulation_metrics_toy():
    """
    Minimal toy simulation_metrics.csv so the Simulation tab works.
    """
    scenarios = ["S1_null","S2_main_effects","S3_interactions","S4_access_bias","S5_many_small_tribes","S6_rare_disease","S7_multimorbidity_strong","S8_distribution_shift"]
    rng = np.random.default_rng(7)
    rows = []
    for sc in scenarios:
        for rep in range(10):
            if sc == "S1_null":
                ari = rng.normal(0.00, 0.01)
                nmi = rng.normal(0.00, 0.01)
                auc = rng.normal(0.58, 0.01)
                cooc = rng.normal(0.998, 0.0006)
                prev_mae = rng.normal(0.005, 0.0005)
            elif sc == "S3_interactions":
                ari = rng.normal(0.04, 0.01)
                nmi = rng.normal(0.075, 0.01)
                auc = rng.normal(0.61, 0.01)
                cooc = rng.normal(0.9992, 0.0003)
                prev_mae = rng.normal(0.008, 0.001)
            else:
                ari = rng.normal(0.035, 0.015)
                nmi = rng.normal(0.075, 0.012)
                auc = rng.normal(0.61, 0.015)
                cooc = rng.normal(0.9990, 0.0004)
                prev_mae = rng.normal(0.02, 0.004)
            rows.append({
                "scenario": sc,
                "rep": rep,
                "ARI": float(max(0, ari)),
                "NMI": float(max(0, nmi)),
                "Hypertension__roc_auc": float(auc),
                "cooc_corr": float(cooc),
                "prev_mae": float(max(0, prev_mae)),
            })
    return pd.DataFrame(rows)


def build_toy_outputs(N=8000, seed=7):
    df = simulate_toy_cohort(N=N, seed=seed)

    disease_cols = ["hypertension","t2d","hepatitis","epilepsy"]

    # χ² results for a few key group vars
    chi2_parts = []
    for gv in ["tribe","religion","income","education","region","urban"]:
        if gv in df.columns:
            chi2_parts.append(chi2_group_tests(df, gv, disease_cols))
    chi2_df = pd.concat(chi2_parts, ignore_index=True) if chi2_parts else None

    auc_df, shap_df = fit_simple_models_and_importance(df, disease_cols)
    umap_df = make_umap_and_clusters(df)
    sim_df = make_simulation_metrics_toy()

    return {
        "phenotype": df,
        "chi2": chi2_df,
        "shap": shap_df,
        "umap": umap_df,
        "sim_metrics": sim_df,
        "auc": auc_df,  # optional
    }
