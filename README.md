# Microstructure Workshop — Group 5: 17-4PH (PH174)

Laser powder bed fusion (LPBF) meta-analysis of **17-4PH precipitation-hardening stainless steel**, compared with **316L**.

> Data and code are by **Drs Raymond Wong and Bogdan Dovgyy**. Cite their paper in the slides:
> Wong et al., *Critical statistical assessment of data in metal additive manufacturing*, Materials & Design (2025) — https://www.sciencedirect.com/science/article/pii/S026412752500721X

## Key dates

| Date | What |
|---|---|
| **7 Dec 2026, 3pm** | Slides submitted (15 min talk + up to 2 appendix slides on who did what) |
| **9 Dec 2026** | Presentation: 15 min + up to 20 min Q&A — **everyone gets asked questions** |

Internal milestones are in [`docs/plan.md`](docs/plan.md).

## Where to find things

| Folder | What goes in it |
|---|---|
| [`docs/`](docs/) | Brief summary, task owners & timeline, meeting notes |
| [`literature/`](literature/) | Reading list + one notes file per topic for the lit review |
| [`data/`](data/) | `am_properties.xlsx` goes here **on your own laptop only** (not committed) |
| [`notebooks/group5/`](notebooks/group5/) | **The notebooks we run** — EDA, Dimension Reduction, Process Maps, set up for 17-4PH + 316L |
| [`notebooks/course_original/`](notebooks/course_original/) | Untouched course notebooks (outputs cleared, MIT licence), for reference only — they won't find the data from here |
| [`notebooks/analysis/`](notebooks/analysis/) | Your own extra notebooks — name them `NN_topic_initials.ipynb` |
| [`src/group5_data.py`](src/group5_data.py) | Shared loader that cleans the data (see below) |
| [`figures/`](figures/) | Figures for the slides, by section — the notebooks save here automatically |
| [`presentation/`](presentation/) | Slide outline and final deck |

## Getting started (≈10 min)

1. **Clone** the repo (GitHub Desktop: *File → Clone repository*, or `git clone https://github.com/Eyto88/Microstructure-Group-5.git`).
2. **Add the data:** copy `am_properties.xlsx` from the workshop folder into `data/`.
3. **Install packages** (Anaconda already has most):
   ```bash
   pip install -r requirements.txt
   ```
4. **Open Jupyter** from the repo folder (`jupyter notebook`), go to `notebooks/group5/` and run a notebook top to bottom.

All three notebooks in `notebooks/group5/` have been run end to end on the workshop dataset with no errors.

## What's different in our notebook copies

Compared with the course originals:
- `174PH` is renamed to `17-4PH` right after the data is loaded, and `materials_list = ['17-4PH', '316L']`.
- Data path is `../../data/am_properties.xlsx`; figures save to `figures/<section>/`.
- Two leftover cells from another project are disabled (marked *Group 5 note*), `cm.get_cmap` → `plt.get_cmap` (newer matplotlib), and the single-material process map uses `n = 0` (17-4PH).

## Shared data loader

For any **new** analysis, use the shared loader so we all work from the same cleaned data:

```python
import sys; sys.path.append('../../src')
from group5_data import load_data, summary
df = load_data()                      # all materials, cleaned
ph = df[df.material == '17-4PH']
summary(df)                           # rows/papers/value counts for 17-4PH vs 316L
```

It adds short column names, cleans manufacturer spellings (EOS / EOSINT / "EOS Germany" → `EOS`), groups treatment into *As-built / Heat treated / HIP*, adds a `paper` key, recomputes VED, and flags known problem rows in `issue`.

## What we know about the data so far

| | 17-4PH | 316L |
|---|---|---|
| Rows / papers | 219 / ~44 | 278 / 22 |
| Yield stress values | 158 | 70 |
| Density values | 125 | 273 |
| Heat treated / HIP rows | ~121 | 9 |
| Rows with a printer manufacturer | **56** | 275 |

**Things to raise in the talk:**
- **Printer effect is weak for 17-4PH**: 163/219 rows have no manufacturer — the course notebook's printer analysis ends up driven by 316L printers.
- **Heat treatment dominates 17-4PH strength** (median yield ~640 MPa as-built vs ~970 MPa heat treated), so process maps must be read by treatment.
- **Data-quality flags**: Rafi 2013 is actually 15-5 PH; Hsu 2019 is an ODS-modified 17-4PH; several papers are entered twice under different spellings; Ozsoy 2021 alone supplies 28 rows.
- **Process maps use few rows**: the "all outputs combined" map has only ~51 17-4PH and ~61 316L rows with every property filled in.

## How we work

See [`CONTRIBUTING.md`](CONTRIBUTING.md) — short version: **pull before you start, work on a branch or in your own notebook, open a pull request, never commit the data file.**

## Team

| Name | GitHub | Main area |
|---|---|---|
| | | |

*(Fill in — see `docs/plan.md` for the task split.)*
