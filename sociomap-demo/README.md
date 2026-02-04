# SOCIOMAP Demo (Public, Interactive Companion App)

This repository contains the **public interactive demo** for the paper:

**SOCIOMAP: Mapping sociogenomic inequities in chronic disease risk in Nigeria**

The demo is designed to be **safe to share publicly**: by default it runs on a **simulated (“toy”) Nigerian-like cohort** that reproduces key real-world challenges (high-cardinality groups, underdiagnosis/access bias, ICD noise, missingness, multimorbidity, and interaction-driven risk), **without releasing any participant-level data**.


---

## What the demo lets you explore

The app provides an end-to-end interactive exploration of SOCIOMAP outputs:

- **Overview**
  - cohort size, disease count, missingness rate
  - overall disease prevalence (bar chart)
  - data preview table

- **Stratified prevalence**
  - disease prevalence by **tribe / religion / income / education / region / urban**
  - top-k filtering for high-cardinality groups (e.g., tribes)

- **χ² heterogeneity**
  - chi-square association testing by group variable
  - BH-FDR adjusted q-values
  - Manhattan-style bar plot (−log10 q)
  - global significance heatmap

- **Model explanations**
  - global feature importance summaries (proxy SHAP for public demo)
  - top-k features per disease with interpretability-focused labels

- **Latent subgroups**
  - UMAP embedding of tabular features
  - KMeans clusters overlay
  - coloring by cluster or sociodemographic variables

- **Simulation validation (optional tab)**
  - loads a toy `simulation_metrics.csv` in toy mode
  - boxplots per scenario and metric (ARI, NMI, AUC, co-occurrence correlation, etc.)

---

## Privacy & data-sharing note (important)

**Default mode: simulated data only**

- The demo runs entirely on a **generated synthetic cohort**.
- No real participant-level Nigerian cohort data is included in this repository.
- This makes the demo safe for public sharing and journal reviewers.

**Optional mode: plug in your own exports**

If you want to run the same interface on your own internal data, you can provide CSV exports in `data/`.
Do **NOT** commit sensitive files to a public repo.

---

## Repository structure

```
sociomap-demo/
├── app.py
├── requirements.txt
├── README.md
├── utils/
│   ├── io.py
│   ├── plots.py
│   └── toy_data.py
└── data/                      # optional (for private/internal use)
    ├── phenotype.csv
    ├── chi2_results.csv
    ├── shap_global.csv
    ├── umap_clusters.csv
    └── simulation_metrics.csv
```

---

## Quickstart (run locally)

### 1) Create and activate a Python environment

```bash
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows (PowerShell)
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the app

```bash
streamlit run app.py
```

Open the displayed local URL in your browser (typically http://localhost:8501).

---

## Using the simulated toy demo (recommended for public)

In the app sidebar:

- **Use simulated toy data (public demo)** = ON
- Choose:
  - **Toy cohort size (N)** (e.g., 8,000–20,000)
  - **Random seed** (for reproducibility)

The app will generate the cohort and compute all outputs automatically.

---

## What the toy simulation mimics

The toy generator approximates properties found in real-world Nigerian-scale analyses:

- High-cardinality social structure (many tribes with imbalance)
- Correlated sociodemographics via a latent SES factor
- Behavioral/lifestyle gradients (diet, BMI, smoking, urbanicity)
- Multimorbidity structure via a shared latent health factor
- Interaction-driven risk (e.g., salt × low-income × north increases hypertension risk)
- Diagnosis/access bias causing underdiagnosis in lower-access groups
- ICD noise (sensitivity/specificity)
- Structured missingness (non-random)

---

## Running the app on your own exported outputs (private/internal)

If you want to run SOCIOMAP Demo on your own data:

1. Turn **OFF** the sidebar toggle:
   - **Use simulated toy data (public demo)** = OFF

2. Add CSV files in `data/` (or another directory and point the sidebar path to it).

---

## Expected file formats

### `data/phenotype.csv`

Individual-level table.

**Required columns (recommended):**
- `pid`
- `tribe`
- `religion`
- `income`
- `education`
- `region`
- `urban`

**Optional numeric / lifestyle columns:**
- `bmi`
- `fruitveg`
- `phys_act`
- `smoke`
- `alcohol`
- `palm_oil`
- …

**Disease flags (binary):**
- One column per disease (0/1), e.g.:
  - `Hypertension`
  - `Type2Diabetes`
  - …

---

### `data/chi2_results.csv`

One row per *(group_var, group, disease)*.

**Columns:**
- `group_var`
- `group`
- `disease`
- `n_group`
- `p`
- `q`
- `rej_fdr`
- `valid_expected_counts`

---

### `data/shap_global.csv`

One row per *(disease, feature)*.

**Columns:**
- `disease`
- `feature`
- `mean_abs_shap`

---

### `data/umap_clusters.csv`

One row per individual.

**Columns:**
- `pid`
- `umap1`
- `umap2`
- `cluster`

**Optional overlays:**
- `tribe`
- `religion`
- `income`
- `education`
- `region`
- `urban`

---

### `data/simulation_metrics.csv` (optional)

**Columns:**
- `scenario`
- `rep`
- *(optional)* `split`
- Metrics (e.g., `ARI`, `NMI`, `Hypertension__roc_auc`, `cooc_corr`, `prev_mae`, …)

---

## Reproducibility

- The simulated demo is fully seeded.
- Using the same `(N, seed)` reproduces identical toy cohorts and figures.

---

## Notes on SHAP in the public demo

For public safety and speed, the demo currently uses a **proxy global importance**
(e.g., logistic coefficient magnitudes on one-hot encoded features), which behaves similarly to global SHAP summaries.

If you want:
- true SHAP computation,
- per-person explanation panels,
- subgroup SHAP aggregation,

an optional **“SHAP mode”** can be enabled when `shap` is installed and data size is manageable.

---

## Contact & project links

- **Main project repository:** https://github.com/1234-Ariel-code/sociomap/
- **Demo repository:** https://github.com/1234-Ariel-code/sociomap-demo

For questions or collaboration, please contact the authors via the SOCIOMAP repository.
