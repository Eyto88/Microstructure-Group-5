"""Cleaned 17-4PH dataset for Group 5: one function, every step documented.

    import sys; sys.path.append('../../src')
    from group5_clean import load_clean
    ph = load_clean()          # 185 rows, 31 papers (17-4PH only)

Each step below is described in docs/cleaning-log.md. The function only reads
data/am_properties.xlsx (kept on your own laptop, never committed) and returns a
DataFrame; nothing is written to disk.

Columns added on top of group5_data.load_data():
    paper       first author + year; rows with a missing year get their paper's year
    condition   As-built / Heat treated / HIP / Unknown (blank labels checked paper by paper)
    ht_route    named heat treatment, e.g. "Solution + H900", "Direct age H900"
    ht_group    ht_route with rare routes merged into "Other HT" (for models)
    make        printer make, recovered from the Model column and filled down within each paper
    El_usable   elongation, blanked where the column holds reduction of area (Leo 2021)
    xl_row      row number in the Excel file (for tracing back to the source)
    ml_yield    True if the row can be used to model yield (4 laser settings + condition + YS)
"""
import re

import numpy as np
import pandas as pd

from group5_data import load_data

# ---------------------------------------------------------------- paper key
AUTHOR_FIXES = {"rhafi": "rafi", "pasebania": "pasebani", "lasgari": "lashgari",
                "fachini": "facchini", "tzu-hou hsu": "hsu"}
# Same paper filed under two different years.
YEAR_FIXES = [("mahmoudi", None, 2017), ("yadollahi", 2016, 2017)]

# ---------------------------------------------------------------- blank heat-treatment labels
# 50 rows have no Y/N/HIP label. Every paper was checked (paper text, abstract, or an
# as-built "twin" row in the same paper). Evidence is in docs/cleaning-log.md.
BLANK_LABEL_DECISIONS = {
    "rashid 2017": "As-built", "sabooni 2021": "As-built", "irrinki 2018": "As-built",
    "leo 2021": "As-built", "kudzal 2017": "As-built", "facchini 2010": "As-built",
    "sun 2020": "As-built", "vunnam 2019": "As-built", "yadollahi 2017": "As-built",
    "weaver 2021": "Unknown",
}

# ---------------------------------------------------------------- row-level corrections
LEO_EL_IS_REDUCTION_OF_AREA = "leo 2021"
PASEBANI_DOUBLE_ENTERED_ROWS = (1398, 1401)   # repeat the measurements of rows 1218-1221
ESKANDARI_REVERSED_STEPS = (1302, 1304)       # ageing listed before the 1040 °C solution step

MAIN_ROUTES = ["As-printed", "Solution only", "Direct age H900", "Solution + H900", "Solution + H1025"]


def _paper_key(df):
    a = df["author"].astype(str).str.strip().str.lower().replace(AUTHOR_FIXES)
    y = df["year"].copy()
    for author, old, new in YEAR_FIXES:
        m = a == author if old is None else (a == author) & (y == old)
        y[m] = new
    known = pd.DataFrame({"a": a, "y": y}).dropna().groupby("a").y.agg(lambda s: sorted(set(s)))
    y2 = y.copy()
    for i in y[y.isna()].index:
        ys = known.get(a[i], [])
        y2[i] = ys[0] if len(ys) == 1 else np.nan
    key = (a + " " + y2.map(lambda v: "" if pd.isna(v) else str(int(v)))).str.strip()
    # Continuation rows with no year that belong to the paper above them.
    return key.replace({"shi": "shi 2021", "yadollahi": "yadollahi 2017"})


def _make_from_model(m):
    if pd.isna(m):
        return np.nan
    s = str(m).lower()
    if "3d" in s or "prox" in s or "pro x" in s:
        return "3D Systems"
    if "eos" in s:
        return "EOS"
    if "renishaw" in s:
        return "Renishaw"
    if "concept" in s or "lasercusing" in s:
        return "Concept Laser"
    if s.startswith("slm"):
        return "SLM Solutions"
    return np.nan


