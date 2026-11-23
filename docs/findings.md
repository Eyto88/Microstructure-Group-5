# Findings

One section per analysis. Write the **result**, the **number/figure** behind it, and **what it means** — this becomes the slides and our Q&A prep.

## Data overview

- 219 rows of 17-4PH from ~33 papers (all LPBF); after removing the wrong/modified alloy and duplicates, 196 rows from 31 papers. 316L has 278 rows from 22 papers. (An earlier count of ~44 split papers whose year was missing.)
- ~121 of the 17-4PH rows are heat treated or HIPed; almost all 316L rows are as-built.
- Only 56 17-4PH rows record the printer manufacturer.
- **Final cleaned set: 185 rows from 31 papers** (`load_clean()` in `src/group5_clean.py`; every step in [`cleaning-log.md`](cleaning-log.md)). Beyond the alloy and duplicate-paper fixes: 4 double-entered Pasebani rows and 7 repeated measurements removed, 50 blank heat-treatment labels checked paper by paper, Leo 2021 "elongation" is really reduction of area.
- Rows are not independent: the 5 biggest papers give 40% of rows (largest: 28 rows). Always report **papers** as well as rows.
- Printer make is usually only typed on a paper's first row; filled down within each paper it is known for 177 of 185 rows.

## EDA & correlations

Notebook: `notebooks/analysis/05_eda_lab_effect_EV.ipynb`. Methods explained in [`statistics-explained.md`](statistics-explained.md).

- **The heat treatment sets the strength level.** Median yield: as-printed 645 MPa (16 papers), solution only 801 (7), direct age H900 937 (7), solution + H900 1071 (10), solution + H1025 1154 (5). "Heat treated" must always be split by **named** treatment.
- **One recipe can still scatter widely.** Solution + H900 runs 365–1550 MPa; paper medians 790–1500, and only 4 of 10 papers reach the wrought H900 minimum (1170 MPa).
- Solution + H1025 looks tight (1121–1198 MPa) because 10 of its 11 rows are one process: EOS M290, 220 W / 755.5 mm/s, 1050 °C 0.5 h + 552 °C 4 h. It shows those labs agree, not that H1025 is more reliable.
- **Within one treatment, laser settings show no clear link to yield.** Spearman, one point per paper × setting: as-printed |ρ| ≤ 0.31, solution + H900 |ρ| ≤ 0.24, all p > 0.25.
- **Powder matters, but isn't the whole story.** Pasebani 2018 (same settings, solution + H900): water-atomised 365–1000 MPa at 91–95% density vs gas-atomised 1116–1255 MPa. Yet the two strongest H900 papers (Lebrun, Tyler) also used water-atomised powder.
- Tyler 2014's 1550 MPa is above typical wrought H900 and is unverified.

## Printer effect

- Note: with so few 17-4PH manufacturer values, check whether the result is driven by 316L or by one paper.
- **The lab explains far more than the printer.** Kruskal–Wallis ε² (share of spread explained; printer filled down within each paper):

| Subset | Rows | Printer brands | Papers | ε² printer | ε² paper | Paper, chance level (95% of shuffles) |
|---|---|---|---|---|---|---|
| Heat-treated yield, within the same named treatment | 72 | 5 | 18 | 0.10 (p = 0.03) | **0.28** (p = 0.01) | < 0.15 |
| As-printed yield | 31 | 3 | 14 | 0.12 (p = 0.06) | **0.82** (p = 0.01) | < 0.32 |
| As-printed density | 55 | 4 | 10 | 0.02 (p = 0.28) | **0.49** (p < 0.001) | < 0.13 |

- A per-printer ANOVA on "Treated = Y" rows looks significant, but each printer group is only 2–4 papers with different heat treatments; with one value per paper the printer difference is not significant (p = 0.17, 12 papers). Compare printers **within one named treatment** and count papers.

## Dimension reduction (PCA)

-

## Process maps — 17-4PH

| Output | What the map shows | Rows used |
|---|---|---|
| Consolidation | As-printed: density falls towards low power / high speed (lack of fusion), clearest within one study (Irrinki 2018); across papers ρ(density, P/v) = 0.46, not significant | 37 rows, 12 settings, 10 papers |
| Yield stress | No gradient, even with the treatment fixed. Solution + H900: near-identical settings (220 W, ~755 mm/s) give 1041 vs 1300 MPa; 48 W/300 mm/s and 200 W/820 mm/s both give ~1000–1100 MPa. Treatment lifts the whole map (645 → 1070 MPa) | As-printed 32 rows / 13 settings / 15 papers; solution + H900 14 / 8 / 9 |
| Elongation | | |
| Work hardening | | |
| All combined | | ~51 |

## 17-4PH vs 316L

-

## Data-quality issues

- Rafi 2013 is labelled 17-4PH but the paper studies 15-5 PH.
- Hsu 2019 is an ODS-modified 17-4PH.
- Duplicate entries under different spellings/years (Mahmoudi 2016/2017, Pasebani/Pasebania, Rafi/Rhafi, Lashgari/Lasgari).
- 153 of 219 17-4PH rows have no paper link.
- Ozsoy 2021 supplies 28 rows (15% of the cleaned set), so it can dominate maps.
- Pasebani rows 1398–1401 repeat the measurements of rows 1218–1221 with different metadata (double-entered).
- Leo 2021: 3 measurements entered 3 times; its "elongation" column is reduction of area.
- Eskandari 2021 rows 1302–1304 list ageing before the solution step.
- "Shi" and "Yadollahi" rows with no year belong to Shi 2021 and Yadollahi 2017.

## Machine learning (yield)

99 rows, 19 papers; inputs = 4 laser settings + named heat treatment; 20 repeats of 5-fold cross-validation.

| Model | R² random split | R² whole papers held out | Average error, papers held out |
|---|---|---|---|
| Random forest | 0.46 | −0.07 | 209 MPa |
| XGBoost | 0.37 | −0.16 | 213 MPa |
| Linear regression | 0.32 | −0.58 | 249 MPa |
| **Baseline: median per heat treatment** | 0.27 | **0.19** | **181 MPa** |

- With a random split the models look fine, because they recognise each lab by its favourite settings. On labs they've never seen, **no model beats the baseline**: the laser settings add noise, not information. A tuned XGBoost did worse (−0.33).
- Always test with whole papers held out (GroupKFold) and compare with this baseline.

## Likely Q&A questions

- Why is the as-built yield strength of LPBF 17-4PH lower than wrought H900?
- Why does powder atomisation gas (N₂ vs Ar) matter?
- Is the "printer effect" real or a paper/lab effect?
- Why can't you just use volumetric energy density (VED) as the single process variable?
- Did you separate the heat treatments? (Yes: named routes; the spread within Solution + H900 alone is 365–1550 MPa.)
- Why Spearman and not Pearson? Why one point per paper?
- Your model scores R² ≈ 0.5, isn't that good? (Only on a random split; on new papers it's below the baseline.)
- Would XGBoost or a neural network do better? (XGBoost: no. Too little data for a neural network, and the missing information, e.g. powder and density before ageing, isn't in the inputs.)
