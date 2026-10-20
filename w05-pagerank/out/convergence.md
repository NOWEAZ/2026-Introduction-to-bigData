# Task 2 · Convergence Analysis

## A2 · Iteration Table

Measured on the benchmark graph ($N = 1,200$, $\text{tol} = 10^{-10}$):

| $\beta$ | Iterations | Time (s) | Top 3 Nodes | Top-10 Ranking Changes |
|:---:|:---:|:---:|:---|:---|
| **0.50** | 14 | 0.008s | p00009, p00001, p00006 | Base ranking (p00000: 7th, p00004: 8th) |
| **0.70** | 17 | 0.010s | p00009, p00001, p00006 | **First change**: p00004 & p00000 swap positions |
| **0.85** | 20 | 0.011s | p00009, p00001, p00006 | Stable with $\beta=0.70$ order |
| **0.95** | 23 | 0.012s | p00009, p00001, p00006 | Stable with $\beta=0.85$ order |
| **0.99** | 24 | 0.014s | p00009, p00001, p00006 | Stable with $\beta=0.85$ order |

---

## A3 · Shape of the Curve and Behavior as $\beta \to 1$

As $\beta$ increases, the required iteration count grows monotonically and its derivative slows down.
- **Mathematical reason**: In power iteration, the convergence rate is determined by the spectral gap $1 - |\lambda_2|$ of the transition matrix. For PageRank with uniform teleportation, $|\lambda_2| \le \beta$. The error vector at iteration $k$ contracts by at least a factor of $\beta$ each step ($e_k \le \beta^k e_0$). As $\beta \to 1$, the contraction factor approaches 1, diminishing the per-step shrinkage and requiring significantly more iterations to satisfy $L_1 < \text{tol}$.
- **Physical intuition**: The teleport probability $1 - \beta$ acts as a restorative force, constantly pulling the random surfer uniformly across all nodes and rapidly smoothing probability mass. As $\beta \to 1$, teleportation vanishes, and probability diffuses solely through graph paths, taking much longer to escape near-traps and cycles.

---

## A4 · Graph Size Scaling: Iterations vs. Wall Time

Comparing two graph sizes ($N = 1,200$ vs. $N = 20,000$, a **16.7×** size difference) at $\text{tol} = 10^{-10}$:

| Graph Size ($N$) | $\beta = 0.85$ (iters / time) | $\beta = 0.95$ (iters / time) |
|:---|:---:|:---:|
| **1,200 nodes** | 20 iters / 0.011s | 23 iters / 0.012s |
| **20,000 nodes** | 21 iters / 0.255s | 24 iters / 0.249s |

- **Iteration Count**: Barely changes (20 $\to$ 21 for $\beta=0.85$, 23 $\to$ 24 for $\beta=0.95$). The mixing time of expander / scale-free networks is governed by graph diameter and degree distribution, which grow logarithmically with $N$. Hence, spectral convergence is largely scale-invariant.
- **Wall Time**: Grows roughly linearly with the number of edges $O(|E|)$ (from ~0.011s to ~0.255s, a ~23× increase matching the edge expansion). Each iteration must iterate over every active node and its edge list.

---

## A5 · Tolerance Scaling: Cost per Digit of Accuracy

Comparing tolerances with $\beta = 0.85$ on $N = 1,200$:
- $\text{tol} = 10^{-6}$: **12 iterations** (0.007s)
- $\text{tol} = 10^{-10}$: **20 iterations** (0.011s)
- **Cost**: A difference of $10^{-4}$ (4 decimal digits) cost **8 iterations**, which is exactly **2 extra iterations per decimal digit** of precision. This matches the theoretical rate where $\beta^2 = 0.85^2 \approx 0.72$, steadily shrinking residual $L_1$ norm.

---

## A6 · Stability of Top-10 Rankings Across $\beta$

- **When does it first change?**: The ranking first changes between **$\beta = 0.50$** and **$\beta = 0.70$**.
  - At $\beta = 0.50$: 7th is `p00000`, 8th is `p00004`.
  - At $\beta = 0.70$: `p00004` overtakes `p00000` to become 7th, pushing `p00000` to 8th.
  - The top 6 nodes (`p00009`, `p00001`, `p00006`, `p00005`, `p00003`, `p00002`) remain completely stable throughout $\beta \in [0.5, 0.99]$.
- **Implication**: Lower $\beta$ emphasizes immediate in-degree and local connectivity (closer to uniform distribution), whereas higher $\beta$ allows multi-step transitive authority to accumulate. The choice of $\beta = 0.85$ directly influences boundary rankings; published rankings are subjective to this parameter tuning.

---

## A7 · Machine Information
- **Platform**: `Windows-11-10.0.26200-SP0`
- **Processor**: `AMD64 Family 25 Model 97 Stepping 2, AuthenticAMD`
- **Python**: `3.14.8`

