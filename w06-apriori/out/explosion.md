# Task 2 · The Support Explosion Curve

## A3 · Table of Results

Measured on 20,000 baskets, 2,000 items (spanning support 400 down to 3, a **133×** range):

| Support ($s$) | Frequent Pairs | Peak Counters | Memory (Peak MB) | Runtime (s) | Growth Factor (Counters) | Growth Factor (Pairs) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **400** | 249 | 10,585 | 1.1 MB | 0.37s | — | — |
| **200** | 776 | 58,626 | 6.7 MB | 0.60s | **5.54×** | **3.12×** |
| **100** | 2,244 | 273,701 | 28.6 MB | 1.36s | **4.67×** | **2.89×** |
| **50** | 6,397 | 820,259 | 107.7 MB | 2.09s | **3.00×** | **2.85×** |
| **25** | 17,045 | 893,456 | 107.7 MB | 2.61s | 1.09× (saturating) | **2.66×** |
| **12** | 43,116 | 893,456 | 110.0 MB | 2.95s | 1.00× (ceiling) | **2.53×** |
| **6** | 101,938 | 893,456 | 126.5 MB | 3.28s | 1.00× (ceiling) | **2.36×** |
| **3** | 250,054 | 893,456 | 163.9 MB | 2.93s | 1.00× (ceiling) | **2.45×** |

---

## A4 · Counter Growth Rate vs. Halving Support

- **Measured Rate**: When support is halved from 400 $\to$ 200, counters explode by **5.54×**. From 200 $\to$ 100, counters expand by **4.67×**, and from 100 $\to$ 50, by **3.00×**.
- **Explanation**: The growth is far worse than doubling per halving ($> 4\times$ to $5.5\times$). In A-Priori, lowering the threshold increases the number of frequent singletons $L_1$. Because pass two counts every pair of items in $L_1$, the number of candidate pairs scales quadratically as $\binom{|L_1|}{2} \approx \frac{1}{2} |L_1|^2$. A modest expansion in surviving singletons causes a quadratic surge in the pair counters that pass two must allocate.
- **Saturation**: Around $s = 25$, almost all 2,000 items qualify as frequent singletons. At that point, the candidate counters hit the physical ceiling of all 893,456 distinct co-occurring pairs that actually exist in the 20,000 baskets.

---

## A5 · The Gap Between Answers and Counters

- **Growth of Answers**: As support is halved, the number of true frequent pairs grows at a steady rate of **$\approx 2.5\times - 3.1\times$** across the entire span (249 $\to$ 776 $\to$ 2,244 $\to$ 6,397 $\to$ 17,045 $\to$ 43,116 $\to$ 101,938 $\to$ 250,054).
- **The Divergence**: At support 400, only 10,585 counters are needed to discover 249 frequent pairs (ratio of ~42 counters per answer). At support 50, finding 6,397 frequent pairs requires holding **820,259 counters** in memory (ratio of ~128 counters per answer).
- **Why this gap is the central problem**: Most allocated counters in pass two belong to candidate pairs that ultimately fail the threshold (transient false candidates). You pay massive memory costs for pairs you will throw away. This gap is the precise motivation for hash-filtered approaches like **PCY (§6.3)**, which weed out unpromising pairs using a compact bitmap before allocating full pair counters.

---

## A2 · The Breaking Point

- Below support $s \approx 25$, the single-machine baseline encounters memory strain: memory consumption rises past 160 MB and runtime increases. On larger real-world datasets with tens of thousands of items, lowering support past this inflection point causes pair counters to exceed available RAM, leading to fatal memory allocation failure (`MemoryError`) or severe OS disk swapping.

---

## A6 · Machine Specification
- **Platform**: `Windows-11-10.0.26200-SP0`
- **Processor**: `AMD64 Family 25 Model 97 Stepping 2, AuthenticAMD`
- **Python**: `3.14.8`

