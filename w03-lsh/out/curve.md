## Crossover Measurement (Task 2)

**A6. Machine Details**
- **CPU:** AMD64 Family 25 Model 117 Stepping 2, AuthenticAMD
- **RAM:** Unknown exactly, but likely 16GB+ on standard setup. No other heavy jobs running.
- **Platform:** Windows 11 (10.0.26200-SP0) / Python 3.14.7

**A3. Timing and Memory Curve**
| n | Brute Force Time (s) | Brute Force Peak Mem | LSH Time (s) | LSH Peak Mem |
|---|---|---|---|---|
| 250 | 0.25 | ~7 KB | 1.48 | ~1.7 MB |
| 500 | 1.01 | ~7.8 KB | 2.48 | ~2.8 MB |
| 1000 | 5.47 | ~9.3 KB | 4.37 | ~4.7 MB |
| 2000 | 20.85 | ~21 KB | 8.15 | ~8.5 MB |
| 4000 | ~83.0 (est) | ~40 KB | ~16.0 (est) | ~17 MB |

**A4. Quadratic Check for Brute Force**
- `n=250` to `n=500`: 0.25s to 1.01s (ratio 4.04x)
- `n=500` to `n=1000`: 1.01s to 5.47s (ratio 5.4x)
- `n=1000` to `n=2000`: 5.47s to 20.85s (ratio 3.81x)
Yes, the time roughly quadruples every time `n` doubles, confirming the expected $O(n^2)$ behavior.

**A5. Peak Memory at Largest n**
At `n=2000`:
- Brute Force: 21,256 bytes
- LSH: 8,503,256 bytes (~8.5 MB)
LSH uses significantly more memory to store the signature matrix and the hash buckets.

**A7. Crossover Point**
Brute force is faster at small $n$. 
- At `n=500`, Brute force (1.01s) is faster than LSH (2.48s).
- At `n=1000`, Brute force (5.47s) is slower than LSH (4.37s).
The crossover point on this machine is approximately around $n = 700 \sim 800$.

**A8. Why LSH loses at small n**
LSH performs an up-front cost of hashing every document multiple times (120 hashes per document) and placing them into buckets across multiple bands. This $O(n)$ setup has a high constant factor. When $n$ is small, the total number of $O(n^2)$ comparisons is tiny, making brute force extremely cheap and bypassing the heavy linear setup cost of LSH.

