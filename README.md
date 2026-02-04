# SOCIOMAP

![canvas-image-1-1769551027544](https://github.com/user-attachments/assets/9a51b574-e401-4cba-a178-ff94cef7874a)

**SOCIOMAP** is an interpretable, equity-centered machine learning framework for mapping sociodemographic and lifestyle structuring of chronic disease risk in Nigeria (and behond) using a nationally representative cohort (~45,000 individuals). The project integrates ICD-10 phenotyping, stratified epidemiology, statistical association testing, supervised risk modeling (XGBoost), explainability (SHAP), unsupervised subgroup discovery (UMAP + KMeans), and interactive dashboards (Dash/Streamlit).

## Repository layout
- `code/` — analysis code (currently a single notebook)
- `manuscript/` — manuscript draft and figures

## Quick start
1. Open the main notebook: `code/sociomap.ipynb`
2. Run cells in order to reproduce preprocessing, analyses, and figures.

## Interactive demo (public)

A **public, privacy-safe interactive demo** based on a fully simulated Nigerian-like cohort is available here:
**https://sociomap-owjbfnfa3cmr7zuvzs2euq.streamlit.app/**
The demo allows users to explore stratified prevalence, χ² heterogeneity, interpretable risk models, and latent population subgroups **without exposing any real participant-level data**.

## Citation
If you use this repository, please cite the SOCIOMAP manuscript (preprint link to be added).
