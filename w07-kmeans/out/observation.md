# Week 7 · Observations

## Task 1 · k-means and Initialisation

- **Empty cluster handling (R3)**: When a cluster loses all its points, `update` relocates its centroid to the data point furthest from any currently non-empty cluster centroid (`max_i min_c d(p_i, c)`). This splits the highest-SSE region and guarantees $k$ active clusters, whereas the alternative of keeping the old centroid leaves a dead, zero-member cluster sitting idle whenever other centroids wall it off.
- **Success rate over 40 seeds**: On `BLOBS`, `k-means++` recovered the three true blobs (`SSE = 0.120`) on **40 out of 40 seeds (100%)**, whereas `random` initialisation found them on **27 out of 40 seeds (67.5%)** and got trapped in a bad local optimum (`SSE ≈ 96.1`, where two centroids split one blob and one centroid straddles two blobs) on **13 out of 40 seeds (32.5%, mean SSE `31.313`)**.
- **Cost vs. payoff of `k-means++`**: `k-means++` spends $O(n k)$ distance evaluations up front to spread starting centroids across well-separated clusters, buying both much lower final SSE and fewer Lloyd iterations to converge; you would only skip it when $k$ is huge and streaming/pass constraints forbid $k$ sequential scans over the dataset (where parallel `k-means||` or random sampling is used instead).
- **Why not choose $k$ by minimising SSE**: Monotonically increasing $k$ always provides more degrees of freedom to reduce within-cluster distance, reaching the trivial global minimum $\text{SSE} = 0$ at $k = n$ (one cluster per point, pure overfitting); choosing $k$ requires an elbow/knee criterion or an information/complexity penalty (such as BIC/AIC or silhouette score).

---

## Task 2 · The Curse of Dimensionality

- **Where contrast drops below 1**: For $n = 1,000$ uniform points in $[0, 1]^d$ (20,000 random pairs), contrast $(\max - \min)/\min$ drops below `1.0` at **$d = 50$** (`contrast = 0.982`) and below `0.5` around **$d \approx 115\text{--}120$** (`0.545` at $d = 100$, `0.372` at $d = 200$).
- **Effect of point count $n$ (A6)**: Increasing $n$ from `1,000` to `2,000` slightly increases contrast at fixed dimension (`0.982 → 1.022` at $d = 50$; `0.372 → 0.448` at $d = 200$) while leaving relative standard deviation ($\sigma / \mu$) unchanged (`0.083` and `0.041`), because larger samples probe slightly further into the $O(\sqrt{\ln n})$ extremes of the distance distribution without changing its underlying concentration around $\mu \approx \sqrt{d/6}$.
- **Does this threaten LSH on Jaccard similarity (A8)?**: **No.** The Euclidean curse relies on dense, independent uniform coordinates where every dimension adds equal-variance background noise, whereas document shingle sets in Week 3 are extremely sparse binary vectors with low intrinsic dimensionality where Jaccard similarity ignores shared zeros ($0\text{--}0$) and preserves high contrast between true near-duplicates and unrelated documents.

---

## Task 3 · Triangle-Inequality Pruned k-means

- **Per-point storage**: We store **2 extra floats per point** (`40,000` floats total for $n = 20,000$): an upper bound $u[i] \ge d(p_i, c_{a[i]})$ on the distance to its assigned centroid, and a lower bound $l[i] \le \min_{j \ne a[i]} d(p_i, c_j)$ on the distance to the second-closest centroid.
- **Which bound does the work and maintenance cost (R5)**: The per-point lower/upper bound test $u[i] \le \max(l[i], s[a[i]])$ (where $s[a] = \frac{1}{2}\min_{j \ne a} d(c_a, c_j)$) eliminates **88.9%** of all distance evaluations (`1,146,949` calls vs. `10,320,000` in baseline, cutting runtime from `23.62s` to `3.51s`); maintaining it costs only $k = 12$ centroid-shift distances and $\binom{k}{2} = 66$ inter-centroid distances per iteration (`78` distance calls per pass, or `3,276` calls across 42 passes = `0.03%` of baseline) plus $O(n)$ scalar additions/subtractions.
- **Why SSE difference is exactly zero**: Our final SSE is `10,737,882.94` (`0.0000%` drift, identical to the last digit and same `43` iterations) because triangle-inequality pruning is **exact**: it skips a distance calculation only when $d(p_i, c_{a[i]}) \le u[i] < \min_{j \ne a[i]} d(p_i, c_j)$ is mathematically guaranteed, so every single point receives the exact same cluster assignment on every single iteration as `NaiveKMeans`.
- **First-iteration fraction**: Iteration 1 cannot prune anything and performs $n \times k = 20,000 \times 12 = 240,000$ distance evaluations, which accounts for **$20.9\%$** (`240,000 / 1,146,949`) of all distance computations across the entire 43-iteration run.

