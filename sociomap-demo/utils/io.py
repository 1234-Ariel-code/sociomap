import os
import pandas as pd

def _read_csv(path: str):
    if not os.path.exists(path):
        return None
    return pd.read_csv(path)

def load_all(data_dir: str):
    return {
        "phenotype": _read_csv(os.path.join(data_dir, "phenotype.csv")),
        "chi2": _read_csv(os.path.join(data_dir, "chi2_results.csv")),
        "shap": _read_csv(os.path.join(data_dir, "shap_global.csv")),
        "umap": _read_csv(os.path.join(data_dir, "umap_clusters.csv")),
        "sim_metrics": _read_csv(os.path.join(data_dir, "simulation_metrics.csv")),
    }
