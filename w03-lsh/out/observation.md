## Task 1
- **Why one pass over the rows, rather than one pass per column?**
  In large-scale data processing, the matrix may be too large to fit in memory. Scanning row by row allows us to process the data as a stream without loading the entire matrix. Re-scanning per column or sorting requires random access or holding everything in memory.
- **Your R5 decision on the leftover rows**
  If the signature length does not evenly divide by the number of bands, `lsh_candidates` raises a `ValueError`. This strict approach avoids bugs from unevenly sized bands or silently dropped signature data.
- **The estimate for S1-S4 was 1.0 and the truth is 2/3. What would you change to narrow that, and what would it cost?**
  We should increase the number of hash functions to generate longer signatures. The cost is increased memory usage for storing the signatures and extra CPU time to compute the additional hashes.


## Task 2
- **Crossover n and Machine:**
  The crossover happened between `n=500` and `n=1000` (roughly around ~750). The machine is an AMD64 CPU running Windows 11.
- **Quadratic check:**
  Yes. Time went from 0.25s (250) -> 1.01s (500) -> 5.47s (1000) -> 20.85s (2000). The ratios are roughly $4\times$, which perfectly aligns with the $O(n^2)$ prediction.
- **The size where it became unpleasant:**
  At `n=4000`, brute force takes over a minute, and at `n=8000` it takes over 5 minutes. Time ran out (patience) much faster than memory, as brute force only used a few dozen kilobytes of peak memory.

## Task 3
- **Choice of `n` and `b`, the step, and why there:**
  I chose `n_hashes = 120` and `bands = 30`, meaning `r = 4` rows per band.
  The step sits roughly around $(1/30)^{1/4} \approx 0.42$. 
  I aimed for a step below the threshold (0.6) to guarantee extremely high recall at $s \ge 0.6$. The probability of a candidate at $s=0.6$ is $1 - (1 - 0.6^4)^{30} \approx 0.984$. The cost is doing a few extra comparisons on false positives, but since average random similarity is very low, it still avoids >99.9% of total comparisons.
- **What happened to recall when moving the step the wrong way:**
  When I originally tested with a higher step (e.g. `n=720`, `b=120`, `r=6`), the step was around `0.45` but evaluating it was extremely slow. If I used `n=240, b=40, r=6` (step ~ `0.54`), recall dropped to ~85% because it was too close to the 0.6 threshold, missing some genuine pairs.
- **At what scale would "hashing is free" stop being a fair simplification?**
  When document sizes or vocabularies are massive, and the number of hash functions `n` is large, computing $O(n \times \text{vocab})$ hashes can dominate. In pure Python, evaluating 100+ hash functions across millions of shingles introduces a massive constant factor that eclipses the fast $O(1)$ native set intersections.
