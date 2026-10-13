# Week 4 Observations

## Task 1
- **Bloom filter structural asymmetry**: A Bloom filter can never produce a false negative because inserted items set their corresponding $k$ bit positions to 1, and bits are never cleared back to 0. The predicted false-positive rate (§4.4.2) was 0.860% and measured was 0.880%, matching within expected sample error ($|0.880\% - 0.860\%| = 0.020\% \le 0.065\%$).
- **Flajolet-Martin combining rule**: Arithmetic averaging of $2^R$ produces ~2.8x-3.0x due to exponential outliers, while a pure median yields a coarse power-of-two 0.82x. Grouping into 4 groups of 16 (median within group, mean across groups) yields 22,528 (~1.13x of true 19,953), reliably landing well within the factor-of-two requirement.
- **Reservoir sampling**: By including the $i$-th item with probability $k / (i+1)$ (`if rng.randrange(i+1) < k: sample[j] = item`), every item seen has uniform inclusion probability $k / n$ at each step without knowing stream length or storing the stream.

## Task 2
- **Limit reached & bottleneck**: For the exact set, memory gives out first. Holding distinct strings in Python's hash set requires ~77.5 bytes per item; at $n \ge 25,000,000$ (~10M distinct items), memory reaches ~1 GB, and past $10^8$ items, physical RAM exhausts and triggers heavy swapping/OOM.
- **Growth rates**: Exact set memory grows linearly at $\approx 77.5\text{ bytes/item}$ ($O(N)$ growth), whereas Flajolet-Martin memory is completely flat at $\approx 0.013\text{ MB}$ ($O(1)$ growth, bounded strictly by the 64 hash counters).
- **Factor of two utility for distinct visitors**: A factor-of-two estimate is sufficient for capacity planning and detecting order-of-magnitude traffic surges (e.g., distinguishing 100K vs 1M visitors for infrastructure scaling), but unacceptable for ad billing, financial payouts, or SLA reporting where exact user counts are contractually audited.

## Task 3
- **Parameter changed & derivation**: Changed the number of hash functions from $k=1$ (baseline) to $k=7$. By §4.4.2, minimizing $P(k) = (1 - e^{-kn/m})^k$ with respect to $k$ yields $k_{\text{opt}} = \frac{m}{n} \ln 2$. For $m/n = 10$, $k_{\text{opt}} = 10 \ln 2 \approx 6.9315 \approx 7$.
- **R6 theoretical floor & reached rate**: The theoretical minimum error rate for $m/n = 10$ is $(1/2)^{10 \ln 2} \approx 0.819\%$. With $k=7$, our filter achieved a measured rate of **0.799%** (1,599 / 200,000 false positives), cutting mistakes by **91.6%** from the baseline's 9.511% and qualifying for the "strong" tier ($\le 0.9\%$).
- **If $n$ were unknown**: If $n$ is underestimated, the filter oversaturates and the false-positive rate degrades toward 100%; if overestimated, bits remain mostly 0 and memory is wasted, or $k$ is chosen suboptimally. In practice, one would use *Scalable Bloom Filters* (dynamically chaining new filters with geometrically decreasing error rates) or couple the filter with a cardinality sketch (Flajolet-Martin / HyperLogLog) to monitor stream volume in $O(1)$ memory.
