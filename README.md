# 🧠 PSO-Guided Construction of MRD Codes in Rank Metric

This repository provides a Python implementation of **Particle Swarm Optimization (PSO)** to discover and construct **Maximum Rank Distance (MRD) codes** in the **rank metric** space, using proper algebraic operations over finite fields \( \mathbb{F}_{q^m} \).

## 🔧 Features

- Implements a PSO algorithm tailored for rank-metric code construction.
- Operates over **finite fields** using [`galois`](https://github.com/mhostetter/galois).
- Supports calculation of:
  - **Minimum Rank Distance** (core MRD property)
  - **Generalized Rank Weights** (optional)
- Demonstrates search over the space of generator matrices to find optimal codes.

---

## 📖 Background

MRD codes are analogues of MDS codes under the rank metric. Their key property is achieving the **Singleton-like bound**:

\[
d \leq \min(n, m) - k + 1
\]

Constructing MRD codes (e.g., Gabidulin codes) algebraically is known but limited in generality. This repo explores a **metaheuristic approach** using PSO to discover MRD codes from scratch, enabling discovery in underexplored parameter regimes.

---

## 🧪 Example Usage

```python
from pso_mrd import pso_mrd_field

# Search for [n=4, k=2] MRD code over GF(2^3) with target d=3
G, d = pso_mrd_field(q=2, m=3, k=2, n=4, d_target=3, use_generalized_weight=True)
print("Best Generator Matrix Found:\n", G)
print("Minimum Rank Distance:", d)
```

---

## 🐍 Requirements

- Python 3.8+
- [`galois`](https://github.com/mhostetter/galois) library
```bash
pip install galois
```

---

## 📁 File Structure

```
pso_mrd.py      # Core implementation
README.md       # This file
```

---

## 🚀 How It Works

1. Particles are initialized as random generator matrices over \(\mathbb{F}_{q^m}\).
2. Fitness is evaluated via **minimum rank distance**.
3. PSO updates are applied using binary thresholded velocities.
4. The global best solution (max rank distance) is returned.

---

## 📚 References

- Gabidulin, E. M. (1985). *Theory of codes with maximum rank distance.*
- Delsarte, P. (1978). *Bilinear forms over a finite field with applications to coding theory.*
- Sheekey, J. (2016). *A new family of linear maximum rank distance codes.*

---

## 📬 License

MIT License – use it, modify it, cite it 🚀
