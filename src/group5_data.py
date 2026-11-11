"""Shared data loading and cleaning for Group 5 (17-4PH vs 316L).

Use this in any new notebook so everyone works from the same cleaned data:

    import sys; sys.path.append('../../src')   # from notebooks/<folder>/
    from group5_data import load_data
    df = load_data()                 # all materials, cleaned
    ph = df[df.material == '17-4PH']

The course notebooks (notebooks/group5/) read the raw file directly and do not
use this module - that's fine, they are kept close to the originals on purpose.
"""
from pathlib import Path
import re

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = REPO_ROOT / "data" / "am_properties.xlsx"

# Short, code-friendly names for the columns we use most.
COLUMNS = {
    "Material": "material",
    "Author's Last Name": "author",
    "Year": "year",
    "Link to paper": "link",
    "Manufacturer": "manufacturer_raw",
    "Model": "printer_model",
    "Powder Size Distribution (μm)": "powder_size",
    "Laser Power (W)": "power_W",
    "Scanning Speed (mm/s)": "speed_mm_s",
    "Layer Thickness (um)": "layer_um",
    "Hatch Spacing (um)": "hatch_um",
    "Beam Size (um)": "beam_um",
    "Scanning strategy": "scan_strategy",
    "Building Direction": "build_direction",
    "Volumetric energy density (J/mm3)": "VED_J_mm3",
    "Consolidation (%)": "density_pct",
    "Treated (HIP/Y/N)": "treated_raw",
    "Temperature (°C)": "HT1_temp_C",
    "Time (Hrs)": "HT1_time_h",
    "Temperature 2 (°C)": "HT2_temp_C",
    "Time 2 (Hrs)": "HT2_time_h",
    "Hardness (HV)": "hardness_HV",
    "Test direction": "test_direction",
    "Yield Stress (MPa)": "YS_MPa",
    "Ultimate Tensile Stress (MPa)": "UTS_MPa",
    "Elongation (%)": "elongation_pct",
    "Average Work Hardening": "work_hardening",
    "Average Grain Size (μm)": "grain_size_um",
}
NUMERIC = ["year", "power_W", "speed_mm_s", "layer_um", "hatch_um", "beam_um", "VED_J_mm3",
           "density_pct", "HT1_temp_C", "HT1_time_h", "HT2_temp_C", "HT2_time_h", "hardness_HV",
           "YS_MPa", "UTS_MPa", "elongation_pct", "work_hardening", "grain_size_um"]

# Messy manufacturer spellings -> one name each (extend as you find more).
MANUFACTURERS = [
    (r"\beos", "EOS"),
    (r"3d\s*systems", "3D Systems"),
    (r"slm\s*solution", "SLM Solutions"),
    (r"concept\s*laser", "Concept Laser"),
    (r"renishaw", "Renishaw"),
    (r"riton", "Guangzhou Riton"),
    (r"\bipg", "IPG"),
    (r"aconity", "Aconity3D"),
    (r"sisma", "SISMA"),
    (r"phenix", "Phenix"),
    (r"\bmtt", "MTT"),
]

# Author spellings that refer to the same group/paper in the 17-4PH data.
AUTHOR_FIXES = {"rhafi": "rafi", "pasebania": "pasebani", "lasgari": "lashgari",
                "fachini": "facchini", "tzu-hou hsu": "hsu"}

# Known data-quality issues found while reviewing the 17-4PH papers.
# Matched on (cleaned author, year); year None = any year.
KNOWN_ISSUES = {
    ("rafi", 2013): "Paper is on 15-5 PH, not 17-4PH",
    ("hsu", None): "Oxide-dispersion-strengthened (modified) 17-4PH",
}


def _clean_manufacturer(x):
    if pd.isna(x) or str(x).strip().lower() in {"", "nan", "none"}:
        return np.nan
    s = str(x).strip().lower()
    for pattern, name in MANUFACTURERS:
        if re.search(pattern, s):
            return name
    return str(x).strip(" ()")


def _clean_treatment(x):
    s = str(x).strip().upper()
    if s == "HIP":
        return "HIP"
    if s == "Y":
        return "Heat treated"
    if s == "N":
        return "As-built"
    return "As-built (not stated)"


def load_data(path=DATA_FILE, materials=None, drop_known_issues=False):
    """Load am_properties.xlsx and return a tidy DataFrame.

    Adds: material ('174PH' -> '17-4PH'), manufacturer (cleaned), treatment
    (As-built / Heat treated / HIP / As-built (not stated)), paper (author + year
    key for grouping rows from the same study), issue (known data problems).
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Put the workshop's am_properties.xlsx in the data/ folder "
            "(see data/README.md).")
    raw = pd.read_excel(path)
    raw.columns = [" ".join(str(c).split()) for c in raw.columns]
    df = raw.rename(columns=COLUMNS)[[c for c in COLUMNS.values() if c in raw.rename(columns=COLUMNS)]].copy()

    df["material"] = df["material"].astype(str).str.strip().replace({"174PH": "17-4PH", "MS": "18Ni300"})
    for c in NUMERIC:
        if c in df:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df["manufacturer"] = df["manufacturer_raw"].map(_clean_manufacturer)
    df["treatment"] = df["treated_raw"].map(_clean_treatment)

    author = df["author"].astype(str).str.strip().str.lower().replace(AUTHOR_FIXES)
    df["paper"] = author + " " + df["year"].map(lambda y: "" if pd.isna(y) else str(int(y)))
    df["paper"] = df["paper"].str.strip()

    def issue(row):
        a = AUTHOR_FIXES.get(str(row["author"]).strip().lower(), str(row["author"]).strip().lower())
        for (au, yr), msg in KNOWN_ISSUES.items():
            if a == au and (yr is None or row["year"] == yr) and row["material"] == "17-4PH":
                return msg
        return np.nan
    df["issue"] = df.apply(issue, axis=1)

    # Recompute VED = P / (v * h * t) to check the recorded value.
    df["VED_calc"] = df["power_W"] / (df["speed_mm_s"] * df["hatch_um"] / 1000 * df["layer_um"] / 1000)

    if drop_known_issues:
        df = df[df["issue"].isna()]
    if materials is not None:
        df = df[df["material"].isin(materials)]
    return df.reset_index(drop=True)


def summary(df, materials=("17-4PH", "316L")):
    """Quick table: rows, papers and how many values each key property has."""
    cols = ["power_W", "speed_mm_s", "density_pct", "hardness_HV", "YS_MPa", "UTS_MPa",
            "elongation_pct", "work_hardening", "manufacturer"]
    sub = df[df["material"].isin(materials)]
    out = sub.groupby("material")[cols].count()
    out.insert(0, "papers", sub.groupby("material")["paper"].nunique())
    out.insert(0, "rows", sub.groupby("material").size())
    return out


if __name__ == "__main__":
    d = load_data()
    print(summary(d).T)
    print("\nTreatment split:\n", d[d.material.isin(["17-4PH", "316L"])]
          .groupby(["material", "treatment"]).size())
    print("\nRows with known issues:", d["issue"].notna().sum())
