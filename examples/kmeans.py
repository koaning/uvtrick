import random
from uvtrick import Env 


def bench():
    from sklearn.datasets import make_regression
    from time import time
    from sklearn.cluster import KMeans

    X, y = make_regression(n_samples=10_000, n_features=10, random_state=42)
    tic = time()
    pca = KMeans().fit(X, y)
    toc = time()
    return toc - tic

def combiner(pairs, times=4):
    combos = []
    for pkg, py in pairs:
        for i in range(times):
            combos.append([pkg, py, i])
    random.shuffle(combos)
    return combos

combos = combiner(
    pairs=[("0.22", "3.7"), ("0.23", "3.7"), ("0.24", "3.7"), ("1.4", "3.9"), ("1.5", "3.9")], 
    times=10
)

results = []
for version, py, i in combos:
    timed = Env(f"scikit-learn=={version}", python=py).run(bench)
    results.append({
        "i": i, 
        "version": version,
        "python": py,
        "time": timed
    })
    print(version, timed)

import polars as pl

pl.DataFrame(results).sort("version").write_csv("results.csv")