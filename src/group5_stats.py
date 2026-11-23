"""Statistics helpers used in notebooks/analysis/05_eda_lab_effect_EV.ipynb.

Plain-language explanations of each method are in docs/statistics-explained.md.
"""
import numpy as np
import pandas as pd
from scipy.stats import kruskal, spearmanr

LASER = ["power_W", "speed_mm_s", "layer_um", "hatch_um"]


def epsilon_squared(values, groups):
    """Kruskal-Wallis effect size: share of the spread (in ranks) explained by the grouping.

    eps2 = (H - k + 1) / (n - k); about 0 = no effect, 1 = the grouping explains everything.
    Returns (eps2, p_value, k_groups, n).
    """
    df = pd.DataFrame({"y": np.asarray(values), "g": np.asarray(groups)}).dropna()
    gs = [x.y.values for _, x in df.groupby("g")]
    k, n = len(gs), len(df)
    H, p = kruskal(*gs)
    return round(float((H - k + 1) / (n - k)), 2), float(p), k, n


def shuffle_threshold(values, groups, reps=500, q=0.95, seed=0):
    """eps2 that random (shuffled) group labels reach in q of cases: the 'chance' level."""
    rng = np.random.default_rng(seed)
    values, groups = np.asarray(values), np.asarray(groups)
    return float(np.quantile([epsilon_squared(values, rng.permutation(groups))[0] for _ in range(reps)], q))


def within_treatment(df, col="YS_MPa", min_papers=3):
    """Subtract each named treatment's median, keeping treatments used by >= min_papers papers.

    Lets you compare spread *within* a recipe (e.g. lab vs printer) without
    the big differences *between* recipes getting in the way.
    """
    ht = df[df.condition.isin(["Heat treated", "HIP"]) & df[col].notna()]
    n_pap = ht.groupby("ht_route").paper.nunique()
    keep = [r for r in n_pap[n_pap >= min_papers].index if r not in ("HT, temps not given", "Unknown")]
    h = ht[ht.ht_route.isin(keep)].copy()
    h["residual"] = h[col] - h.groupby("ht_route")[col].transform("median")
    return h


def spearman_per_setting(df, col="YS_MPa", settings=("power_W", "speed_mm_s", "layer_um", "hatch_um", "VED_calc")):
    """Spearman rho of each laser setting vs a property, one point per paper x setting
    (so a paper with many rows doesn't get many votes)."""
    m = (df.dropna(subset=[col]).groupby(["paper"] + LASER, dropna=False)
         .agg(y=(col, "median"), VED_calc=("VED_calc", "median")).reset_index())
    out = {}
    for c in settings:
        mm = m.dropna(subset=[c, "y"])
        rho, p = spearmanr(mm[c], mm.y)
        out[c] = {"rho": round(float(rho), 2), "p": round(float(p), 3), "n": len(mm)}
    return pd.DataFrame(out).T


def cross_validate(df, model_factory, split="papers", reps=20, target="YS_MPa", group_col="ht_group"):
    """Mean R2 and mean absolute error over repeated 5-fold cross-validation.

    split="random": rows shuffled into folds (the usual way; rows from a paper can be
    in both training and testing). split="papers": whole papers held out (GroupKFold),
    i.e. the model predicts labs it has never seen.
    model_factory=None gives the baseline: median per named heat treatment.
    """
    from sklearn.metrics import mean_absolute_error, r2_score
    from sklearn.model_selection import GroupKFold, KFold
    d = df.reset_index(drop=True)
    X = pd.concat([d[LASER], pd.get_dummies(d[group_col]).astype(int)], axis=1).values.astype(float)
    y, g = d[target].values, d.paper.values
    r2s, maes = [], []
    for rep in range(reps):
        pred = np.zeros(len(y))
        if split == "papers":
            ug = np.unique(g)
            perm = dict(zip(ug, np.random.default_rng(rep).permutation(len(ug))))
            folds = GroupKFold(5).split(X, y, [perm[v] for v in g])
        else:
            folds = KFold(5, shuffle=True, random_state=rep).split(X)
        for tr, te in folds:
            if model_factory is None:
                med = d.iloc[tr].groupby(group_col)[target].median()
                pred[te] = [med.get(k, np.median(y[tr])) for k in d.iloc[te][group_col]]
            else:
                m = model_factory()
                m.fit(X[tr], y[tr])
                pred[te] = m.predict(X[te])
        r2s.append(r2_score(y, pred))
        maes.append(mean_absolute_error(y, pred))
    return round(float(np.mean(r2s)), 2), round(float(np.mean(maes)))
