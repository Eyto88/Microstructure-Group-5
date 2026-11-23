# Cleaning log: 17-4PH (219 → 185 rows, 31 papers)

Everything here is done in code by `load_clean()` in [`src/group5_clean.py`](../src/group5_clean.py), so anyone can rerun it. Row numbers are Excel rows in `am_properties.xlsx` (column `xl_row`).

## Row counts

| Step | Rows left | What was removed and why |
|---|---|---|
| 17-4PH rows in the file | 219 | |
| Wrong or modified alloy | 205 | Rafi 2013 studies **15-5PH**, not 17-4PH; Hsu 2019 is an **ODS-modified** 17-4PH (14 rows) |
| Same paper entered twice | 196 | Identical settings, condition and properties under a different spelling or year (Mahmoudi 2016/2017, Pasebani/Pasebania, Rafi/Rhafi, …); 9 rows |
| Double-entered Pasebani rows | 192 | Rows 1398–1401 have the same yield/UTS/elongation/hardness as rows 1218–1221 but different HT temperature, density and settings: the same measurements copied with the wrong metadata (grain size 0.035 µm is also impossible) |
| Repeated measurements | 185 | Rows in the same paper with identical yield, UTS, elongation and density: copies, not new samples (e.g. Leo 2021 has 3 values entered 3 times; one Molaei row appears twice) |

## Paper key

Rows are grouped by **first author + year** (`paper`), because rows from one paper share the same powder, printer, furnace and test rig.

- Author spellings are merged (Rhafi → Rafi, Pasebania → Pasebani, Lasgari → Lashgari, Fachini → Facchini, Tzu-Hou Hsu → Hsu).
- Rows with a missing year get their paper's year. Two continuation blocks had no year at all and were counted as separate papers before: **"Shi" → Shi 2021** and **"Yadollahi" → Yadollahi 2017**.
- "Paper" stands in for "lab". It's approximate: some groups publish several papers (e.g. Qin 2023 and Shi 2021 share authors).

## Heat-treatment labels

50 of the 196 rows had a blank `Treated (HIP/Y/N)`. We didn't assume; each paper was checked.

| Paper | Decision | Evidence |
|---|---|---|
| Rashid 2017 | As-built | Same settings and densities as its heat-treated rows; hardness 315–346 HV vs 450–458 HV after HT (as-built twins) |
| Sabooni 2021 | As-built | Same settings as its HT and HIP rows; yield 500 vs 1100/1230 MPa |
| Irrinki 2018 | As-built | Paper reports as-printed properties for gas- and water-atomised powder; no HT described |
| Leo 2021 | As-built | Full text: only post-build step is wire-EDM removal |
| Kudzal 2017 | As-built | ≥25% retained austenite reported, which solution + ageing would remove |
| Facchini 2010 | As-built | Paper is on metastable austenite in as-built parts; YS/UTS = 0.46 (as-built signature) |
| Sun 2020 | As-built | As-built thin-wall study; hardness in the as-built range |
| Vunnam 2019 | As-built | Title is about the as-built microstructure (row has no property values) |
| Yadollahi 2017 | As-built | Exact copy of an N-labelled row |
| Weaver 2021 | **Unknown** | Not stated; excluded from anything split by condition |

A classifier trained on the labelled rows guessed the blanks wrongly for 7 of 9 papers, so condition has to come from the paper, not be inferred from the numbers.

## Named heat treatment (`ht_route`)

"Treated = Y" mixes very different recipes, so each heat-treated row is named from its temperatures:

- **Solution** = a step at ≥ 950 °C (usually ~1040 °C). Ageing named after its temperature in °F: **H900** (465–500 °C), **H1025** (540–560 °C), **H1150** (610–630 °C).
- **"Solution + H900"** = solution then age; **"Direct age H900"** = ageing only, no solution step.
- Other cases: Solution only, Double age, HIP, HIP + age, other ageing temperatures.
- **Eskandari 2021 rows 1302–1304** list the ageing step *before* the 1040 °C solution step, so they're labelled "Step order unclear" rather than guessed.
- `ht_group` merges routes used by fewer than ~5 papers into "Other HT" for modelling.

## Other corrections

- **Leo 2021 elongation** is actually reduction of area (Table 5 gives no elongation), so `El_usable` is blank for it.
- **Printer make** is often only written on the first row of each paper. It's recovered from the Model column where needed and **filled down within each paper**: printer known for 177 of 185 rows (113 before filling).
- Printer **model** names in some rows are Excel drag-fill artefacts (ProX301…307); the make is still right.
- **Ozsoy 2021** alone supplies 28 rows (15%); check results with and without it.
