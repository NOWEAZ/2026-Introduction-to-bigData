# Task 2 · Curse of Dimensionality — Contrast Curve

## A2 · Measurements Across Dimensions

### Table 1: $n = 1,000$ Points (20,000 Sampled Pairs)

| Dimension ($d$) | Mean Distance | Min Distance | Max Distance | Spread ($\sigma$) | Contrast $\frac{\max - \min}{\min}$ | Relative Stdev $\frac{\sigma}{\mu}$ | Time (s) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 0.521 | 0.003 | 1.326 | 0.248 | 488.582 | 0.476 | 0.019 |
| 5 | 0.884 | 0.111 | 1.687 | 0.249 | 14.257 | 0.282 | 0.024 |
| 10 | 1.274 | 0.438 | 2.159 | 0.245 | 3.925 | 0.193 | 0.033 |
| 20 | 1.815 | 0.821 | 2.670 | 0.245 | 2.253 | 0.135 | 0.050 |
| 50 | 2.867 | 1.909 | 3.785 | 0.238 | 0.982 | 0.083 | 0.101 |
| 100 | 4.068 | 3.206 | 4.954 | 0.243 | 0.545 | 0.060 | 0.189 |
| 200 | 5.776 | 4.871 | 6.682 | 0.239 | 0.372 | 0.041 | 0.372 |

### Table 2: $n = 2,000$ Points (20,000 Sampled Pairs)

| Dimension ($d$) | Mean Distance | Min Distance | Max Distance | Spread ($\sigma$) | Contrast $\frac{\max - \min}{\min}$ | Relative Stdev $\frac{\sigma}{\mu}$ | Time (s) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 50 | 2.871 | 1.899 | 3.839 | 0.237 | 1.022 | 0.083 | 0.106 |
| 200 | 5.772 | 4.695 | 6.799 | 0.240 | 0.448 | 0.042 | 0.373 |
| 500 | 9.126 | 8.099 | 10.176 | 0.240 | 0.256 | 0.026 | 0.903 |
| 1000 | 12.909 | 11.970 | 13.806 | 0.240 | 0.153 | 0.019 | 1.803 |

---

## A3 · Contrast Decay and Thresholds

Contrast $(\max - \min) / \min$ collapses precipitously as dimension increases:
- At $d = 2$, the furthest pair is ~489× further apart than the closest pair (`contrast = 488.582`).
- **Drops below 1.0**: Around **$d \approx 50$** (for $n = 1,000$, contrast at $d = 50$ is `0.982`, meaning the furthest pair is less than $2\times$ the distance of the closest pair).
- **Drops below 0.5**: Around **$d \approx 115\text{--}120$** (contrast is `0.545` at $d = 100$ and `0.372` at $d = 200$). By $d = 1000$, contrast shrinks to `0.153`—all pairwise distances lie within a narrow 15% band above the minimum.

---

## A4 · How Mean Distance Grows with Dimension

For two independent uniform points $X, Y \in [0, 1]^d$, each coordinate difference $(X_k - Y_k)^2$ has expectation $\mathbb{E}[(X_k - Y_k)^2] = \frac{1}{6}$ and variance $\frac{7}{180}$. By the Law of Large Numbers and Central Limit Theorem:
$$\mu(d) \approx \sqrt{\frac{d}{6}} \approx 0.4082 \sqrt{d}$$
Checking our measured numbers:
- $d = 20 \to 200$ ($10\times$ increase in $d$): mean grows from `1.815` to `5.776` ($5.776 / 1.815 = 3.182 \approx \sqrt{10} = 3.162$).
- $d = 50 \to 500$ ($10\times$ increase in $d$): mean grows from `2.871` to `9.126` ($9.126 / 2.871 = 3.178 \approx \sqrt{10}$).
- $d = 100 \to 1000$ ($10\times$ increase in $d$): mean grows from `4.068` to `12.909` ($12.909 / 4.068 = 3.173 \approx \sqrt{10}$).
- At $d = 1000$, $\sqrt{1000 / 6} = 12.910$, matching the measured `12.909` to three decimal places. Thus, mean distance grows **proportionally to $\sqrt{d}$**, not linearly in $d$.