def _route(r):
    temps = [x for x in (r.HT1_temp_C, r.HT2_temp_C) if pd.notna(x)]
    ages = [x for x in temps if x < 950]
    if r.condition == "As-built":
        return "As-printed"
    if r.condition == "HIP":
        return "HIP + age" if ages else "HIP"
    if r.condition != "Heat treated":
        return "Unknown"
    sol = any(x >= 950 for x in temps)
    if pd.notna(r.HT1_temp_C) and pd.notna(r.HT2_temp_C) and r.HT1_temp_C < 950 <= r.HT2_temp_C:
        return "Step order unclear"
    if not ages:
        return "Solution only" if sol else "HT, temps not given"
    if len(ages) == 2:
        return "Double age"
    a = ages[0]
    name = ("H900" if 465 <= a <= 500 else "H1025" if 540 <= a <= 560
            else "H1150" if 610 <= a <= 630 else f"{a:.0f} °C")
    return ("Solution + " if sol else "Direct age ") + name


def load_clean(path=None, verbose=False):
    """Return the cleaned 17-4PH table (185 rows from 31 papers)."""
    df = load_data(path) if path else load_data()
    df["xl_row"] = df.index + 2
    raw = pd.read_excel(path) if path else pd.read_excel(load_data.__defaults__[0])
    raw.columns = [" ".join(str(c).split()) for c in raw.columns]
    df["atomisation"] = raw["Method"].astype(str).str.strip().replace({"nan": np.nan})
    df["ht_label_raw"] = raw["Treated (HIP/Y/N)"]
    df["paper"] = _paper_key(df)
    log = [("17-4PH rows in the file", int((df.material == "17-4PH").sum()))]

    # 1. wrong / modified alloy (Rafi 2013 is 15-5PH; Hsu is ODS-modified)
    d = df[(df.material == "17-4PH") & df.issue.isna()].copy()
    log.append(("after removing wrong/modified alloy", len(d)))

    # 2. the same paper entered twice
    cond0 = d.treatment.replace({"As-built (not stated)": "As-built"})
    key = d.paper.str.split().str[0].to_frame("_a").assign(
        power_W=d.power_W, speed_mm_s=d.speed_mm_s, layer_um=d.layer_um, hatch_um=d.hatch_um, c=cond0,
        YS=d.YS_MPa, UTS=d.UTS_MPa, El=d.elongation_pct, rho=d.density_pct, HV=d.hardness_HV)
    has_prop = d[["YS_MPa", "density_pct", "hardness_HV", "UTS_MPa"]].notna().any(axis=1)
    d = d[~(key.duplicated(keep="first") & has_prop)].copy()
    log.append(("after removing duplicate papers", len(d)))

    # 3. condition: labelled rows as filed; blank labels from the paper check
    d["condition"] = d.treatment.replace({"As-built (not stated)": "As-built"})
    blank = d.ht_label_raw.isna()
    for paper, cond in BLANK_LABEL_DECISIONS.items():
        d.loc[blank & (d.paper == paper), "condition"] = cond

    # 4. corrections
    d["El_usable"] = d.elongation_pct.where(d.paper != LEO_EL_IS_REDUCTION_OF_AREA)
    lo, hi = PASEBANI_DOUBLE_ENTERED_ROWS
    d = d[~d.xl_row.between(lo, hi)].copy()
    log.append(("after removing double-entered Pasebani rows", len(d)))
    dup = d.duplicated(["paper", "YS_MPa", "UTS_MPa", "El_usable", "density_pct"], keep="first") & d.YS_MPa.notna()
    d = d[~dup].copy()
    log.append(("after removing repeated yield measurements", len(d)))

    # 5. printer make: Manufacturer column, else recovered from Model, then filled down in each paper
    d["make"] = d.manufacturer
    rec = d.make.isna() & d.printer_model.map(_make_from_model).notna()
    d.loc[rec, "make"] = d.loc[rec, "printer_model"].map(_make_from_model)
    d["make"] = d.groupby("paper").make.transform(lambda s: s.ffill().bfill())

    # 6. named heat-treatment route
    d["ht_route"] = d.apply(_route, axis=1)
    d["ht_group"] = d.ht_route.where(d.ht_route.isin(MAIN_ROUTES), "Other HT")

    p4 = d[["power_W", "speed_mm_s", "layer_um", "hatch_um"]].notna().all(axis=1)
    d["ml_yield"] = d.condition.isin(["As-built", "Heat treated", "HIP"]) & p4 & d.YS_MPa.notna()
    if verbose:
        for step, n in log:
            print(f"{n:4d}  {step}")
        print(f"{d.paper.nunique():4d}  papers")
    return d.reset_index(drop=True)


if __name__ == "__main__":
    ph = load_clean(verbose=True)
    print(ph.ht_route.value_counts())
