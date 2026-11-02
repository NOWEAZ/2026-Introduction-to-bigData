#!/usr/bin/env python3
"""Week 7 · Task 3 — The same clustering, with far fewer distances.

Textbook §7.3, and §7.1.3 for why distance is the expensive part.

`NaiveKMeans` does what the definition says: every iteration, compare every
point with every centroid. That is n x k distance computations per pass, and on
a real dataset the distance computation is almost the entire cost.

Most of that work is wasted. After the first couple of iterations, most points
do not change cluster, and most centroids barely move. The triangle inequality
lets you prove a point cannot have changed cluster **without measuring it**.

    python3 bench.py
    python3 bench.py --yours

Correctness first: your final SSE must match the baseline's. Fewer distances
with a worse clustering is not an improvement, it is a different algorithm.
"""


class NaiveKMeans:
    """Every point against every centroid, every iteration."""

    def __init__(self, k, max_iter=50):
        self.k, self.max_iter = k, max_iter

    def run(self, points, initial_centroids, distance):
        centroids = list(initial_centroids)
        labels = [None] * len(points)
        for self.iterations in range(1, self.max_iter + 1):
            changed = False
            for i, p in enumerate(points):
                best, bi = None, 0
                for j, c in enumerate(centroids):
                    d = distance(p, c)
                    if best is None or d < best - 1e-12:
                        best, bi = d, j
                if labels[i] != bi:
                    labels[i] = bi
                    changed = True
            centroids = _means(points, labels, self.k, centroids)
            if not changed:
                break
        return labels, centroids


def _means(points, labels, k, previous):
    out = []
    for j in range(k):
        group = [p for p, l in zip(points, labels) if l == j]
        if group:
            out.append(tuple(sum(v) / len(group) for v in zip(*group)))
        else:
            out.append(previous[j])
    return out


class YourKMeans:
    """Your k-means.

        __init__(k, max_iter=50)
        run(points, initial_centroids, distance) -> (labels, centroids)

    Same starting centroids, same `distance` function - which is counted. That
    counter is your score.

    The idea, from §7.3 and the triangle inequality:

        if a point is much closer to its current centroid than that centroid
        moved, and than any other centroid could have come, then it cannot have
        changed cluster, and you do not have to measure anything

    Keeping enough bookkeeping to make that test cheap, without keeping so much
    that the bookkeeping costs more than the distances, is the task.

    You may call `distance` on two centroids, and those calls are counted too -
    which is the correct accounting, since that is real work. There are k of
    them and n points, and k is much smaller than n. That asymmetry is the
    whole opening.
    """

    def __init__(self, k, max_iter=50):
        self.k, self.max_iter = k, max_iter

    def run(self, points, initial_centroids, distance):
        n = len(points)
        k = self.k
        centroids = list(initial_centroids)
        labels = [0] * n
        upper = [0.0] * n
        lower = [0.0] * n

        # Iteration 1: full pass to establish exact initial bounds
        self.iterations = 1
        for i, p in enumerate(points):
            best1, bi = None, 0
            best2 = float("inf")
            for j, c in enumerate(centroids):
                d = distance(p, c)
                if best1 is None or d < best1 - 1e-12:
                    if best1 is not None:
                        best2 = best1
                    best1, bi = d, j
                elif d < best2:
                    best2 = d
            labels[i] = bi
            upper[i] = best1
            lower[i] = best2

        new_centroids = _means(points, labels, k, centroids)
        if new_centroids == centroids:
            return labels, new_centroids

        for self.iterations in range(2, self.max_iter + 1):
            # Step 1: how far each centroid moved (k distance calls)
            delta = [distance(centroids[j], new_centroids[j]) for j in range(k)]
            centroids = new_centroids

            max1, max2, j_max1 = -1.0, -1.0, 0
            for j, d_move in enumerate(delta):
                if d_move > max1:
                    max2 = max1
                    max1 = d_move
                    j_max1 = j
                elif d_move > max2:
                    max2 = d_move

            # Half minimum inter-centroid distances (k*(k-1)/2 calls)
            s = [float("inf")] * k
            for j1 in range(k):
                c1 = centroids[j1]
                for j2 in range(j1 + 1, k):
                    half_d = 0.5 * distance(c1, centroids[j2])
                    if half_d < s[j1]:
                        s[j1] = half_d
                    if half_d < s[j2]:
                        s[j2] = half_d

            changed = False
            for i, p in enumerate(points):
                a = labels[i]
                u = upper[i] + delta[a]
                l = lower[i] - (max2 if a == j_max1 else max1)
                upper[i] = u
                lower[i] = l

                m = l if l > s[a] else s[a]
                if u <= m - 1e-11:
                    continue

                # Tighten upper bound to current assigned centroid (1 call)
                u = distance(p, centroids[a])
                upper[i] = u
                if u <= m - 1e-11:
                    continue

                # Point might move: check the other k - 1 centroids
                best1, bi = u, a
                best2 = float("inf")
                for j, c in enumerate(centroids):
                    if j == a:
                        continue
                    d = distance(p, c)
                    if (j < bi and d <= best1 + 1e-12) or (j > bi and d < best1 - 1e-12):
                        best2 = best1
                        best1, bi = d, j
                    elif d < best2:
                        best2 = d
                upper[i] = best1
                lower[i] = best2
                if bi != a:
                    labels[i] = bi
                    changed = True

            new_centroids = _means(points, labels, k, centroids)
            if not changed:
                centroids = new_centroids
                break

        return labels, centroids