---

## A5 · Relative Standard Deviation vs. Contrast

Notice that the absolute standard deviation $\sigma$ stays virtually constant around `0.24` across all dimensions from $d = 2$ to $d = 1000$ (since by the delta method, $\text{Var}(\sqrt{S_d}) \approx \frac{\text{Var}((X_k - Y_k)^2)}{4 \mathbb{E}[(X_k - Y_k)^2]} = \frac{7/180}{4/6} = \frac{7}{120} \implies \sigma \approx \sqrt{7/120} \approx 0.2415$).
Because $\sigma \approx 0.2415$ is constant while $\mu \approx \sqrt{d/6}$ grows as $\sqrt{d}$, the **relative standard deviation** $\sigma / \mu$ decays smoothly as $O(1/\sqrt{d})$:
- $d = 2$: `0.476`
- $d = 20$: `0.135`
- $d = 200$: `0.041`
- $d = 1000$: `0.019`

**Which better captures "distance stopped meaning anything"?**
- **Relative standard deviation ($\sigma / \mu$)** is a much more stable, distribution-level metric of concentration of measure because it depends on all pairs and is invariant to single-pair extreme outliers or sample size $n$.
- **Contrast**, however, directly measures the extreme gap between the single closest and single furthest pair in a finite sample, which is what nearest-neighbor queries actually see—though it is noisy at low dimensions because a single lucky close pair makes $\min \to 0$ and explodes the ratio.

---

## A6 · Dependence on Point Count ($n$)

Comparing $n = 1,000$ vs. $n = 2,000$ at fixed dimensions:
- At $d = 50$: `contrast = 0.982` ($n = 1000$) vs. `1.022` ($n = 2000$), while `relative_stdev` is unchanged (`0.083` vs. `0.083`).
- At $d = 200$: `contrast = 0.372` ($n = 1000$) vs. `0.448` ($n = 2000$), while `relative_stdev` is essentially unchanged (`0.041` vs. `0.042`).

Why? Contrast depends on the sample minimum and maximum over the pool of available point pairs. With more points (or more pairs examined), you sample further into the tails of the distance distribution, finding a slightly smaller $\min$ and slightly larger $\max$, which nudges contrast upward logarithmic-slowly in $n$. However, because the tail decays sub-Gaussianly with constant $\sigma \approx 0.24$, increasing $n$ only buys a tiny $O(\sqrt{\ln n})$ spread, which is quickly overwhelmed by the $\sqrt{d}$ growth of the mean.

---

## A7 · Machine and Timing

- **Platform**: `Windows-11-10.0.26200-SP0`
- **Processor**: `AMD64 Family 25 Model 97 Stepping 2, AuthenticAMD`
- **Python**: `3.14.8`
- **Largest run ($d = 1000, n = 2000, 20000\text{ pairs}$)**: `1.803s`

---

## A8 · Does This Threaten LSH on Jaccard Similarity (Week 3)?

**No — not for real document shingle sets.**
The curse of dimensionality measured here relies on **uniformly and independently distributed dense coordinates** in a hypercube $[0, 1]^d$, where every dimension contributes independent noise of equal magnitude so that distances concentrate around $\sqrt{d/6}$.
In contrast, Week 3's LSH operates on **sparse binary shingle vectors** representing real documents:
1. **Extreme sparsity and non-uniformity**: A document only contains a tiny fraction of the universe of all possible $k$-shingles, and Jaccard similarity ignores shared zeros ($0\text{--}0$ matches), looking only at the union of active shingles in the two documents.
2. **Low intrinsic dimensionality / planted structure**: Near-duplicate or topically related documents share specific phrases and correlations rather than independent uniform random bits, so genuine near-neighbors maintain high Jaccard similarity ($\ge 0.5$) while unrelated documents have Jaccard similarity near $0$, preserving a huge contrast ratio regardless of vocabulary size.

