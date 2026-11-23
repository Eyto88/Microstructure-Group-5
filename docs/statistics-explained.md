# Statistics we use, explained

Short, plain explanations for the Q&A. Code: [`src/group5_stats.py`](../src/group5_stats.py).

## Pearson vs Spearman correlation

Both answer "does Y go up when X goes up?" and run from −1 to +1 (0 = no link).

| | Pearson r | Spearman ρ |
|---|---|---|
| Question | How close are the points to a straight line? | Does Y keep rising (or falling) as X rises, in any shape? |
| How | r = cov(X, Y) / (σ<sub>X</sub> σ<sub>Y</sub>) on the raw values | Replace each value by its rank (1st, 2nd, …), then Pearson on the ranks |
| One extreme value | Can swing it a lot | Small effect: it just becomes the top or bottom rank |
| Use for | Clean, straight-line data | Curved trends, outliers, small/messy data (**ours**) |

- **Covariance** measures whether X and Y move together: for each point, is X above its average *and* Y above its average (adds), or one above and one below (subtracts)? Dividing by the two standard deviations removes the units, giving −1 to +1.
- Always give **n** and **p**: ρ = 0.4 from 8 points can easily be chance.
- **Our rule:** Spearman, with **one point per paper and setting**, so a paper with 28 rows doesn't get 28 votes.

## Kruskal–Wallis and ε² ("how much does the grouping explain?")

Used to ask: does the **paper (lab)** or the **printer brand** explain more of the spread in a property?

1. **Rank** all n samples from lowest (1) to highest (n), ignoring groups. Ranks stop one extreme value dominating.
2. For each group i (e.g. each paper), add up its ranks R<sub>i</sub> (n<sub>i</sub> samples). If the grouping didn't matter, every group's average rank would be near the middle. The test statistic measures how far they are:
   H = 12 / (n(n+1)) × Σ R<sub>i</sub>²/n<sub>i</sub> − 3(n+1)
3. Turn H into an effect size from 0 to 1 (k = number of groups):
   **ε² = (H − k + 1) / (n − k)**, roughly the share of the spread (in ranks) explained by the grouping.

**Comparing within one heat treatment:** before ranking heat-treated samples, subtract each named treatment's median. Then a sample's number means "how far above or below normal for its own recipe", so differences *between* recipes (H900 vs H1025) don't count.

**Chance check (shuffle test):** randomly reshuffle which paper each sample belongs to, recompute ε², repeat 500 times. If the real ε² is above what 95% of shuffles give, it isn't luck from small groups.

**Caution:** with many groups of 1–2 samples, ε² comes out high easily, so give the number of groups and samples, and compare with the shuffle level.

## Testing a model: random split vs whole papers held out

- **Random split (KFold):** hide a random 20% of rows, train on the rest, repeat. Rows from the same paper end up on both sides, so the model has already "met" that lab. Because each lab uses its favourite settings, the model can recognise the lab and recall its results: memorising, not learning physics.
- **Whole papers held out (GroupKFold):** all of a paper's rows are either in training or in testing. The model has to predict a lab it has never seen, which is how an engineer would actually use it.
- **Baseline:** always compare with "predict the median for that heat treatment". A model that can't beat it isn't using the laser settings usefully.
- **R²:** share of the variation the predictions explain. 1 = perfect, 0 = no better than always guessing the average, below 0 = worse than that. **MAE** = average size of the error, in MPa.
