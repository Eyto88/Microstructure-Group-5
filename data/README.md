# Data

**Put `am_properties.xlsx` here on your own laptop.** It's the dataset from the workshop folder. It is **not committed**, because the repo is public and the data belongs to the course. `.gitignore` blocks everything in this folder except this README.

```
data/
├── README.md           ← this file (committed)
└── am_properties.xlsx  ← you add this (not committed)
```

## What's in it

- 1,409 rows, 75 columns, all LPBF.
- Materials: Ti6Al4V (424), 316L (278), AlSi10Mg (249), IN718 (239), **174PH (219)**.
- 17-4PH is labelled **`174PH`** in the raw file. Both our notebooks and `src/group5_data.py` rename it to `17-4PH`.

## Column notes

- The UTS column is called `Ultimate Tensile Stress (MPa)`, not "Strength".
- The test-temperature column is misspelt `Test Temerature (℃)`.
- `Treated (HIP/Y/N)` uses `Y`, `y`, `N`, `HIP`, or blank. Blank usually means as-built, but this isn't guaranteed.

## Known issues (17-4PH)

See `docs/findings.md` → *Data-quality issues*. `load_data()` flags these rows in the `issue` column.

This is **not** the same file as the one on the public GitHub repo (`Process Parameters and Properties LPBF.xlsx`): that one has 229 rows, six other alloys, and no 17-4PH.
