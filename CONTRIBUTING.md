# How we work in this repo

Ten people, one repo — these few rules keep it from turning into a mess.

## The rules

1. **Pull before you start** (GitHub Desktop: *Fetch origin → Pull*; terminal: `git pull`).
2. **Never commit `data/am_properties.xlsx`** — it's course data and the repo is public. `.gitignore` already blocks it.
3. **Don't edit someone else's notebook.** Two people editing one `.ipynb` creates merge conflicts that are painful to fix. Copy it into `notebooks/analysis/` with your initials instead.
4. **Clear outputs before committing notebooks** (*Kernel → Restart & Clear Output*). Save figures to `figures/` instead — they're what goes in the slides.
5. **Small, clear commits:** `"Add 17-4PH process map for yield stress"`, not `"stuff"`.

## Workflow

**Simple (fine for notes, lit review, figures):** pull → edit → commit → push to `main`.

**For code changes (`src/`, `notebooks/group5/`):** use a branch and a pull request so someone else checks it.

```bash
git checkout -b eda-printer-effect      # new branch
# ...work...
git add notebooks/analysis/03_printer_effect_EV.ipynb figures/eda/
git commit -m "Printer-effect analysis for 17-4PH"
git push -u origin eda-printer-effect
# then open a Pull Request on GitHub and ask one person to review
```

## Where things go

| You're adding… | Put it in… | Name it like… |
|---|---|---|
| Lit review notes | `literature/notes/` | `heat-treatment.md` |
| A new analysis notebook | `notebooks/analysis/` | `04_pca_316L_comparison_AZ.ipynb` |
| A figure for the slides | `figures/<section>/` | `process_map_YS_17-4PH_asbuilt.png` |
| Meeting notes | `docs/meeting-notes/` | `2026-11-18.md` |
| A task / to-do | GitHub **Issues** (use the *Task* template) | — |

## Citing

Any slide using the dataset, code or figures from it must credit **Drs Raymond Wong and Bogdan Dovgyy** and cite Wong et al. (2025). Add papers you use to `literature/references.md`.
