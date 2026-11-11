# Findings

One section per analysis. Write the **result**, the **number/figure** behind it, and **what it means** — this becomes the slides and our Q&A prep.

## Data overview

- 219 rows of 17-4PH from ~44 papers (all LPBF); 316L has 278 rows from 22 papers.
- ~121 of the 17-4PH rows are heat treated or HIPed; almost all 316L rows are as-built.
- Only 56 17-4PH rows record the printer manufacturer.

## EDA & correlations

-

## Printer effect

- Note: with so few 17-4PH manufacturer values, check whether the result is driven by 316L or by one paper.

## Dimension reduction (PCA)

-

## Process maps — 17-4PH

| Output | What the map shows | Rows used |
|---|---|---|
| Consolidation | | |
| Yield stress | | |
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
- Ozsoy 2021 supplies 28 rows (13%), so it can dominate maps.

## Likely Q&A questions

- Why is the as-built yield strength of LPBF 17-4PH lower than wrought H900?
- Why does powder atomisation gas (N₂ vs Ar) matter?
- Is the "printer effect" real or a paper/lab effect?
- Why can't you just use volumetric energy density (VED) as the single process variable?
-
