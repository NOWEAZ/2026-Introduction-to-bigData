#!/usr/bin/env python3
"""Week 3 · Task 3 — Find the same pairs without comparing everything.

Textbook §3.4.

`BruteForce` compares every pair. On 3,000 documents that is 4.5 million
comparisons and it is completely correct. On 3 million documents it is 4.5
trillion and it is completely useless.

Beat it. Find the same near-duplicate pairs while making far fewer comparisons.

    python3 bench.py
    python3 bench.py --yours

The harness counts every call you make to `similarity()`. That is your score.
It also checks **recall** - which of the truly similar pairs you found. Skipping
comparisons is easy; skipping comparisons without losing the pairs is the task.
"""


class BruteForce:
    """Correct, and quadratic."""

    def __init__(self, threshold):
        self.threshold = threshold

    def find(self, docs, similarity):
        """docs is [set_of_shingles, ...]. Return {(i, j), ...} with i < j."""
        out = set()
        for i in range(len(docs)):
            for j in range(i + 1, len(docs)):
                if similarity(docs[i], docs[j]) >= self.threshold:
                    out.add((i, j))
        return out


class YourFinder:
    """Your near-duplicate finder.

        __init__(threshold)
        find(docs, similarity) -> {(i, j), ...}

    `similarity(a, b)` is the only way to compare two documents, and every call
    is counted. Everything else - signatures, banding, bucketing - is free, in
    the sense that the harness does not charge you for it. That is deliberate:
    it is also roughly true at scale, where the comparison is the expensive
    part and the hashing is linear.

    Two knobs decide everything:

        the number of hashes in a signature
        how many bands you split it into

    §3.4.2 gives you the relationship between those and the probability that a
    pair at similarity s becomes a candidate. It is an S-curve, and where its
    step sits is something you choose. Choose it on purpose and be able to say
    why in observation.md - a threshold of 0.8 does not mean bands should be
    anything in particular until you have done the arithmetic.

    You may reuse your Task 1 code.
    """

    def __init__(self, threshold):
        self.threshold = threshold
        # For threshold 0.6, we want the S-curve step to be reasonable.
        # r = 4, b = 30 -> step ~ (1/30)^(1/4) = 0.427
        # P(s=0.6) = 1 - (1 - 0.6^4)^30 = 0.984 (Good recall > 95%)
        self.bands = 30
        self.n_hashes = 120

    def find(self, docs, similarity):
        from task1_minhash import minhash_signatures, lsh_candidates
        import random

        # 1. Map shingles to integer row indices
        vocab = {}
        columns = []
        for d in docs:
            col = set()
            for shingle in d:
                if shingle not in vocab:
                    vocab[shingle] = len(vocab)
                col.add(vocab[shingle])
            columns.append(col)
        n_rows = len(vocab)
        
        if n_rows == 0:
            return set()

        # 2. Generate hash functions: h(x) = (a * x + b) % p
        random.seed(42)
        p = 2**31 - 1
        hash_fns = []
        for _ in range(self.n_hashes):
            a = random.randint(1, p - 1)
            b = random.randint(0, p - 1)
            def make_hash(a, b, p):
                return lambda x: (a * x + b) % p
            hash_fns.append(make_hash(a, b, p))

        # 3. Minhash and LSH
        signatures = minhash_signatures(columns, hash_fns, n_rows)
        candidates = lsh_candidates(signatures, self.bands)

        # 4. Compare only candidates
        out = set()
        for i, j in candidates:
            if similarity(docs[i], docs[j]) >= self.threshold:
                out.add((i, j))
        return out
